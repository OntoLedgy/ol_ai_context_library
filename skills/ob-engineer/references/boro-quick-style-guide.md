# BORO Quick Style Guide

The implementation standard for OB (Ontoledgy/BORO) Python codebases.
This guide overrides PEP 8 and `python-data-engineer` defaults where they conflict.
Rules not covered here fall back to `python-data-engineer` standards.

Source: BORO/Ontoledgy Confluence space — BORO Clean Coding sections (pages 6495863472,
6495863609, 6495863620, 6495862997, 6495863571).

---

## Naming Conventions

| Symbol | BORO Standard | PEP 8 / py-data-eng default | Notes |
|--------|--------------|----------------------------|-------|
| Class names | CamelCase, **plural** | CamelCase, singular | `class MyObjectTypes:` |
| Class file names | `snake_case` | `snake_case` | Compatible |
| Constant names | `CAPITAL_CASE` | `UPPER_SNAKE_CASE` | Compatible |
| All other names | `snake_case` | `snake_case` | Compatible |
| Function names | **action verbs** | verbs recommended | `get_something()`, `export_data()` |
| File names | **actor names** aligned with public function | descriptive | `data_exporter.py` → `export_data()` |
| Boolean functions | `is_` or `has_` prefix | `is_` recommended | Mandatory in BORO |
| Private methods | **`__double_underscore`** | `_single_underscore` | **BORO overrides PEP 8** |
| String delimiter | **single quotes only** | either | `'example string'` |
| Forbidden names | `process`, `handle`, `data`, `item`, `tmp`, `res`, unclear abbreviations | — | **Strictly forbidden** |
| Forbidden single letters | All except `self`, `cls` | Loop indices allowed | **BORO overrides** |
| File rename rule | If public function renamed → file **must** be renamed | — | BORO-specific rule |

### Deeper Naming Principles

- Use intention-revealing names — precision over brevity
- Avoid disinformation — don't imply wrong meaning
- Make meaningful distinctions — adjacent things must be distinguishable
- Use pronounceable, searchable names
- Avoid encodings (no type prefixes)
- Class names = plural nouns; avoid `Manager`, `Processor`, `Data`, `Info`
- Method names = verbs or verb phrases; accessors use `get_`/`set_`/`is_`
- No mental mapping, no slang, no culture-specific terms
- One word per concept — consistency across sibling methods and classes

---

## Code Layout

| Rule | BORO Standard | PEP 8 default | Notes |
|------|--------------|---------------|-------|
| Line length | **20 chars** | 79 chars | **BORO overrides PEP 8** — intentional |
| Between instructions | One empty line | — | BORO-specific |
| After colon `:` (function/loop) | Do NOT leave next line empty | — | BORO-specific |
| Variable assignments | Always on new line after backslash `\` | implicit continuation | BORO uses backslash |
| Function arguments | Each argument on its own line; no spaces around `=` in calls | flexible | BORO-specific |
| Named parameters | **Always specify argument name at call site**; use `*` to enforce | best practice | **Mandatory in BORO** |
| Type annotations | **Always specify** all parameter types | encouraged | **Mandatory in BORO** |
| Return type | **Always specified**, on new line before colon; `-> None` if nothing returned | encouraged | **Mandatory in BORO** |
| For loops | `in` block goes on a new line | — | BORO-specific |
| Class member sequence | constants → static attrs → object attrs → inner classes → getters/setters → methods | — | BORO-specific |
| Indentation | 4 spaces; no TABs | 4 spaces | Compatible |
| Related attributes | No empty line between them; empty line between all other members | — | BORO-specific |

---

## Function Design

| Rule | BORO Standard |
|------|--------------|
| Return | Only one item |
| Responsibility | One thing only — strict separation of concerns |
| Decomposition | Break into sub-functions as much as possible |
| Too many arguments | Create a class to pass them |
| Flag arguments | **Forbidden** |
| Private functions | Called only by the file's public function; never called externally |
| Exposing behaviour | If external code needs it → expose as a public method |

---

## File / Module Structure

| Rule | BORO Standard |
|------|--------------|
| Per-file rule | **One public (entry point) function + its private subfunctions** |
| Exception | Facade/suite files may have multiple related public functions |
| Orchestrator pattern | When managing a sequence of processes → use `orchestrate_*()` function |
| Orchestrator file name | `[name]_orchestrator.py` |
| Orchestrator function name | `orchestrate_[name]()` |
| Nesting | Orchestrators can be nested |

---

## Class Design

| Rule | BORO Standard |
|------|--------------|
| Instance methods | Use `self` |
| No `self`/`cls` usage | Declare as `@staticmethod` |
| Class-level methods | Use `@classmethod` (e.g. `bie_identity_type(cls)`) |

---

## Constants and Strings

| Rule | BORO Standard |
|------|--------------|
| Hardcoded strings | **Never** — define as constants or enums |
| Constants location | Separate file(s) |
| Enums | Separate class |
| File/folder paths | Use `os.path.join()` and `os.sep`; use `Path()` constructor |

---

## Error Handling

| Rule | BORO Standard |
|------|--------------|
| Catch specificity | **Only specific exceptions** — never bare `except:` or `except Exception:` |
| Traceback preservation | Use bare `raise` inside `except` |
| Unimplemented | `raise NotImplementedError` is allowed |

---

## Library Usage

Always read `ob-library-selection.md` first to confirm the correct platform libraries
for the current codebase variant.

| Rule | BORO variant | Ontoledgy variant |
|------|-------------|-------------------|
| File/folder operations | `nf_common` `Files` and `Folders` | `bclearer_pdk` equivalents |
| General utilities | Check `nf_common` first | Check `bclearer_pdk`, `ai`, `ui` first |

The following rules apply to **both** variants:

| Rule | Standard |
|------|---------|
| Import style | **Explicit only**: `from file import class/method/constant` |
| Wildcard imports | **Forbidden**: `from x import *` |
| Folder imports | **Forbidden**: `import folder_a.folder_b` |

---

## Comments

| Rule | BORO Standard |
|------|--------------|
| General comments | Clean code must not need comments |
| Code self-documentation | Code should be clear and self-explanatory |
| Allowed comments | Development purposes only: `# TODO`, development notes |

---

## Loop Design

| Rule | BORO Standard |
|------|--------------|
| Loop body > 1 statement | Extract all loop content into a private function |
| Nested loops | Must NOT be visible — group into private functions |
| `for` loop `in` clause | Goes on a new line |

---

## Best Practices

| Principle | Rule |
|-----------|------|
| YAGNI | Don't write code you don't need yet |
| DRY — Rule of Three | Third time you write the same code → extract to a helper |
| Fail Fast | Validate input; fail on invalid state as early as possible |
| API Design | Simple things should be simple; complex things should be possible |

---

## Implementation Checklist

Use this checklist when implementing or reviewing OB code.

### Naming
- [ ] Classes: CamelCase, plural
- [ ] Files: snake_case, actor name matching public function
- [ ] Functions: action verbs (`get_`, `export_`, `import_`, `orchestrate_`)
- [ ] Private functions: `__double_underscore`
- [ ] Constants: `CAPITAL_CASE`
- [ ] Booleans: `is_` or `has_` prefix
- [ ] No vague names: no `data`, `tmp`, `process`, `handle`, `res`

### Layout
- [ ] Lines: ≤ 20 characters
- [ ] Function args: each on its own line
- [ ] Type annotations: all parameters declared
- [ ] Named parameters: enforced with `*`
- [ ] Return type: declared on new line before `:`
- [ ] Variable assignments: new line after `\`
- [ ] For loops: `in` block on new line
- [ ] One empty line between instructions

### Structure
- [ ] One public function per file
- [ ] Orchestrators in `*_orchestrator.py` files
- [ ] Private functions: only called by the file's public function
- [ ] `@staticmethod` where no `self`/`cls` needed
- [ ] `@classmethod` for class-level identity methods

### Strings and Constants
- [ ] No hardcoded strings — all in constants/enums
- [ ] Paths use `os.path.join()` + `os.sep` or `Path()`
- [ ] String delimiter: single quotes

### Error Handling
- [ ] Specific exceptions only — named exception types
- [ ] Bare `raise` to preserve traceback
- [ ] No `except:` or `except Exception:`

### Libraries
- [ ] Active variant's platform library checked before writing general functions
- [ ] Imports: `from file import name` only
- [ ] No `from x import *`
- [ ] No folder-level imports

### Comments
- [ ] No comments unless `# TODO` / development note
