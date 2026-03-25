# Clean Code Refactor — Rust

Language-specific refactoring patterns for Rust.
Read alongside the general `clean-code-refactor` SKILL.md.

---

## Naming Fixes

| Violation | Before | After |
|-----------|--------|-------|
| Non-snake_case function | `processRecord()` | `process_record()` |
| Non-PascalCase type | `transaction_record` struct | `TransactionRecord` |
| Abbreviation | `fn proc_txn`, `let cfg` | `fn process_transaction`, `let configuration` |
| Non-UPPER_SNAKE_CASE constant | `const max_batch: usize = 500` | `const MAX_BATCH: usize = 500` |
| Non-verb method | `fn validation(&self)` | `fn validate_record(&self)` |

---

## Function Extraction (Rust)

```rust
// Before — one function handling everything
fn process_data(
    records: &[RawRecord],
    config: &Config,
    output_path: &str,
) -> Result<(), AppError> {
    // 60 lines: validation, transformation, writing
    ...
}

// After
fn process_data(
    records: &[RawRecord],
    config: &Config,
    output_path: &str,
) -> Result<(), AppError> {
    let validated = validate_records(records)?;
    let transformed = transform_records(&validated, config);
    write_results(&transformed, output_path)
}

fn validate_records(records: &[RawRecord]) -> Result<Vec<TransactionRecord>, AppError> {
    ...
}

fn transform_records(
    records: &[TransactionRecord],
    config: &Config,
) -> Vec<ProcessedRecord> {
    ...
}

fn write_results(records: &[ProcessedRecord], output_path: &str) -> Result<(), AppError> {
    ...
}
```

---

## Parameter Reduction (Rust)

```rust
// Before — too many parameters
fn create_record(
    name: String,
    amount: f64,
    currency: String,
    source: String,
    timestamp: DateTime<Utc>,
) -> Record { ... }

// After — introduce a struct
pub struct CreateRecordRequest {
    pub name: String,
    pub amount: f64,
    pub currency: String,
    pub source: String,
    pub timestamp: DateTime<Utc>,
}

fn create_record(request: CreateRecordRequest) -> Record { ... }
```

---

## `.unwrap()` Removal (Rust)

```rust
// Before — unwrap in production code
let record = db.find(id).unwrap();
let content = fs::read_to_string(path).unwrap();

// After — propagate with ?
fn load_record(id: &str) -> Result<Record, AppError> {
    let record = db.find(id)?;
    Ok(record)
}

fn read_file(path: &str) -> Result<String, AppError> {
    let content = fs::read_to_string(path)?;
    Ok(content)
}

// Before — expect with no useful context
let value = map.get("key").expect("should be there");

// After — expect with invariant explanation
let value = map.get("key")
    .expect("'key' is always present — inserted during initialisation in new()");
```

---

## Error Handling Fixes (Rust)

```rust
// Before — string errors
fn load(path: &str) -> Result<Vec<Record>, String> {
    fs::read_to_string(path).map_err(|e| e.to_string())
}

// After — typed error enum with thiserror
#[derive(Debug, thiserror::Error)]
pub enum LoadError {
    #[error("failed to read file {path:?}: {source}")]
    Io {
        path: String,
        #[source]
        source: std::io::Error,
    },
    #[error("invalid record at line {line}: {message}")]
    Parse { line: usize, message: String },
}

fn load(path: &str) -> Result<Vec<Record>, LoadError> {
    let content = fs::read_to_string(path)
        .map_err(|source| LoadError::Io { path: path.to_string(), source })?;
    parse_records(&content)
}
```

---

## Smell Fixes (Rust)

```rust
// Before — magic numbers
if retry_count > 3 {
    std::thread::sleep(Duration::from_millis(500));
}

// After — named constants
const MAX_RETRY_COUNT: u32 = 3;
const RETRY_DELAY: Duration = Duration::from_millis(500);

if retry_count > MAX_RETRY_COUNT {
    std::thread::sleep(RETRY_DELAY);
}

// Before — unnecessary clone
fn process(record: &Record) -> Processed {
    let id = record.id.clone();  // clone of &str-backed field
    Processed { id, ..Default::default() }
}

// After — borrow instead
fn process(record: &Record) -> Processed {
    Processed { id: record.id.as_str(), ..Default::default() }
}
// Or if ownership is needed, document why:
let id = record.id.clone();  // owned String needed — passed to async task
```

---

## Pub Visibility Fix (Rust)

```rust
// Before — everything public
pub struct RecordProcessor {
    pub reader: CsvReader,
    pub records: Vec<Record>,
}

// After — minimal visibility
pub struct RecordProcessor {
    reader: CsvReader,         // internal — consumers use process()
    records: Vec<Record>,      // internal — mutable state
}

impl RecordProcessor {
    pub fn new(reader: CsvReader) -> Self { ... }
    pub fn process(&mut self) -> Result<(), AppError> { ... }
    pub fn results(&self) -> &[Record] { &self.records }
}
```
