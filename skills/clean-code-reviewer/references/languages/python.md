# Clean Code Reviewer — Python

Language-specific rules for applying clean coding standards to Python code.
Read alongside the general standards in `prompts/coding/standards/clean_coding/`.

---

## Naming Violations

| Violation | Example | Rule |
|-----------|---------|------|
| Abbreviation | `df`, `txn`, `cfg`, `acct` | Reveal intent: `transactions_dataframe`, `transaction`, `configuration` |
| Single-letter variable (outside loop index) | `x = load()`, `d = {}` | Name reveals purpose |
| Encoding in name | `str_name`, `list_items`, `b_flag` | No type encoding |
| Non-verb function | `def validation():` | Functions are verbs: `def validate_record():` |
| Non-noun class | `class DoProcessing:` | Classes are nouns: `class RecordProcessor:` |
| Screaming snake for non-constant | `PROCESSOR = Processor()` | `UPPER_SNAKE_CASE` for true module-level constants only |

---

## Function Violations

| Violation | Python-Specific Signal |
|-----------|----------------------|
| > 20 lines | Flag; check if multiple concerns present |
| > 3 parameters | Suggest `@dataclass` or `TypedDict` parameter object |
| Flag argument (`is_verbose`, `dry_run`) | Function does two things — split it |
| Mutable default argument | `def f(items=[])` — shared across calls, always a bug |
| `*args, **kwargs` in non-wrapper | Hides the real interface; make parameters explicit |
| Side effect in query function | `def get_count()` that also writes to DB |

---

## Class Violations

| Violation | Python-Specific Signal |
|-----------|----------------------|
| > 200 lines | Likely violating SRP; look for natural split points |
| `__init__` longer than 10 lines | Doing too much in construction; extract to factory |
| Methods that use no `self` fields | Should be a module-level function or `@staticmethod` |
| God class (30+ methods) | Decompose; look for clusters of methods that share fields |
| Mutable class-level attribute | `class Foo: items = []` — shared across instances |

---

## Error Handling Violations

| Violation | Example | Rule |
|-----------|---------|------|
| Bare `except:` | `except:` | Always name the exception |
| `except Exception:` without re-raise | Swallows unexpected errors | Log and re-raise or use specific type |
| Returning `None` as sentinel | `return None` on failure | Raise an exception; never signal failure with `None` |
| `None` passed as argument | `process(record=None)` | Validate at boundary; never propagate `None` into logic |
| Missing `raise X from Y` | `except E: raise NewError(...)` | Chain: `raise NewError(...) from e` |
| Catching then immediately passing | `except E: pass` | Either handle or re-raise |

---

## Smell Violations

| Smell | Python-Specific Signal |
|-------|----------------------|
| Magic number | `if count > 47:`, `time.sleep(0.3)` | Extract as named constant |
| Commented-out code | `# old_process(record)` | Delete; git history preserves it |
| `TODO` without owner/issue | `# TODO: fix this` | Must have owner or ticket reference |
| Duplicated logic | Same transform in 2+ places | Extract to shared function |
| Import inside function | `def f(): import pandas` | Move to module level unless circular import |
| Long list of positional args | `f(a, b, c, d, e)` | Use keyword arguments; introduce parameter object |

---

## Size Reference (Python)

| Unit | Max | Note |
|------|-----|------|
| Function / method body | 20 lines | Excluding signature and docstring |
| Class | 200 lines | Excluding docstrings and blank lines |
| Module | 500 lines | Soft limit; over this, look for natural splits |
| Parameters | 3 | More → introduce `@dataclass` parameter object |
