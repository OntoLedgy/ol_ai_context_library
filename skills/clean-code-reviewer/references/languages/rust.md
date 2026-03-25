# Clean Code Reviewer — Rust

Language-specific rules for applying clean coding standards to Rust code.
Read alongside the general standards in `prompts/coding/standards/clean_coding/`.

Note: Rust's compiler and Clippy enforce many clean coding rules automatically.
Focus the review on what they do not catch: intent, naming clarity, and design.

---

## Naming Violations

| Violation | Example | Rule |
|-----------|---------|------|
| Non-snake_case function/variable | `processRecord()`, `RecordCount` | Use `snake_case`: `process_record()`, `record_count` |
| Non-PascalCase type | `transaction_record`, `processing_error` | Structs/enums/traits use `PascalCase` |
| Non-UPPER_SNAKE_CASE constant | `max_batch: usize = 500` | Constants/statics: `MAX_BATCH: usize = 500` |
| Abbreviation | `txn`, `cfg`, `acct`, `rec` | Reveal intent: `transaction`, `configuration` |
| Single-letter type param where context unclear | `fn process<T>(item: T)` | Use descriptive: `fn process<TRecord>(record: TRecord)` |
| Non-verb method | `fn validation(&self)` | Methods are verbs: `fn validate_record(&self)` |

---

## Function Violations

| Violation | Rust-Specific Signal |
|-----------|---------------------|
| > 20 lines | Extract helper functions; Rust closures and iterators make this natural |
| > 3 parameters | Introduce a struct for related parameters |
| `.unwrap()` in non-test code | Replace with `?`, `.expect("context")`, or explicit match |
| `.expect("TODO")` or `.expect("fix later")` | The message must explain WHY this is expected to succeed |
| `panic!` for expected failure | Use `Result<T, E>` — panics are for programmer errors only |
| Ignoring `Result` with `let _ = ...` | Explicitly handle or document why it's safe to ignore |
| Clone as first resort | Only clone when ownership genuinely cannot be borrowed; comment why |

---

## Struct / Enum Violations (maps to Class rules)

| Violation | Rust-Specific Signal |
|-----------|---------------------|
| Public fields on structs with invariants | `pub amount: f64` with validity rules | Use private fields + constructor that validates |
| Missing `#[derive(Debug)]` | All public types should be debuggable | Add `#[derive(Debug)]` |
| Enum variants with unnamed fields | `Error(String, String)` | Use named fields: `Error { field: String, message: String }` |
| Large enum with many variants (>10) | Consider splitting into sub-enums | |
| Struct with > 7 fields | Consider whether it has a single responsibility | |

---

## Error Handling Violations

| Violation | Example | Rule |
|-----------|---------|------|
| `unwrap()` in production code | `.read_to_string(&mut s).unwrap()` | Use `?` or explicit error handling |
| String-typed errors | `Err("something went wrong".to_string())` | Define a typed error enum with `thiserror` |
| Missing `#[from]` on wrapping errors | Manual `map_err` for every underlying error type | Use `#[from]` in the error enum |
| Discarding error context | `map_err(\|_\| MyError::Io)` loses original | Preserve original: `map_err(\|e\| MyError::Io(e))` |
| Mixing `panic!` and `Result` in same layer | — | Choose one strategy per layer; panics in library code are always wrong |

---

## Smell Violations

| Smell | Rust-Specific Signal |
|-------|---------------------|
| Magic number | `if count > 47`, `Duration::from_millis(300)` | Extract as `const MAX_RETRY: u32 = 47` |
| Repeated `.clone()` chains | `a.clone()`, `b.clone()` throughout a function | Restructure to borrow; clone only once at boundary |
| `Box<dyn Trait>` where generics suffice | — | Prefer static dispatch; use `dyn` only when heterogeneity is needed |
| `pub` on everything | All fields/methods `pub` | Only expose what callers need |
| `unsafe` without comment | `unsafe { ... }` with no explanation | Document the invariant being upheld |
| Dead code (`#[allow(dead_code)]`) | — | Delete unused code; don't suppress the warning |

---

## Clippy as First Pass

Before applying this checklist, run:
```bash
cargo clippy -- -D warnings
```

Clippy catches many violations automatically (naming conventions, common anti-patterns,
missing derives). The clean code reviewer focuses on what Clippy does not:
intent-revealing names, single responsibility, and design-level smells.

---

## Size Reference (Rust)

| Unit | Max | Note |
|------|-----|------|
| Function body | 20 lines | Excluding signature |
| `impl` block | 200 lines total | Over this, consider splitting the type's responsibilities |
| Struct fields | 7 | More fields often signals multiple responsibilities |
| Parameters | 3 | More → introduce a struct |
| Match arms | 10 | Over this, consider extracting per-arm logic to functions |
