# Clean Coding Skills — Development Plan

## Overview

This document proposes a modular set of Claude Code skills derived from the clean coding standards in `prompts/coding/standards/clean_coding/`. Each skill targets a specific concern so they can be used independently or composed together.

---

## Source Material

All skills are grounded in the existing standards:

| Document | Path |
|----------|------|
| Functions | `prompts/coding/standards/clean_coding/functions.md` |
| Classes | `prompts/coding/standards/clean_coding/classes.md` |
| Naming | `prompts/coding/standards/clean_coding/meaningful_names.md` |
| Error Handling | `prompts/coding/standards/clean_coding/error_handling.md` |
| Comments | `prompts/coding/standards/clean_coding/comments.md` |
| Formatting | `prompts/coding/standards/clean_coding/formatting.md` |
| Concurrency | `prompts/coding/standards/clean_coding/concurrency.md` |
| Objects & Data Structures | `prompts/coding/standards/clean_coding/objects_and_data_structures.md` |
| Boundaries | `prompts/coding/standards/clean_coding/boundaries.md` |
| Emergence | `prompts/coding/standards/clean_coding/emergence.md` |
| Smells & Heuristics | `prompts/coding/standards/clean_coding/smells_and_heuristics.md` |
| Summary | `prompts/coding/standards/clean_coding/clean_coding_standards.md` |
| Full Reference | `prompts/coding/standards/clean_coding/clean_coding_full_details.md` |
| Testing Guidelines | `prompts/coding/standards/testing/TESTING_GUIDELINES.md` |
| Test Quality Requirements | `prompts/coding/standards/testing/TEST_QUALITY_REQUIREMENTS.md` |
| Commit Standards | `prompts/coding/standards/cicd/commit_standards.md` |

---

## Skill Architecture

Five modular skills, each following the existing `skill.yaml` + `prompts/task.md` pattern used by `bie-data-engineer` and `bie-component-ontologist`.

```
ol_ai_context_library/skills/
├── clean-code-reviewer/       # Detect violations — produces a report
├── clean-code-refactor/       # Fix violations — rewrites code
├── clean-code-naming/         # Naming-focused — high daily-use value
├── clean-code-tests/          # Test generation and review
└── clean-code-commit/         # Commit message validation and generation
```

---

## Skill Definitions

### 1. `clean-code-reviewer`

**Purpose:** Analyse code and produce a structured violation report against clean coding standards.

**Modes:**

| Mode | Checks |
|------|--------|
| `full` | All standards combined (functions + classes + naming + errors + smells) |
| `functions` | Size (< 20 lines), argument count (0–3), abstraction level, side effects, flag arguments |
| `classes` | SRP, cohesion, coupling, size (< 200 lines), dependency direction |
| `naming` | Intent-revealing names, noun/verb conventions, searchability, no encoding |
| `errors` | Exception patterns, null returns, null parameters, context in exceptions |
| `smells` | Duplication, dead code, magic numbers, feature envy, large classes |

**Input schema:**
```yaml
required: [mode, target_path]
properties:
  mode: enum [full, functions, classes, naming, errors, smells]
  target_path: string   # file or directory to analyse
  severity_threshold: enum [low, medium, high]  # optional filter
```

**Output:** Structured report — violation list with location, rule, severity, and suggested fix.

**References:** All 13 clean coding documents.

---

### 2. `clean-code-refactor`

**Purpose:** Rewrite code to fix clean coding violations. Can act on reviewer output or work directly on a file.

**Modes:**

| Mode | What It Fixes |
|------|---------------|
| `functions` | Extract methods, reduce argument lists, remove flag args, separate concerns |
| `classes` | Split responsibilities, improve cohesion, apply SRP |
| `naming` | Rename symbols to reveal intent across a file or module |
| `errors` | Convert return codes to exceptions, remove null returns/params |
| `smells` | DRY violations, dead code removal, magic number extraction |

**Input schema:**
```yaml
required: [mode, target_path]
properties:
  mode: enum [functions, classes, naming, errors, smells]
  target_path: string
  violations_report: string   # optional — output from clean-code-reviewer
```

**Output:** Refactored file(s) with a change summary listing each modification and the rule applied.

**References:** Mode-scoped — only the standards relevant to the selected mode.

---

### 3. `clean-code-naming`

**Purpose:** Standalone naming skill. High daily-use value; naming is the most frequently violated standard.

**Modes:**

| Mode | Description |
|------|-------------|
| `review` | Audit all names in a file/module — flags violations with explanation |
| `fix` | Rename symbols to comply with standards, with before/after mapping |
| `suggest` | Given a function/class purpose description, return 3 candidate names |

**Input schema:**
```yaml
required: [mode]
properties:
  mode: enum [review, fix, suggest]
  target_path: string          # for review and fix modes
  purpose_description: string  # for suggest mode
  symbol_type: enum [function, class, variable, module]  # for suggest mode
```

**Output:** Violation list (review), renamed file (fix), or 3 ranked name suggestions with rationale (suggest).

**References:** `meaningful_names.md`

---

### 4. `clean-code-tests`

**Purpose:** Generate and review tests following the project testing standards.

**Modes:**

| Mode | Description |
|------|-------------|
| `generate` | Create unit tests for a class or function — covers happy path, error conditions, edge cases |
| `review` | Review existing tests against quality requirements (coverage scope, structure, naming, mocking) |
| `coverage-check` | Identify untested paths — happy path, error conditions, edge cases, input validation |

**Input schema:**
```yaml
required: [mode, target_path]
properties:
  mode: enum [generate, review, coverage-check]
  target_path: string
  test_category: enum [unit, integration]  # defaults to unit
```

**Output:** Test file (generate), annotated review report (review), or gap analysis with recommended test cases (coverage-check).

**References:** `TESTING_GUIDELINES.md`, `TEST_QUALITY_REQUIREMENTS.md`

---

### 5. `clean-code-commit`

**Purpose:** Validate or generate commit messages per the Conventional Commits specification.

**Modes:**

| Mode | Description |
|------|-------------|
| `validate` | Check a commit message against the standard — returns pass/fail with issues |
| `generate` | Generate a compliant commit message from a diff or change description |

**Input schema:**
```yaml
required: [mode]
properties:
  mode: enum [validate, generate]
  commit_message: string   # for validate mode
  diff_or_description: string  # for generate mode
  scope: string  # optional — component or module name
```

**Output:** Pass/fail with issues list (validate), or a formatted commit message with type, scope, and description (generate).

**References:** `cicd/commit_standards.md`

---

## File Structure Per Skill

Each skill follows the established pattern:

```
clean-code-reviewer/
├── skill.yaml               # Metadata, input/output schema, model config, execution limits
├── prompts/
│   └── task.md             # Jinja2 template with mode-conditional logic
└── references/
    ├── functions.md
    ├── classes.md
    ├── meaningful_names.md
    ├── error_handling.md
    └── smells_and_heuristics.md
```

> **References strategy (open question):** Copy the relevant standards files into each skill's `references/` directory, or reference the shared path in `prompts/coding/standards/`? Copying keeps skills self-contained but creates duplication. Shared paths reduce duplication but couple skills to the repo layout.

---

## Implementation Order

### Phase 1 — Core pair (highest ROI)

1. **`clean-code-reviewer`** — establishes the standard baseline, generates actionable output for all other skills
2. **`clean-code-refactor`** — acts on reviewer output; together these cover the full detect-and-fix loop

### Phase 2 — High-frequency standalone

3. **`clean-code-naming`** — daily use, self-contained, limited scope makes it easy to validate
4. **`clean-code-tests`** — critical for quality gates; ties into testing standards already documented

### Phase 3 — Workflow integration

5. **`clean-code-commit`** — narrow scope, CI/CD integration point; lower urgency than the others

---

## Open Questions

1. **Refactor output mode** — should `clean-code-refactor` write changes directly (`workspace-write`) or propose them as a diff for approval (`read-only`)?
2. **References strategy** — copy files into each skill's `references/` dir, or reference the shared `prompts/coding/standards/` path?
3. **Phase priority** — implement Phase 1 first (reviewer + refactor), or build all 5 in parallel?
4. **Commit skill scope** — `clean-code-commit` is narrow; include in Phase 3 or defer entirely?
