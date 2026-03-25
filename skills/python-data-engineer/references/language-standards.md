# Python Language Standards

---

## Naming

| Symbol | Convention | Notes |
|--------|-----------|-------|
| Functions / methods | `snake_case` verbs | `calculate_total()`, `load_records()` |
| Classes | `PascalCase` nouns | `TransactionProcessor`, `AccountRepository` |
| Variables | `snake_case` nouns | `transaction_count`, `source_file_path` |
| Constants (module-level) | `UPPER_SNAKE_CASE` | `MAX_BATCH_SIZE = 500` |
| Private (single `_`) | `_name` | Discourage external use; not enforced |
| Name-mangled (`__`) | `__name` | Rarely needed; use deliberately |
| Modules / packages | `snake_case` | `transaction_service.py`, `data_models/` |
| Type aliases | `PascalCase` | `RecordList = list[dict[str, Any]]` |

No abbreviations: `transaction` not `txn`, `dataframe` not `df`, `configuration` not `cfg`.

---

## Code Style (PEP 8 + project conventions)

- Line length: 88 characters (black/ruff default)
- Two blank lines between top-level definitions
- One blank line between methods in a class
- Imports: stdlib → third-party → local, alphabetical within groups
- No wildcard imports (`from x import *`)
- Prefer explicit relative imports within a package

---

## Type Annotations

Full annotations on all public functions and methods:

```python
from __future__ import annotations

def process_batch(
    records: list[dict[str, Any]],
    batch_size: int = 100,
) -> list[ProcessedRecord]:
    ...
```

- Use `list[T]`, `dict[K, V]`, `tuple[T, ...]` (Python 3.9+; no `from typing import List`)
- `T | None` instead of `Optional[T]` (Python 3.10+)
- `Protocol` for structural typing over `ABC` where possible
- `TypeVar` for generic functions
- `@dataclass(frozen=True)` for value objects

---

## Classes

- `@dataclass` or `@dataclass(frozen=True)` for data-holding classes
- `__slots__` for performance-sensitive, high-instance-count classes
- Override `__repr__` on classes that don't use `@dataclass`
- `__eq__` and `__hash__` must be consistent — if you define `__eq__`, define `__hash__`
- `Protocol` classes for interfaces (no abstract base class boilerplate needed)

---

## Functions

- Prefer `*` to enforce keyword-only arguments in public APIs:
  ```python
  def create_record(*, name: str, value: int) -> Record: ...
  ```
- Generator functions (`yield`) over building large lists when consumers iterate
- Context managers (`@contextmanager` or `__enter__`/`__exit__`) for resource lifecycle
- No mutable default arguments:
  ```python
  # Wrong
  def append(item, lst=[]):  # mutable default — shared across calls
  # Correct
  def append(item, lst=None):
      if lst is None: lst = []
  ```

---

## Error Handling

| Pattern | Use |
|---------|-----|
| `raise ValueError(msg)` | Invalid input / argument |
| `raise TypeError(msg)` | Wrong type |
| `raise RuntimeError(msg)` | Unexpected state |
| `raise FileNotFoundError(msg)` | Missing file |
| `raise X from Y` | Chaining exceptions (preserve original) |
| `except SpecificError` | Always specific; never bare `except:` |

- Never return `None` as an error signal; raise an exception
- Never catch-and-swallow: if you catch, log or re-raise
- Use `contextlib.suppress(ErrorType)` only when ignoring is intentional and documented

---

## Idiomatic Python

```python
# Comprehensions over loops for simple transforms
processed = [transform(r) for r in records if r.is_valid]

# Unpacking
first, *rest = items
name, value = record

# f-strings for interpolation
message = f"Processed {count} records from {source_path}"

# Walrus operator for assign-and-test
if chunk := file.read(4096):
    process(chunk)

# enumerate instead of manual index
for index, record in enumerate(records):
    ...

# zip for parallel iteration
for source, target in zip(sources, targets):
    ...
```
