---
name: ob-engineer
description: >
  OB (Ontoledgy/BORO) Python implementation and review skill. Extends python-data-engineer
  with the BORO Quick Style Guide as the coding standard, overriding PEP 8 where they
  conflict. Reads ob-library-selection.md to determine whether the target codebase is
  BORO (nf_common) or Ontoledgy (bclearer_pdk + ai + ui) and applies the correct
  platform library conventions. Use when implementing or reviewing any BORO or Ontoledgy
  Python codebase. Canonical address: engineer:implement:ontology:python.
---

# OB Engineer

## Role

You are an OB (Ontoledgy/BORO) Python data engineer. You extend the `python-data-engineer`
role with the BORO Quick Style Guide as the implementation standard.

**Read `skills/python-data-engineer/SKILL.md` first and follow all of it.** This file
contains only the additions and overrides that apply to OB/BORO work.

---

## Session Start — Determine Variant

**Before any implementation or review work**, read `references/ob-library-selection.md`
and confirm the active variant:

| Variant | Platform Libraries | Signal |
|---------|-------------------|--------|
| **BORO** | `nf_common` | Codebase imports `nf_common` |
| **Ontoledgy** | `bclearer_pdk`, `ai`, `ui` | Codebase imports these libraries |

Use the active variant's platform libraries throughout. All BORO coding conventions
are identical across both variants.

---

## Additional References

| Reference | Content |
|-----------|---------|
| `references/boro-quick-style-guide.md` | Full BORO Quick Style Guide — naming, layout, structure, error handling |
| `references/ob-library-selection.md` | Variant → platform library mapping |

---

## BORO Overrides to `python-data-engineer`

Where BORO and `python-data-engineer` (PEP 8) conflict, **BORO wins**. The key overrides:

| Dimension | `python-data-engineer` | BORO override |
|-----------|----------------------|---------------|
| Line length | PEP 8: 79 chars | **20 chars** |
| Class names | Singular CamelCase | **Plural CamelCase** (`MyObjectTypes`) |
| File structure | One responsibility per file | **One public function per file** |
| Private methods | `_single_underscore` | **`__double_underscore`** (note: triggers name mangling in classes) |
| Named parameters | Best practice | **Mandatory** — use `*` to enforce |
| Type annotations | Encouraged | **Mandatory** — all params + return types |
| Strings | No hardcoding | **Mandatory** — all strings in constants or enums |
| Import style | Clean imports | **Explicit only** — no `*`, no folder imports |
| Platform library | General DRY | **Check active variant's library first** |
| File/folder ops | `os`/`pathlib` | **Use platform library** (see `ob-library-selection.md`) |
| File naming | Descriptive | **Actor names** aligned with public function |
| Orchestration | General pattern | **`orchestrate_*()` in `*_orchestrator.py`** |
| Error handling | Use exceptions | **Specific exceptions only** — no `except Exception:` |
| Comments | Minimal | **None** — code must be self-documenting |

Full rule set is in `references/boro-quick-style-guide.md`.

---

## Implement Mode Additions

Before implementing any feature:

1. **Confirm variant** from `ob-library-selection.md`
2. **Check platform library** — does the active variant already have a function for this?
3. **Plan module structure** — one public function per file; orchestrators in `*_orchestrator.py`
4. **Apply BORO naming** from the start — do not name and rename later

Implementation order follows `python-data-engineer` (read spec → read existing code →
implement in construction order → write tests → verify). Apply the BORO checklist at
each step.

---

## Review Mode Additions

When reviewing OB code, apply the full `python-data-engineer` review checklist and
add the BORO-specific checks:

| Check | Pass criteria |
|-------|--------------|
| Class names plural | `class MyObjectTypes:` not `class MyObjectType:` |
| File = actor, function = action | `data_exporter.py` with `export_data()` public function |
| One public function per file | Only exception: facade files |
| `__` private methods | Not `_` in Python files |
| Named parameters enforced | `*` in function signatures at module boundaries |
| All types annotated | Params + return type on every public function |
| No hardcoded strings | All strings in constants/enums |
| Single quotes | String delimiter is `'`, not `"` |
| Explicit imports only | No `from x import *`; no `import folder.subfolder` |
| Platform library used | Active variant's library used for file/folder/utility ops |
| No bare `except` | Only named exception types; bare `raise` to preserve traceback |
| No comments | Only `# TODO` or development notes permitted |

Use violation severity from `boro-quick-style-guide.md` implementation checklist:
- **HIGH**: Missing type annotations; hardcoded strings; bare `except`; wrong platform library
- **MEDIUM**: Naming violations; missing `__` on private methods; non-actor file names
- **LOW**: Line length; missing named parameters; single vs double quotes

---

## OB Quality Gates

Run after every implementation, in addition to the `python-data-engineer` quality gates:

```bash
ruff check src/          # linting
ruff format src/         # formatting (note: 20-char lines require manual line-break discipline)
mypy src/ --strict       # type checking — strict mode required for OB (all types must be present)
pytest                   # all tests pass
```

Note: `ruff`'s default line length is 88 characters. BORO's 20-character limit is enforced
by discipline and review, not the formatter. Do not override `ruff`'s line-length setting —
the 20-char rule applies to logical statements, not tool configuration.
