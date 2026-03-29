# BORO Quick Style Guide — Rust

The implementation standard for OB (Ontoledgy/BORO) Rust codebases.
This guide overrides `rust-data-engineer` defaults where they conflict.
Rules not covered here fall back to `rust-data-engineer` standards.

Derived from the Python BORO Quick Style Guide (`boro-quick-style-guide.md`),
translating each principle to idiomatic Rust while preserving the same
design philosophy: precision, self-documentation, and strict separation of concerns.

Source: BORO/Ontoledgy Confluence space — BORO Clean Coding sections (pages 6495863472,
6495863609, 6495863620, 6495862997, 6495863571).

---

## Naming Conventions

| Symbol | BORO Standard | Rust / rust-data-eng default | Notes |
|--------|--------------|------------------------------|-------|
| Struct/enum names | PascalCase, **plural** | PascalCase, singular | `struct ObjectTypes {}` |
| Trait names | PascalCase, **plural or verb** | PascalCase | `trait Exportable {}` or `trait ObjectFormatters {}` |
| Module/file names | `snake_case`, **actor names** aligned with public function | `snake_case`, descriptive | `data_exporter.rs` → `pub fn export_data()` |
| Constant names | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` | Compatible |
| All other names | `snake_case` | `snake_case` | Compatible |
| Function names | **action verbs** | verbs recommended | `get_something()`, `export_data()` |
| Boolean functions | `is_` or `has_` prefix | `is_` recommended | **Mandatory in BORO** |
| Private functions | `fn` (no `pub`) — **module-private only** | `fn` or `pub(crate)` | BORO: never `pub(crate)` for internal helpers; visibility is `fn` (module-private) or `pub` (public API) |
| Forbidden names | `process`, `handle`, `data`, `item`, `tmp`, `res`, unclear abbreviations | — | **Strictly forbidden** |
| Forbidden single letters | All except `self` | Loop indices allowed | **BORO overrides** — no `i`, `j`, `k`, `n`, `x` |
| File rename rule | If public function renamed → file **must** be renamed | — | BORO-specific rule |

### Deeper Naming Principles

- Use intention-revealing names — precision over brevity
- Avoid disinformation — don't imply wrong meaning
- Make meaningful distinctions — adjacent things must be distinguishable
- Use pronounceable, searchable names
- Avoid encodings (no type prefixes, no Hungarian notation)
- Struct/enum names = plural nouns; avoid `Manager`, `Processor`, `Data`, `Info`
- Method names = verbs or verb phrases; accessors use `get_`/`set_`/`is_`
- No mental mapping, no slang, no culture-specific terms
- One word per concept — consistency across sibling methods and structs

---

## Code Layout

| Rule | BORO Standard | Rust default | Notes |
|------|--------------|-------------|-------|
| Line length | **20 chars** | 100 chars (rustfmt) | **BORO overrides** — intentional; enforced by discipline, not rustfmt |
| Between statements | One empty line | — | BORO-specific |
| After opening `{` | Do NOT leave next line empty | — | BORO-specific |
| Variable bindings | One `let` per line; never chain assignments | one per line | BORO-specific emphasis |
| Function arguments | Each argument on its own line | flexible | BORO-specific |
| Struct field args | Use struct construction for > 3 params; **name every field** at construction site | best practice | **Mandatory in BORO** — Rust has named fields by default; always use them |
| Type annotations | **Compiler-enforced** for function signatures; **add explicitly** on `let` bindings when type is not obvious from the right-hand side | inferred where possible | BORO adds explicit `let` annotation discipline |
| Return type | **Always specified** in function signature; `-> ()` if nothing returned (do not omit) | omit for `()` | **BORO overrides** — explicit `-> ()` |
| For loops | Iterator body on new line after `.for_each(\|item\|` or `for item in` on separate line from collection | — | BORO-specific |
| Impl block member sequence | constants → associated functions (constructors) → getters/setters → methods → trait impls | — | BORO-specific |
| Indentation | 4 spaces; no TABs | 4 spaces | Compatible |
| Related fields | No empty line between them; empty line between unrelated field groups | — | BORO-specific |

---

## Function Design

| Rule | BORO Standard |
|------|--------------|
| Return | Only one value (use a named struct if multiple values needed — no raw tuples in public APIs) |
| Responsibility | One thing only — strict separation of concerns |
| Decomposition | Break into sub-functions as much as possible |
| Too many arguments | Create a config/params struct to pass them (> 3 params) |
| Flag arguments | **Forbidden** — use enums with meaningful variant names |
| Private functions | Module-private `fn` — called only by the module's public function; never `pub(crate)` for internal helpers |
| Exposing behaviour | If external code needs it → promote to `pub fn` in the module's public API |
| Closures | Extract closures > 1 expression into named private functions |
| Method chains | Break chains > 3 links into named intermediate `let` bindings |

---

## File / Module Structure

| Rule | BORO Standard |
|------|--------------|
| Per-file rule | **One `pub fn` (entry point) + its private helper functions** |
| Exception | Facade modules may re-export multiple public items |
| Orchestrator pattern | When managing a sequence of stages → use `pub fn orchestrate_*()` |
| Orchestrator file name | `*_orchestrator.rs` |
| Orchestrator function name | `orchestrate_*()` |
| Nesting | Orchestrators can be nested |
| `mod.rs` / module directories | Use `module_name.rs` (not `module_name/mod.rs`) — Rust 2018+ edition style |
| Re-exports | Only in facade/lib.rs; explicit `pub use` (never `pub use crate::module::*`) |

---

## Type Design (Structs, Enums, Traits)

| Rule | BORO Standard |
|------|--------------|
| Struct names | **Plural** PascalCase (`ObjectTypes`, `TransactionRecords`) |
| Enum names | **Plural** PascalCase; variants are **singular** PascalCase (`enum OutputFormats { Csv, Json }`) |
| Trait names | PascalCase; verb/adjective forms preferred (`Exportable`, `Validatable`) |
| Instance methods | `&self` or `&mut self` — prefer `&self` (immutable borrow) |
| No `self` usage | Associated function (like Python's `@staticmethod`): `fn new()`, `fn from_*()` |
| Constructors | `fn new()` for primary; `fn from_*()` for conversions; `fn try_new()` / `fn try_from_*()` when fallible |
| Derive macros | `#[derive(Debug)]` **mandatory** on all types; add `Clone`, `PartialEq` only when semantically meaningful |
| Tuple structs | **Forbidden** in public APIs — use named fields for self-documentation |
| Raw tuples | **Forbidden** in function returns and public APIs — use named structs |
| Field visibility | Private by default; expose with getter methods, not `pub` fields |

---

## Constants and Strings

| Rule | BORO Standard |
|------|--------------|
| Hardcoded strings | **Never** — define as `const` or enum variants |
| Constants location | Separate `constants.rs` module |
| Enums | Separate module per domain enum |
| File/folder paths | Use `std::path::Path` / `PathBuf`; construct with `.join()` |
| String type | Use `&str` for borrowing, `String` for ownership; never `&String` in function params |
| Magic numbers | **Forbidden** — all numeric literals as named `const` values |

---

## Error Handling

| Rule | BORO Standard |
|------|--------------|
| Error types | **Domain-specific error enums** with `thiserror` — one error enum per module boundary |
| Generic errors | **Forbidden**: no `Box<dyn Error>`, no `anyhow::Error` in library/domain code (`anyhow` only in binary entry points) |
| `.unwrap()` | **Forbidden** in production code — use `?` operator |
| `.expect()` | Only when the invariant is **provably true**; message must document the invariant (e.g. `.expect("config validated at startup")`) |
| Error context | Every `?` propagation at a boundary must add context (`.map_err()` or `thiserror` `#[from]`) |
| Panic | **Forbidden** in library code — only in binary entry points or test code |
| `todo!()` / `unimplemented!()` | Allowed during development; **forbidden** in merged code |

---

## Ownership and Borrowing

These rules have no Python equivalent — they are Rust-specific BORO additions derived from
the same design philosophy (precision, no waste, explicit contracts).

| Rule | BORO Standard |
|------|--------------|
| Prefer borrowing | `&T` over `T` unless ownership transfer is semantically required |
| Clone discipline | **Never clone to satisfy the borrow checker** — restructure ownership instead; `Clone` only when the domain requires independent copies |
| Lifetime annotations | Explicit when not elidable; name them meaningfully (`'record`, `'config`, not `'a`, `'b`) |
| `Arc`/`Rc` | Only for genuine shared ownership (documented in a comment why shared); never as a convenience to avoid restructuring |
| `Box<dyn Trait>` | Only when runtime polymorphism is required (heterogeneous collections); prefer generics with trait bounds for static dispatch |
| `unsafe` | **Forbidden** unless architecturally approved and documented with `// SAFETY:` comment explaining the invariant |
| `Copy` types | Derive `Copy` only for small, semantically value-like types (IDs, flags, coordinates) |
| Interior mutability | `Cell`/`RefCell`/`Mutex` only when mutation through shared reference is architecturally necessary; document why |

---

## Imports / `use` Statements

| Rule | BORO Standard |
|------|--------------|
| Import style | **Explicit**: `use crate::module::TypeName;` |
| Glob imports | **Forbidden**: no `use crate::module::*;` (exception: test preludes in `#[cfg(test)]`) |
| Re-exports | Only in facade modules / `lib.rs`; explicit `pub use` |
| External crates | Group and separate from internal imports with an empty line |
| `use` ordering | `std` → external crates → `crate::` → `super::` → `self::` |
| Nested paths | Prefer flat imports over deeply nested `use` trees for readability |

---

## Comments

| Rule | BORO Standard |
|------|--------------|
| General comments | Code must not need comments — self-documenting names and structure |
| Doc comments (`///`) | **Mandatory** on every `pub` item — one sentence explaining *what*, not *how* |
| Internal comments | **Forbidden** except `// TODO` and `// SAFETY:` (for approved `unsafe`) |
| `//!` module docs | One sentence at the top of each module file stating the module's actor responsibility |

---

## Iterator and Loop Design

| Rule | BORO Standard |
|------|--------------|
| Prefer iterators | Use `.iter()` / `.into_iter()` chains over `for` loops where the chain reads naturally |
| Iterator body > 1 expression | Extract `.map()` / `.filter()` / `.for_each()` closure into a named private function |
| Nested iteration | Must NOT be visible — extract inner loop into a private function |
| `for` loop `in` clause | Collection expression on a new line if it doesn't fit on one line |
| `.collect()` | Always annotate the target type: `.collect::<Vec<_>>()` or bind to a typed `let` |
| Index access | **Forbidden** in iteration — use `.iter()`, `.enumerate()`, or `.windows()` |

---

## Concurrency (Rust-Specific BORO Addition)

| Rule | BORO Standard |
|------|--------------|
| Async runtime | `tokio` — do not mix runtimes |
| `async fn` | Same function design rules apply — one responsibility, decompose aggressively |
| Channels | Prefer typed channels (`tokio::sync::mpsc`) over shared mutable state |
| `Mutex`/`RwLock` | Only when channels don't fit; hold locks for the shortest possible scope; extract locked operations into a function |
| Spawned tasks | Each spawned task gets a named function — never inline large closures in `tokio::spawn()` |

---

## Best Practices

| Principle | Rule |
|-----------|------|
| YAGNI | Don't write code you don't need yet |
| DRY — Rule of Three | Third time you write the same code → extract to a helper |
| Fail Fast | Validate input at module boundaries; return `Err` on invalid state immediately |
| API Design | Simple things should be simple; complex things should be possible |
| Compiler as Ally | If the compiler can enforce an invariant (types, visibility, lifetimes), let it — don't add runtime checks for compile-time guarantees |
| Zero-Cost Abstractions | Prefer generics over trait objects; prefer stack over heap; prefer borrowing over cloning |

---

## Quality Gates

Run after every implementation:

```bash
cargo build                      # compilation
cargo clippy -- -D warnings      # lint — all warnings are errors
cargo fmt --check                # formatting (note: 20-char line limit is discipline, not rustfmt config)
cargo test                       # all tests pass
cargo doc --no-deps              # doc comments compile and link correctly
```

Note: `rustfmt`'s default `max_width` is 100 characters. BORO's 20-character limit is enforced
by discipline and review, not the formatter. Do not override `rustfmt`'s line-width setting —
the 20-char rule applies to logical statements, not tool configuration.

---

## Implementation Checklist

Use this checklist when implementing or reviewing OB Rust code.

### Naming
- [ ] Structs/enums: PascalCase, plural (`ObjectTypes`, `OutputFormats`)
- [ ] Enum variants: singular PascalCase (`OutputFormats::Csv`)
- [ ] Modules/files: snake_case, actor name matching public function
- [ ] Functions: action verbs (`get_`, `export_`, `orchestrate_`)
- [ ] Private functions: `fn` (no `pub`), module-private only
- [ ] Constants: `UPPER_SNAKE_CASE`
- [ ] Booleans: `is_` or `has_` prefix
- [ ] No vague names: no `data`, `tmp`, `process`, `handle`, `res`
- [ ] No single-letter names except `self`
- [ ] Lifetime names: meaningful words, not single letters (`'record`, not `'a`)

### Layout
- [ ] Lines: ≤ 20 characters (logical statements)
- [ ] Function args: each on its own line
- [ ] Explicit `-> ()` return type (never omitted)
- [ ] Explicit type annotations on `let` bindings where type is non-obvious
- [ ] Struct construction: name every field at construction site
- [ ] One empty line between statements
- [ ] No empty line after opening `{`

### Structure
- [ ] One `pub fn` per file (module)
- [ ] Orchestrators in `*_orchestrator.rs` files
- [ ] Private functions: only called by the module's public function
- [ ] No `pub(crate)` for internal helpers — use `fn` (module-private)
- [ ] Associated functions for constructors (`new`, `from_*`, `try_new`)
- [ ] Module style: `module_name.rs` (not `module_name/mod.rs`)

### Types
- [ ] `#[derive(Debug)]` on all types
- [ ] No tuple structs in public API — named fields only
- [ ] No raw tuples in function returns — named structs
- [ ] `Clone` only when domain semantics require it
- [ ] Private fields with getter methods (no `pub` fields)

### Constants and Strings
- [ ] No hardcoded strings — all in `const` or enum variants
- [ ] No magic numbers — named `const` values
- [ ] Paths use `Path` / `PathBuf` with `.join()`
- [ ] `&str` for borrowing, `String` for ownership; never `&String` in params

### Error Handling
- [ ] Domain error enums with `thiserror`
- [ ] No `Box<dyn Error>` in domain code
- [ ] No `.unwrap()` in production code
- [ ] `.expect()` only with documented invariant
- [ ] `?` with `.map_err()` context at boundaries
- [ ] No `panic!` in library code

### Ownership
- [ ] Borrow (`&T`) unless ownership transfer is required
- [ ] No cloning to satisfy borrow checker
- [ ] Meaningful lifetime names
- [ ] `unsafe` only with approval + `// SAFETY:` comment

### Imports
- [ ] Explicit `use` — no glob imports (except test preludes)
- [ ] Order: `std` → external → `crate` → `super` → `self`
- [ ] Re-exports only in facade / `lib.rs`

### Comments
- [ ] `///` doc comments on every `pub` item
- [ ] `//!` module doc at top of each file
- [ ] No internal comments except `// TODO` and `// SAFETY:`

### Iteration
- [ ] Iterators preferred over `for` loops
- [ ] Closure body > 1 expression → named function
- [ ] No visible nested iteration
- [ ] No index access in loops — use `.iter()` / `.enumerate()`
- [ ] `.collect()` always type-annotated
