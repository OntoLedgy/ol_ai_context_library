# Clean Code Tests — Rust

Language-specific testing patterns for Rust.
Read alongside `references/testing-philosophy.md` and `references/testing-standards.md`.

---

## Framework and Tooling

| Tool | Purpose |
|------|---------|
| `#[test]` (std) | Built-in unit test attribute — no external crate needed |
| `#[tokio::test]` | Async test runner (tokio runtime) |
| `mockall` | Mock trait implementations — `#[automock]` |
| `rstest` | Parametrised tests and fixture injection |
| `tempfile` | Temporary directories and files in tests |
| `assert_matches!` | Pattern-matching assertions (stable since 1.73) |
| `cargo test` | Test runner |

---

## File and Module Structure

```rust
// src/module/component.rs

pub struct TransactionLoader {
    base_path: PathBuf,
}

impl TransactionLoader {
    pub fn load(&self, filename: &str) -> Result<Vec<Transaction>, LoadError> {
        // ...
    }
}

// ─── Tests ────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::PathBuf;
    use tempfile::TempDir;

    fn make_loader(dir: &TempDir) -> TransactionLoader {
        TransactionLoader { base_path: dir.path().to_path_buf() }
    }

    fn write_csv(dir: &TempDir, filename: &str, content: &str) {
        std::fs::write(dir.path().join(filename), content).unwrap();
    }

    #[test]
    fn load_returns_records_when_csv_is_valid() {
        // Arrange
        let dir = TempDir::new().unwrap();
        write_csv(&dir, "data.csv", "id,amount\n1,100\n2,200");
        let loader = make_loader(&dir);

        // Act
        let result = loader.load("data.csv");

        // Assert
        assert!(result.is_ok(), "Expected Ok, got: {:?}", result);
        let records = result.unwrap();
        assert_eq!(records.len(), 2);
    }

    #[test]
    fn load_returns_error_when_file_is_missing() {
        // Arrange
        let dir = TempDir::new().unwrap();
        let loader = make_loader(&dir);

        // Act
        let result = loader.load("missing.csv");

        // Assert
        assert!(result.is_err());
        assert_matches!(result.unwrap_err(), LoadError::FileNotFound { .. });
    }
}
```

Rules:
- Tests live in a `#[cfg(test)] mod tests` block in the same file as the code
- `use super::*` brings all items from the parent module into scope
- Integration tests live in `tests/` at the crate root (separate from source)
- Helper functions (`make_loader`, `write_csv`) are plain functions, not fixtures

---

## Naming

| Unit | Convention | Example |
|------|-----------|---------|
| Test function | `snake_case` — reads as a sentence | `load_returns_records_when_csv_is_valid` |
| Test module | `tests` (standard) or descriptive submodule | `mod load_tests` |
| Test helper | `make_<thing>` or `build_<thing>` | `make_loader`, `build_valid_record` |

Do not prefix with `test_` — the `#[test]` attribute makes the intent clear.

---

## Helper Functions (Builders)

Rust has no fixture injection built in. Use plain helper functions instead:

```rust
fn make_valid_record() -> Transaction {
    Transaction {
        id: "tx-001".to_string(),
        amount: 100.0,
        currency: "GBP".to_string(),
        timestamp: Utc::now(),
    }
}

fn make_loader_with_data(records: &[(&str, &str)]) -> (TempDir, TransactionLoader) {
    let dir = TempDir::new().unwrap();
    let mut csv = "id,amount\n".to_string();
    for (id, amount) in records {
        csv.push_str(&format!("{},{}\n", id, amount));
    }
    std::fs::write(dir.path().join("data.csv"), &csv).unwrap();
    let loader = TransactionLoader { base_path: dir.path().to_path_buf() };
    (dir, loader)  // return TempDir to keep it alive
}
```

---

## Error Path Testing

```rust
#[test]
fn load_returns_file_not_found_when_path_is_missing() {
    let dir = TempDir::new().unwrap();
    let loader = make_loader(&dir);

    let result = loader.load("nonexistent.csv");

    assert!(result.is_err());
    assert_matches!(
        result.unwrap_err(),
        LoadError::FileNotFound { ref path } if path.ends_with("nonexistent.csv")
    );
}

#[test]
fn parse_returns_parse_error_on_malformed_csv() {
    let result = parse_csv("id,amount\nnot-a-number,abc");

    assert_matches!(result.unwrap_err(), ParseError::InvalidField { line: 1, .. });
}
```

---

## Parametrised Tests (`rstest`)

```rust
use rstest::rstest;

#[rstest]
#[case("hello", "HELLO")]
#[case("world", "WORLD")]
#[case("",      ""     )]
fn transform_uppercases_input(#[case] input: &str, #[case] expected: &str) {
    let result = transform(input);
    assert_eq!(result, expected);
}

#[rstest]
#[case("../etc/passwd", "path traversal")]
#[case("/absolute",     "absolute path" )]
fn load_rejects_unsafe_paths(#[case] path: &str, #[case] expected_fragment: &str) {
    let result = load(path);
    assert!(result.is_err());
    let error_message = result.unwrap_err().to_string();
    assert!(
        error_message.contains(expected_fragment),
        "Expected error to contain '{}', got: '{}'",
        expected_fragment,
        error_message,
    );
}
```

---

## Async Tests

```rust
#[tokio::test]
async fn fetch_record_returns_result_for_valid_id() {
    // Arrange
    let mock_client = MockApiClient::new();
    mock_client.expect_get()
        .with(eq("record-1"))
        .returning(|_| Ok(Transaction { id: "record-1".into(), amount: 100.0 }));

    let service = RecordService::new(Arc::new(mock_client));

    // Act
    let result = service.fetch("record-1").await;

    // Assert
    assert!(result.is_ok());
    assert_eq!(result.unwrap().amount, 100.0);
}

#[tokio::test]
async fn fetch_record_propagates_network_error() {
    let mock_client = MockApiClient::new();
    mock_client.expect_get()
        .returning(|_| Err(ApiError::NetworkTimeout));

    let service = RecordService::new(Arc::new(mock_client));
    let result = service.fetch("any-id").await;

    assert_matches!(result.unwrap_err(), ServiceError::Api(ApiError::NetworkTimeout));
}
```

---

## Mocking with `mockall`

```rust
use mockall::{automock, predicate::*};

#[automock]
trait RecordRepository {
    fn find(&self, id: &str) -> Result<Transaction, RepoError>;
    fn save(&mut self, record: &Transaction) -> Result<(), RepoError>;
}

#[test]
fn process_saves_transformed_record() {
    // Arrange
    let mut mock_repo = MockRecordRepository::new();
    mock_repo.expect_find()
        .with(eq("tx-1"))
        .times(1)
        .returning(|_| Ok(Transaction { id: "tx-1".into(), amount: 50.0 }));

    mock_repo.expect_save()
        .times(1)
        .returning(|_| Ok(()));

    let processor = TransactionProcessor::new(mock_repo);

    // Act
    let result = processor.process("tx-1");

    // Assert
    assert!(result.is_ok());
}
```

---

## Integration Tests (crate-level `tests/`)

```rust
// tests/integration/csv_pipeline.rs

use std::path::PathBuf;
use tempfile::TempDir;
use my_crate::pipeline::Pipeline;

#[test]
fn run_pipeline_produces_expected_output_for_valid_csv() {
    // Arrange
    let dir = TempDir::new().unwrap();
    let input = dir.path().join("input.csv");
    let output = dir.path().join("output.json");
    std::fs::write(&input, "id,amount\n1,100\n2,200").unwrap();

    // Act
    Pipeline::run(&input, &output).unwrap();

    // Assert
    let result = std::fs::read_to_string(&output).unwrap();
    assert!(result.contains(r#""amount":100"#));
    assert!(result.contains(r#""amount":200"#));
}
```

---

## Assertion Style

```rust
// Equality
assert_eq!(result.len(), 3, "Expected 3 records, got {}", result.len());

// Inequality
assert_ne!(first_id, second_id);

// Boolean
assert!(result.is_ok(), "Expected Ok, got: {:?}", result);
assert!(result.is_err());

// Pattern matching (preferred for enums)
assert_matches!(result.unwrap_err(), LoadError::FileNotFound { .. });

// Struct fields
let record = result.unwrap();
assert_eq!(record.id, "tx-001");
assert!((record.amount - 100.0).abs() < f64::EPSILON);  // float comparison
```

---

## Anti-Patterns (Rust Specific)

| Anti-pattern | Why |
|--------------|-----|
| `.unwrap()` in assertion position without message | Panic message is useless — add `unwrap_or_else(\|e\| panic!("...: {e}"))` or assert first |
| `.unwrap()` in production code being tested via panic | Tests should verify `Result` / `Option` outcomes, not rely on panics |
| Ignoring `TempDir` return value | Drops immediately → directory deleted before test runs; bind to a variable |
| `#[allow(unused)]` on test fields | Suppresses legitimate warnings; prefer `_` prefix or remove the field |
| Testing `to_string()` output for error matching | Fragile — use `assert_matches!` on the enum variant instead |
