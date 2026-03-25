# Rust Language Standards

---

## Naming

| Symbol | Convention | Example |
|--------|-----------|---------|
| Functions / methods | `snake_case` | `process_batch()`, `load_records()` |
| Structs / enums / traits | `PascalCase` | `TransactionRecord`, `ProcessingError`, `RecordReader` |
| Variables / parameters | `snake_case` | `transaction_count`, `source_path` |
| Constants / statics | `UPPER_SNAKE_CASE` | `MAX_BATCH_SIZE: usize = 500` |
| Modules | `snake_case` | `mod transaction_processor;` |
| Files | `snake_case.rs` | `transaction_processor.rs` |
| Lifetimes | single lowercase letter or short word | `'a`, `'record` |
| Type parameters | single uppercase or descriptive | `T`, `E`, `TRecord` |
| Trait associated types | `PascalCase` | `type Output = TransactionRecord;` |

---

## Ownership and Borrowing

The three rules, always:

1. Each value has one owner
2. There can be any number of immutable references (`&T`) OR exactly one mutable reference (`&mut T`) — never both
3. References must not outlive their owner

```rust
// Immutable by default
let count = 0;
let mut count = 0;   // explicit opt-in to mutability

// Borrowing — prefer references over ownership transfer
fn process(record: &TransactionRecord) -> ProcessedRecord { ... }

// When you need ownership
fn take_and_transform(record: TransactionRecord) -> ProcessedRecord { ... }

// Clone deliberately — not as a reflex to fix borrow errors
let record_copy = record.clone();   // document WHY a clone is needed
```

---

## Structs and Enums

```rust
// Value object — derive common traits
#[derive(Debug, Clone, PartialEq)]
pub struct TransactionRecord {
    pub id: String,
    pub amount: f64,
    pub currency: String,
}

// State/error enum
#[derive(Debug, thiserror::Error)]
pub enum ProcessingError {
    #[error("invalid record id: {0}")]
    InvalidId(String),

    #[error("amount must be positive, got {0}")]
    InvalidAmount(f64),

    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
}
```

---

## Traits (interfaces)

```rust
// Define the interface as a trait
pub trait RecordReader {
    fn read(&self) -> Result<Vec<TransactionRecord>, ProcessingError>;
}

pub trait RecordWriter {
    fn write(&self, records: &[TransactionRecord]) -> Result<(), ProcessingError>;
}

// Implement for concrete types
impl RecordReader for CsvRecordReader {
    fn read(&self) -> Result<Vec<TransactionRecord>, ProcessingError> {
        ...
    }
}

// Generic over the trait (static dispatch — zero cost)
pub fn run_pipeline<R: RecordReader, W: RecordWriter>(
    reader: &R,
    writer: &W,
) -> Result<(), ProcessingError> {
    let records = reader.read()?;
    writer.write(&records)
}

// Dynamic dispatch (when needed for heterogeneous collections or late binding)
pub fn run_pipeline(
    reader: &dyn RecordReader,
    writer: &dyn RecordWriter,
) -> Result<(), ProcessingError> { ... }
```

---

## Error Handling

```rust
use thiserror::Error;

// Library code: typed error enum
#[derive(Debug, Error)]
pub enum AppError {
    #[error("record not found: {id}")]
    NotFound { id: String },

    #[error("validation failed: {0}")]
    Validation(String),

    #[error(transparent)]
    Io(#[from] std::io::Error),
}

// ? operator propagates errors
fn load_and_process(path: &str) -> Result<Vec<ProcessedRecord>, AppError> {
    let content = std::fs::read_to_string(path)?;   // io::Error converted by #[from]
    let records = parse_records(&content)?;
    Ok(records.into_iter().map(process_record).collect())
}

// Never in production logic:
// .unwrap()             — panics on Err
// .expect("...")        — panics with message (OK for startup/tests)
// panic!("...")         — for truly impossible states only
```

---

## Closures and Iterators

```rust
// Iterator chains are idiomatic Rust — prefer over manual loops
let totals: Vec<f64> = records
    .iter()
    .filter(|r| r.amount > 0.0)
    .map(|r| r.amount)
    .collect();

let total: f64 = records.iter().map(|r| r.amount).sum();

// Group by (use itertools crate)
use itertools::Itertools;
let by_currency = records.iter().into_group_map_by(|r| &r.currency);

// Lazy chains — nothing executes until .collect() or terminal op
records
    .iter()
    .filter(|r| r.is_valid())
    .map(|r| transform(r))
    .for_each(|r| write_record(&r));
```

---

## Visibility

```rust
// Default: private to module
struct InternalType { ... }

// Public to crate
pub(crate) struct CrateLocalType { ... }

// Public API
pub struct PublicType { ... }
pub fn public_function() { ... }

// Re-export controlled public API from lib.rs
pub use self::processor::TransactionProcessor;
```

Only expose what callers need. Internal implementation stays private.
