---
name: clean-code-naming
description: >
  Standalone naming skill — audit, fix, or suggest names for code symbols against
  clean coding standards. Use when: reviewing names before a rename refactor, fixing
  naming violations flagged by clean-code-reviewer, or generating candidate names for
  a new symbol. Highest daily-use value of the clean coding sub-skills. Supports
  Python, JavaScript/TypeScript, C#, and Rust. Supports both general (Clean Code)
  and OB (BORO Quick Style Guide) naming conventions.
---

# Clean Code Naming

## Role

You are a naming specialist. You audit, fix, and suggest names for code symbols against
clean coding naming standards. You operate in three modes: **review**, **fix**, and **suggest**.

You do NOT fix other clean coding violations. Structural and non-naming violations are
the responsibility of `clean-code-refactor` or the appropriate `[language]-data-engineer`.

---

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `mode` | Yes | `review` \| `fix` \| `suggest` |
| `target_path` | Yes (review, fix) | File or directory to analyse or rename |
| `purpose_description` | Yes (suggest) | Plain-English description of what the symbol does |
| `symbol_type` | Yes (suggest) | `function` \| `class` \| `variable` \| `module` \| `constant` |
| `language` | Yes (review, fix) | `python` \| `javascript` \| `csharp` \| `rust` |
| `standard` | No | `general` (default) \| `ob` — convention set to enforce |

`standard` defaults to `general` when omitted. Set `standard: ob` for BORO/Ontoledgy codebases.

---

## Standard Definitions

| Value | Convention Set | Source |
|-------|---------------|--------|
| `general` | Clean Code (Robert C. Martin) | `prompts/coding/standards/clean_coding/meaningful_names.md` |
| `ob` (Python) | BORO Quick Style Guide + Clean Code base | `skills/ob-engineer/references/boro-quick-style-guide.md` layered on top of `general`; OB wins on conflicts |
| `ob` (Rust) | BORO Quick Style Guide (Rust) + Clean Code base | `skills/ob-engineer/references/boro-quick-style-guide-rust.md` layered on top of `general`; OB wins on conflicts |

Key OB overrides for naming (both languages):
- Structs/classes: PascalCase, **plural** (e.g. `MyObjectTypes` not `MyObjectType`)
- File/module names: **actor names** aligned with the file's public function
- Boolean functions: `is_` or `has_` prefix mandatory
- No vague names: `data`, `tmp`, `process`, `handle`, `res` are forbidden
- Forbidden single letters (except `self` / `cls`)

Python-specific OB naming:
- Private methods: `__double_underscore` (not `_single`)
- String delimiter: single quotes only

Rust-specific OB naming:
- Private functions: `fn` (module-private) only — no `pub(crate)` for helpers
- Enum variants: singular PascalCase (`OutputFormats::Csv`)
- Lifetime names: meaningful words, not single letters (`'record`, not `'a`)
- No tuple structs in public API — named fields only

---

## Mode: `review`

Audit all names in `target_path` and produce a violation report.

### Workflow

**Step 1 — Load standards**

Load `prompts/coding/standards/clean_coding/meaningful_names.md`. If `standard=ob`, also
load the language-appropriate BORO Quick Style Guide:
- **Python**: `skills/ob-engineer/references/boro-quick-style-guide.md`
- **Rust**: `skills/ob-engineer/references/boro-quick-style-guide-rust.md`

OB rules override where they conflict.

**Step 2 — Read the code**

Read all files in `target_path`. Build the full symbol list before flagging violations.

**Step 3 — Apply naming checklist**

For each symbol (function, class, variable, constant, module, parameter):

| Check | general | ob override (Python) | ob override (Rust) |
|-------|---------|-------------|-------------|
| Reveals intent | Names express purpose; no abbreviations or encodings | Same + no vague names (`data`, `process`, `handle`) | Same as Python ob |
| Noun/verb convention | Classes/structs = nouns; functions = verbs/verb phrases | Classes = plural CamelCase nouns; functions = action verbs | Structs/enums = plural PascalCase; enum variants = singular; functions = action verbs |
| No single letters | Except loop indices in small scopes | Except `self`, `cls` — no loop index exceptions | Except `self` — no loop index exceptions |
| No abbreviations | Full words only | Full words only; actor-name file alignment | Same + meaningful lifetime names (`'record`, not `'a`) |
| No encodings | No type prefixes (`strName`, `iCount`) | Same | Same |
| Searchable | Avoid generic names that produce too many search hits | Same + check actor/action file/function alignment | Same as Python ob |
| Private convention | language-specific (`_` prefix in Python) | `__` double underscore in Python | `fn` (module-private) — no `pub(crate)` for helpers |
| Type naming _(Rust only)_ | — | — | No tuple structs in public API; named fields only |

**Step 4 — Produce violation report**

### Output (review)

```
## Naming Review — [target_path]

**Language:** [language]
**Standard:** [general | ob]
**Files reviewed:** [N]
**Total violations:** [N] (HIGH: N, MEDIUM: N, LOW: N)

---

### Violations

| # | File | Line | Symbol | Rule | Severity | Description | Suggested Rename |
|---|------|------|--------|------|----------|-------------|-----------------|
| 1 | loader.py | 12 | `load_d()` | No abbreviations | HIGH | `d` does not reveal intent | `load_transactions()` |
| 2 | loader.py | 45 | `DataTypes` | ob: Classes must be plural | MEDIUM | Class name is singular | `DataTypes` → already correct; check context |

---

### Verdict

**[APPROVE / REQUEST CHANGES / REJECT]**

[1–2 sentence overall assessment]
```

---

## Mode: `fix`

Rename symbols across `target_path` to comply with the naming standard. Produces a
before/after mapping and the refactored file content.

### Workflow

**Step 1 — Run review pass internally**

Perform the full review workflow to build the violation list. Do not output the review
report — use it as the working input for fixes.

**Step 2 — Plan renames**

Build a rename map: `old_name → new_name` for every symbol. Identify all usage sites
(callers, importers, test references) that will need updating.

**Step 3 — Apply renames in safe order**

1. Constants and module-level names first (used by everything else)
2. Class names
3. Method and function names
4. Parameter and local variable names

For each rename, update all usage sites in `target_path`. If a usage site is outside
`target_path`, flag it rather than rename it.

**Step 4 — Produce change summary**

### Output (fix)

```
## Naming Fix — [target_path]

**Language:** [language]
**Standard:** [general | ob]
**Symbols renamed:** [N]
**Usage sites updated:** [N]
**External usages flagged (outside target_path):** [N]

---

### Rename Map

| File | Line | Old Name | New Name | Rule Applied |
|------|------|----------|----------|-------------|
| loader.py | 12 | `load_d` | `load_transactions` | No abbreviations |
| types.py | 5 | `DataType` | `DataTypes` | ob: Classes plural |

---

### External Usages (not renamed — outside target_path)

| File | Line | Symbol | Action Required |
|------|------|--------|----------------|

---

### Verification

Run after applying:
```bash
[language-appropriate quality gate commands]
```
```

---

## Mode: `suggest`

Given a description of a symbol's purpose, return 3 ranked candidate names with rationale.

### Input fields used

- `purpose_description` — plain English description of what the symbol does or represents
- `symbol_type` — `function` \| `class` \| `variable` \| `module` \| `constant`
- `language` — determines casing convention
- `standard` — `general` (Clean Code principles) or `ob` (BORO actor-action conventions)

### Workflow

1. Load naming standards for the selected `standard`
2. Apply the noun/verb convention for the `symbol_type`
3. Generate 3 candidate names, ranked by how precisely they express purpose
4. Explain the rationale for each

### Output (suggest)

```
## Name Suggestions — [symbol_type]

**Purpose:** [purpose_description]
**Language:** [language]
**Standard:** [general | ob]

---

| Rank | Candidate | Rationale |
|------|-----------|-----------|
| 1 | `extract_transactions_from_csv` | Verb-first; expresses action + subject + source precisely |
| 2 | `load_transactions_from_file` | Slightly less specific about format |
| 3 | `import_transactions` | Accurate but omits source detail |

**Recommended:** `extract_transactions_from_csv`
[One sentence justification]
```


---

## Feedback

If the user corrects this skill's output due to a misinterpretation or missing rule **in the skill itself** (not a one-off preference), invoke `skill-feedback` to capture structured feedback and optionally post a GitHub issue.

If `skill-feedback` is not installed, ask the user: *"This looks like a skill defect. Would you like to install the `skill-feedback` skill to report it?"* If the user declines, continue without feedback capture.
