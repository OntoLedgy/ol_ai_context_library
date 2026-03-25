# Python Patterns

Key Python-idiomatic patterns for data engineering work.

---

## Context Managers — resource lifecycle

Use `with` for anything that needs cleanup (files, DB connections, locks).

```python
# File I/O
with open(file_path, encoding="utf-8") as f:
    records = json.load(f)

# Custom context manager via decorator
from contextlib import contextmanager

@contextmanager
def database_connection(url: str):
    conn = create_connection(url)
    try:
        yield conn
    finally:
        conn.close()
```

Implement `__enter__`/`__exit__` on classes that manage resources.

---

## Dataclasses — value objects

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)   # immutable value object
class TransactionRecord:
    transaction_id: str
    amount: float
    currency: str

@dataclass
class PipelineConfig:
    source_path: str
    batch_size: int = 100
    tags: list[str] = field(default_factory=list)
```

Use `frozen=True` for value objects that should not change after creation.

---

## Protocols — structural interfaces

```python
from typing import Protocol

class RecordReader(Protocol):
    def read(self) -> list[dict[str, Any]]: ...

class RecordWriter(Protocol):
    def write(self, records: list[dict[str, Any]]) -> None: ...
```

Functions that depend on these accept any object implementing the protocol — no explicit inheritance required.

---

## Generators — lazy sequences

```python
def read_in_batches(
    file_path: str,
    batch_size: int,
) -> Generator[list[str], None, None]:
    with open(file_path) as f:
        batch = []
        for line in f:
            batch.append(line.strip())
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
```

Prefer generators over loading entire datasets into memory for large files.

---

## Result Pattern (no external library)

Python uses exceptions rather than `Result[T, E]`, but explicit error states can be modelled with a typed union when callers must handle both paths:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Success[T]:
    value: T

@dataclass(frozen=True)
class Failure:
    error: str
    detail: str

ProcessResult = Success[ProcessedRecord] | Failure
```

Use sparingly — standard exceptions are preferred for most error handling.

---

## Dependency Injection — constructor injection

```python
class TransactionProcessor:
    def __init__(
        self,
        reader: RecordReader,
        writer: RecordWriter,
    ) -> None:
        self._reader = reader
        self._writer = writer

    def process(self) -> None:
        records = self._reader.read()
        ...
        self._writer.write(results)
```

Inject dependencies via constructor. Never instantiate collaborators inside a class — that makes the class untestable.

---

## Functional Patterns

```python
from functools import reduce
from itertools import islice, chain, groupby

# Map / filter with type safety
totals: list[float] = list(map(lambda r: r.amount, valid_records))
valid = list(filter(lambda r: r.amount > 0, records))

# Prefer comprehensions for readability
totals = [r.amount for r in valid_records]
valid = [r for r in records if r.amount > 0]

# Group by key
from itertools import groupby
sorted_records = sorted(records, key=lambda r: r.category)
for category, group in groupby(sorted_records, key=lambda r: r.category):
    process_group(category, list(group))
```
