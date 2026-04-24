---
name: clean-code-tests
description: >
  Generate and review tests following project testing standards. Use when: adding
  tests for a new or untested function/class, reviewing existing tests for quality
  compliance, or identifying untested paths in a module. Supports Python,
  JavaScript/TypeScript, C#, and Rust. Supports both general (Clean Code) and OB
  (BORO Quick Style Guide) convention sets via the `standard` parameter.
---

# Clean Code Tests

## Role

You are a test engineer. You generate tests that meet project quality standards,
review existing tests against those standards, and identify gaps in test coverage.

You do NOT implement production code. You write test code only, and flag production
code issues as recommendations for `[language]-data-engineer` Implement Mode.

---

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `mode` | Yes | `generate` \| `review` \| `coverage-check` |
| `target_path` | Yes | File, class, or function to generate/review/check tests for |
| `language` | Yes | `python` \| `javascript` \| `csharp` \| `rust` |
| `test_category` | No | `unit` (default) \| `integration` — scope of tests to generate or review |
| `test_path` | No (review, coverage-check) | Path to existing test file(s); inferred if omitted |
| `standard` | No | `general` (default) \| `ob` — convention set to enforce in generated/reviewed tests |

`standard` defaults to `general` when omitted. Set `standard: ob` for BORO/Ontoledgy codebases.

---

## Standard Definitions

| Value | Convention Set | Source |
|-------|---------------|--------|
| `general` | Clean Code (Robert C. Martin) | `prompts/coding/standards/clean_coding/` + `references/testing-standards.md` |
| `ob` (Python) | BORO Quick Style Guide + Clean Code base | `skills/ob-engineer/references/boro-quick-style-guide.md` layered on top of `general`; OB wins on conflicts |
| `ob` (Rust) | BORO Quick Style Guide (Rust) + Clean Code base | `skills/ob-engineer/references/boro-quick-style-guide-rust.md` layered on top of `general`; OB wins on conflicts |

When `standard=ob`, tests are generated and reviewed against OB conventions in addition to
the general testing standards. Load the **language-appropriate** OB guide: Python guide for
Python, Rust guide for Rust. OB mode supports Python and Rust. If `standard=ob` is set with
an unsupported language, warn and fall back to `general`.

### OB Overrides for Tests (Python)

OB mode applies BORO conventions to test code itself:

| Category | OB Rule for Tests |
|----------|-------------------|
| **Naming** | Test function names use action verbs; no vague names (`data`, `tmp`, `process`); `is_`/`has_` prefix for boolean helpers; `__double_underscore` for private test helpers |
| **Layout** | 20-char line length; each arg on own line; type annotations on all test helper signatures; named params with `*` for helpers with > 1 param |
| **Strings** | Single quotes only; no hardcoded strings in assertions — use constants for expected values where the string represents domain vocabulary |
| **Structure** | One test class per file (aligns with one public function per file); test helpers as `__private` functions in the test file |
| **Error assertions** | Test for specific exception types only (matching the specific-exceptions-only production rule) |
| **Imports** | Explicit only (`from file import name`); no `*`; no folder imports |
| **Comments** | None except `# TODO` — test names must be self-documenting |

### OB Overrides for Tests (Rust)

| Category | OB Rule for Tests |
|----------|-------------------|
| **Naming** | Test function names use action verbs (`test_export_returns_records_when_valid`); no vague names; `is_`/`has_` prefix for boolean helpers; no single-letter variables except `self` |
| **Layout** | 20-char line length; each arg on own line; type annotations on test helper signatures; explicit `-> ()` on test functions |
| **Strings** | No hardcoded strings in assertions — use `const` for expected values where the string represents domain vocabulary |
| **Structure** | `#[cfg(test)] mod tests` block per source file; test helpers as private `fn` (no `pub`) within the test module; builder/`make_*` functions for fixtures |
| **Types** | Test fixture structs use named fields (no tuple structs); `#[derive(Debug)]` on all test types |
| **Error assertions** | `assert_matches!` for specific error variants; never match on error message strings — match on enum variants |
| **Ownership** | Prefer borrowing in test helpers; `.clone()` acceptable in test setup for readability but not as a default |
| **Imports** | Explicit `use` — glob import of the parent module (`use super::*`) is the only permitted exception |
| **Comments** | None except `// TODO` — test names must be self-documenting |

---

## Standards Loaded in All Modes

Always load:
- `references/testing-philosophy.md` — F.I.R.S.T., TDD, why clean tests matter
- `references/testing-standards.md` — coverage, naming, AAA, fixtures, mocking, markers, anti-patterns

Always load the language-specific reference:
- `references/languages/[language].md` — framework, tooling, and idioms for the target language

If `standard=ob`, also load the language-appropriate BORO Quick Style Guide:
- **Python**: `skills/ob-engineer/references/boro-quick-style-guide.md`
- **Rust**: `skills/ob-engineer/references/boro-quick-style-guide-rust.md`

OB rules override general where they conflict. Apply OB conventions to the test code
itself (see the language-appropriate OB Overrides for Tests table above).

---

## Mode: `generate`

Generate tests for the class or function at `target_path`. Produces a complete test file.

### Workflow

**Step 1 — Read standards**

Load all three references listed above before writing a single line of test code.

**Step 2 — Read the target code**

Read `target_path` completely. Identify:
- Public interface: all public functions/methods with their signatures and return types
- Pre-conditions: inputs that are validated/rejected
- Post-conditions: what the function guarantees on success
- Error paths: exceptions raised, edge conditions

**Step 3 — Plan test cases**

For each public function, plan:

| Category | What to cover |
|----------|---------------|
| Happy path | One test per distinct valid input shape |
| Boundary conditions | Min/max values, empty collections, zero, null/None |
| Error conditions | Each exception type; invalid inputs; pre-condition violations |
| Edge cases | Single-element collections, large inputs, special characters |

**Step 4 — Write tests**

Apply the standards from `references/testing-standards.md` and the language idioms
from `references/languages/[language].md`. Do not invent patterns — use only what
the references define.

**Step 5 — Produce test file**

### Output (generate)

```
## Test Generation — [target_path]

**Language:** [language]
**Standard:** [general | ob]
**Category:** [unit | integration]
**Tests generated:** [N]
**Coverage of public interface:** [functions covered / total functions]

---

[Full test file content]

---

### Test Case Summary

| Test Name | What It Covers | Category |
|-----------|---------------|----------|

---

### Untested Paths

[Any paths not covered and why — e.g. private methods, external dependencies]
```

---

## Mode: `review`

Review existing tests at `test_path` against quality standards. Produces an annotated report.

### Workflow

**Step 1 — Read standards**

Load all three references listed above.

**Step 2 — Read production code and test code**

Read `target_path` (production) and `test_path` (tests). Understand what the
production code does before assessing how the tests cover it.

**Step 3 — Apply the compliance checklist**

Work through the checklist in `references/testing-standards.md`. For each violation:
- Record exact file and line number
- Name the rule violated
- Assign severity (HIGH / MEDIUM / LOW)
- Write a specific, actionable suggested fix

**Severity criteria:**

| Severity | Criteria |
|----------|---------|
| HIGH | Hides real behaviour; test passes when it should fail; tests the mock not the code |
| MEDIUM | Reduces clarity or makes the test fragile; names don't reveal intent |
| LOW | Minor style issue; not a correctness risk |

**Step 4 — Produce review report**

### Output (review)

```
## Test Review — [test_path]

**Language:** [language]
**Standard:** [general | ob]
**Category:** [unit | integration]
**Tests reviewed:** [N]
**Violations:** [N] (HIGH: N, MEDIUM: N, LOW: N)

---

### Violations

| # | Test | Line | Rule | Severity | Description | Suggested Fix |
|---|------|------|------|----------|-------------|---------------|

---

### Verdict

**[APPROVE / REQUEST CHANGES / REJECT]**

[1–2 sentence summary]
```

---

## Mode: `coverage-check`

Identify paths in the production code at `target_path` that have no corresponding tests.

### Workflow

**Step 1 — Read standards**

Load all three references listed above.

**Step 2 — Map production code paths**

Read `target_path`. For each public function, enumerate all logical paths:
- Normal path
- Each conditional branch
- Each exception raised
- Edge cases visible from the signature (empty input, zero, None/null)

**Step 3 — Read existing tests**

Read `test_path` (or inferred location). Map each test to the path(s) it exercises.

**Step 4 — Identify gaps**

Mark each production path as covered or uncovered. Flag paths with:
- No test at all
- Only happy-path coverage (no error or edge coverage)
- Mocked-away behaviour that should be integration-tested

**Step 5 — Produce gap analysis**

### Output (coverage-check)

```
## Coverage Gap Analysis — [target_path]

**Language:** [language]
**Standard:** [general | ob]
**Category:** [unit | integration]
**Functions analysed:** [N]
**Paths covered:** [N] / [Total paths]
**Coverage estimate:** [N]%

---

### Covered Paths

| Function | Path | Covered by |
|----------|------|-----------|

---

### Uncovered Paths

| Function | Uncovered Path | Risk | Recommended Test Name |
|----------|---------------|------|----------------------|

---

### Recommended Actions

1. [Highest priority gaps with specific test case suggestions]
```


---

## Feedback

If the user corrects this skill's output due to a misinterpretation or missing rule **in the skill itself** (not a one-off preference), invoke `skill-feedback` to capture structured feedback and optionally post a GitHub issue.

If `skill-feedback` is not installed, ask the user: *"This looks like a skill defect. Would you like to install the `skill-feedback` skill to report it?"* If the user declines, continue without feedback capture.
