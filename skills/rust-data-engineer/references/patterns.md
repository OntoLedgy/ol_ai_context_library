# Rust Patterns

---

## Builder Pattern (construction with many optional fields)

```rust
#[derive(Debug)]
pub struct PipelineConfig {
    source_path: String,
    batch_size: usize,
    max_retries: u32,
}

pub struct PipelineConfigBuilder {
    source_path: String,
    batch_size: usize,
    max_retries: u32,
}

impl PipelineConfigBuilder {
    pub fn new(source_path: impl Into<String>) -> Self {
        Self {
            source_path: source_path.into(),
            batch_size: 100,
            max_retries: 3,
        }
    }

    pub fn batch_size(mut self, batch_size: usize) -> Self {
        self.batch_size = batch_size;
        self
    }

    pub fn max_retries(mut self, max_retries: u32) -> Self {
        self.max_retries = max_retries;
        self
    }

    pub fn build(self) -> PipelineConfig {
        PipelineConfig {
            source_path: self.source_path,
            batch_size: self.batch_size,
            max_retries: self.max_retries,
        }
    }
}

// Usage
let config = PipelineConfigBuilder::new("data/input.csv")
    .batch_size(500)
    .build();
```

Use when construction requires many optional parameters. Avoids long function signatures.

---

## Newtype Pattern (type safety over primitives)

```rust
// Prevent mixing up semantically different IDs
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct TransactionId(String);

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct AccountId(String);

impl TransactionId {
    pub fn new(id: impl Into<String>) -> Self {
        Self(id.into())
    }
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

// Compiler prevents: fn expecting TransactionId from receiving AccountId
fn find_transaction(id: &TransactionId) -> Option<TransactionRecord> { ... }
```

---

## Option and Result combinators

```rust
// Option
let amount = record.amount
    .filter(|&a| a > 0.0)       // Some only if positive
    .map(|a| a * 1.1)           // transform
    .unwrap_or(0.0);             // default if None

// Result
let processed = parse_record(raw)
    .map(|r| enrich_record(r))              // transform on Ok
    .map_err(|e| ProcessingError::from(e))  // transform error type
    .and_then(|r| validate_record(r))?;     // chain fallible op, propagate with ?

// Convert between Option and Result
let record = find_record(id)
    .ok_or_else(|| ProcessingError::NotFound { id: id.to_string() })?;
```

---

## Trait Objects vs Generics

```rust
// Generics (static dispatch — preferred when possible)
// Monomorphised at compile time; zero runtime cost
pub fn process<R: RecordReader, W: RecordWriter>(reader: &R, writer: &W) { ... }

// Trait objects (dynamic dispatch — use when you need heterogeneity)
// Runtime dispatch via vtable
pub fn build_pipeline(stages: Vec<Box<dyn PipelineStage>>) -> Pipeline { ... }
pub fn process(reader: &dyn RecordReader, writer: &dyn RecordWriter) { ... }
```

Prefer generics. Use `dyn Trait` when you genuinely need a heterogeneous collection or late binding.

---

## Iterator Adapters

```rust
// Prefer iterator chains over manual loops
let valid_totals: Vec<f64> = records
    .iter()
    .filter(|r| r.is_valid())
    .map(|r| r.amount)
    .collect();

// Custom iterator for lazy sequences
pub struct BatchIterator<'a> {
    source: &'a [TransactionRecord],
    batch_size: usize,
    position: usize,
}

impl<'a> Iterator for BatchIterator<'a> {
    type Item = &'a [TransactionRecord];

    fn next(&mut self) -> Option<Self::Item> {
        if self.position >= self.source.len() { return None; }
        let end = (self.position + self.batch_size).min(self.source.len());
        let batch = &self.source[self.position..end];
        self.position = end;
        Some(batch)
    }
}
```

---

## Async Patterns (Tokio)

```rust
use tokio::fs::File;
use tokio::io::{AsyncBufReadExt, BufReader};

// Process records as they arrive
pub async fn process_stream(path: &str) -> Result<(), AppError> {
    let file = File::open(path).await?;
    let reader = BufReader::new(file);
    let mut lines = reader.lines();

    while let Some(line) = lines.next_line().await? {
        let record = parse_line(&line)?;
        process_record(record).await?;
    }
    Ok(())
}

// Concurrent bounded (avoid spawning unbounded tasks)
use tokio::sync::Semaphore;
use std::sync::Arc;

let semaphore = Arc::new(Semaphore::new(10));  // max 10 concurrent
let mut handles = Vec::new();

for record in records {
    let permit = semaphore.clone().acquire_owned().await?;
    handles.push(tokio::spawn(async move {
        let _permit = permit;  // drops when task completes
        process_record(record).await
    }));
}

for handle in handles {
    handle.await??;
}
```
