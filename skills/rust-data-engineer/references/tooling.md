# Rust Tooling

---

## Standard Toolchain

| Tool | Purpose | Config |
|------|---------|--------|
| `cargo` | Build, test, dependency management | `Cargo.toml` |
| `rustfmt` | Formatting | `rustfmt.toml` |
| `clippy` | Linting (goes well beyond warnings) | `Cargo.toml` `[lints]` |
| `cargo test` | Test runner (built-in) | `Cargo.toml` |
| `cargo-tarpaulin` or `cargo-llvm-cov` | Coverage | |

---

## Cargo.toml (baseline)

```toml
[package]
name = "transaction-pipeline"
version = "0.1.0"
edition = "2021"

[dependencies]
thiserror = "1"
serde = { version = "1", features = ["derive"] }
serde_json = "1"

# Async (if needed)
tokio = { version = "1", features = ["full"] }

# Iterator extensions
itertools = "0.13"

[dev-dependencies]
assert_matches = "1"

[lints.clippy]
pedantic = "warn"
all = "warn"
```

---

## rustfmt.toml

```toml
edition = "2021"
max_width = 100
use_small_heuristics = "Default"
imports_granularity = "Crate"
group_imports = "StdExternalCrate"
```

---

## Clippy configuration (Cargo.toml)

```toml
[lints.clippy]
all = "warn"
pedantic = "warn"
# Allow specific lints you've decided are acceptable
module_name_repetitions = "allow"  # common in Rust naming conventions
```

---

## Quality Gates

```bash
cargo build                        # compile
cargo clippy -- -D warnings        # lint (warnings become errors)
cargo fmt --check                  # format check (no changes)
cargo test                         # all tests pass
cargo test -- --nocapture          # show println! output during tests
cargo tarpaulin --out Html         # coverage report
```

Auto-fix:
```bash
cargo fmt                          # format in place
cargo clippy --fix                 # fix auto-fixable lints
```

---

## Test Structure

Tests live in the same file (unit) or in `tests/` (integration):

```rust
// In the same file as the code — unit tests
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn process_valid_record_returns_processed() {
        let record = TransactionRecord {
            id: "tx-1".to_string(),
            amount: 100.0,
            currency: "USD".to_string(),
        };

        let result = process_record(&record);

        assert!(result.is_ok());
        assert_eq!(result.unwrap().source_id, "tx-1");
    }

    #[test]
    fn process_negative_amount_returns_error() {
        let record = TransactionRecord { amount: -1.0, ..default_record() };

        let result = process_record(&record);

        assert!(matches!(result, Err(ProcessingError::InvalidAmount(_))));
    }
}

// Integration tests — tests/integration_test.rs
// (separate file; compiled as a separate crate; can only use public API)
#[test]
fn pipeline_processes_csv_file_end_to_end() {
    ...
}
```

---

## Async (Tokio)

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

```rust
#[tokio::main]
async fn main() -> Result<(), AppError> {
    run_pipeline().await
}

// Async trait (requires async-trait crate for Rust < 1.75, native in 1.75+)
pub trait RecordReader {
    async fn read(&self) -> Result<Vec<TransactionRecord>, ProcessingError>;
}
```
