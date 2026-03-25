# Clean Code Refactor — Python

Language-specific refactoring patterns for Python.
Read alongside the general `clean-code-refactor` SKILL.md.

---

## Naming Fixes

| Violation | Before | After |
|-----------|--------|-------|
| Abbreviation | `def proc_txn(df):` | `def process_transaction(transactions_dataframe):` |
| Non-verb function | `def validation(record):` | `def validate_record(record):` |
| Non-noun class | `class DoProcessing:` | `class RecordProcessor:` |
| Encoding | `str_name`, `list_items` | `name`, `items` |
| Single-letter | `x = load()` | `records = load()` |

---

## Function Extraction (Python)

```python
# Before — one function doing three things
def process_data(records, config, output_path):
    # validation block (lines 1-15)
    ...
    # transformation block (lines 16-35)
    ...
    # write block (lines 36-54)
    ...

# After — extract with type annotations
def process_data(
    records: list[Record],
    config: ProcessingConfig,
    output_path: str,
) -> None:
    validated = _validate_records(records)
    transformed = _transform_records(validated, config)
    _write_results(transformed, output_path)

def _validate_records(records: list[Record]) -> list[Record]:
    ...

def _transform_records(
    records: list[Record],
    config: ProcessingConfig,
) -> list[Record]:
    ...

def _write_results(records: list[Record], output_path: str) -> None:
    ...
```

Use `_` prefix for private helpers. Add type annotations to all extracted functions.

---

## Argument Reduction (Python)

```python
# Before — too many arguments
def create_record(name, amount, currency, source, timestamp, is_validated):
    ...

# After — introduce @dataclass parameter object
from dataclasses import dataclass

@dataclass(frozen=True)
class RecordCreationRequest:
    name: str
    amount: float
    currency: str
    source: str
    timestamp: datetime
    is_validated: bool

def create_record(request: RecordCreationRequest) -> Record:
    ...
```

---

## Flag Argument Removal (Python)

```python
# Before — flag argument means function does two things
def process(record, dry_run=False):
    if dry_run:
        validate_only(record)
    else:
        validate_and_save(record)

# After — two functions
def process_record(record: Record) -> None:
    validate_and_save(record)

def dry_run_record(record: Record) -> ValidationResult:
    return validate_only(record)
```

---

## Error Handling Fixes (Python)

```python
# Before — None sentinel
def find_record(record_id: str):
    result = db.query(record_id)
    if not result:
        return None   # caller must remember to check
    return result

# After — raise with context
def find_record(record_id: str) -> Record:
    result = db.query(record_id)
    if not result:
        raise RecordNotFoundError(
            f"Record not found: id={record_id!r}")
    return result

# Before — bare except
try:
    process(record)
except:
    pass

# After — specific exception with logging
try:
    process(record)
except ValidationError as error:
    logger.warning("Skipping invalid record %s: %s", record.id, error)
```

---

## Smell Fixes (Python)

```python
# Before — magic numbers
if retry_count > 3:
    time.sleep(0.5)

# After — named constants
MAX_RETRY_COUNT = 3
RETRY_DELAY_SECONDS = 0.5

if retry_count > MAX_RETRY_COUNT:
    time.sleep(RETRY_DELAY_SECONDS)

# Before — duplicated transform
# In module_a.py
processed = [r for r in records if r.amount > 0]
# In module_b.py
valid = [r for r in items if r.amount > 0]

# After — extract to shared function
# In shared/filters.py
def filter_positive_amount(records: list[Record]) -> list[Record]:
    return [record for record in records if record.amount > 0]
```

---

## Mutable Default Argument Fix

```python
# Before — shared mutable default
def append_record(record, collection=[]):
    collection.append(record)
    return collection

# After
def append_record(
    record: Record,
    collection: list[Record] | None = None,
) -> list[Record]:
    if collection is None:
        collection = []
    collection.append(record)
    return collection
```
