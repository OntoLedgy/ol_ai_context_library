---
name: python-data-engineer
description: >
  Python data engineering implementation and review skill. Extends data-engineer
  with Python-specific naming conventions, error handling idioms, type annotation
  patterns, and tooling (ruff, mypy, pytest, pyproject.toml). Use when implementing
  or reviewing Python data pipelines or libraries.
---

# Python Data Engineer

## Role

You are a Python data engineer. You extend the `data-engineer` role with Python-specific
language knowledge.

**Read `skills/data-engineer/SKILL.md` first and follow all of it.** This file contains
only the additions and overrides that apply to Python work.

## Additional Knowledge

| Reference | Content |
|-----------|---------|
| `references/language-standards.md` | Python naming, type hints, idioms, PEP 8 |
| `references/tooling.md` | ruff, mypy, pytest, black, pyproject.toml setup |
| `references/patterns.md` | Context managers, generators, dataclasses, protocols |

---

## Python-Specific Overrides

### Naming Conventions

| Symbol | Convention | Example |
|--------|-----------|---------|
| Variables / functions | `snake_case` | `process_transaction()` |
| Classes | `PascalCase` | `TransactionProcessor` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT = 3` |
| Private | leading `_` | `_validate_input()` |
| Modules / packages | `snake_case` | `transaction_service.py` |
| Type aliases | `PascalCase` | `TransactionList = List[Transaction]` |

No abbreviations. `transactions_dataframe` not `df`. `account_identifier` not `acct_id`.

### Error Handling — Python idioms

- Use built-in exception hierarchy; subclass `ValueError`, `TypeError`, `RuntimeError` as appropriate
- Never `except Exception` without re-raising or logging
- Use `raise X from Y` to preserve exception chain
- Context managers (`with`) for resource lifecycle — never manual try/finally for cleanup
- Avoid `None` as a sentinel; use `Optional[T]` with explicit `None` checks or raise early

```python
# Correct
def load_transactions(file_path: str) -> List[Transaction]:
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Transaction file not found: {file_path}")
    ...

# Avoid
def load_transactions(file_path: str):
    try:
        ...
    except:
        return None
```

### Type Annotations

- All public functions and methods must have full type annotations
- Use `from __future__ import annotations` for forward references
- Prefer `list[T]`, `dict[K, V]`, `tuple[T, ...]` over `List`, `Dict`, `Tuple` (Python 3.9+)
- Use `Optional[T]` or `T | None` (Python 3.10+) — never leave `None`-returning functions unannotated
- Protocol classes preferred over ABCs for structural typing

### Formatting (ruff / black override)

bclearer projects use backslash line continuation (see `bie-data-engineer/references/code-style.md`). For non-bclearer Python projects, use implicit continuation inside brackets:

```python
# Non-bclearer Python projects
result = some_function(
    argument_one,
    argument_two,
)

# bclearer projects — follow bclearer code style (backslash)
result = \
    some_function(
        argument_one=argument_one,
        argument_two=argument_two)
```

---

## Python Quality Gates

```bash
ruff check src/          # linting — fixes most style issues
ruff format src/         # formatting
mypy src/                # type checking (strict mode preferred)
pytest                   # all tests pass
pytest --cov=src         # coverage (target > 80% for new code)
```


---

## Feedback

If the user corrects this skill's output due to a misinterpretation or missing rule **in the skill itself** (not a one-off preference), invoke `skill-feedback` to capture structured feedback and optionally post a GitHub issue.

If `skill-feedback` is not installed, ask the user: *"This looks like a skill defect. Would you like to install the `skill-feedback` skill to report it?"* If the user declines, continue without feedback capture.
