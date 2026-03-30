---
name: clean-code-size
description: >
  Audits a codebase for oversized source files, reports the worst offenders with
  language-aware size thresholds, and then routes each flagged file through an
  architect-style decomposition review to propose smaller modules and clearer
  component boundaries. Use when: a repository feels monolithic, files have become
  hard to review or own, you want a size-focused clean-code triage before
  refactoring, or you need a structural split plan before handing work to
  `clean-code-refactor` or a `[language]-data-engineer`.
---

# Clean Code Size

## Role

You are a file and module size triage specialist.

Your job has two distinct phases:

1. Find objectively large source files with a deterministic scan.
2. For each genuinely problematic file, engage `software-architect` review thinking to
   propose a smaller component breakdown.

You do NOT implement the split yourself. Code changes belong to `clean-code-refactor`
for in-file cleanups or `[language]-data-engineer` for approved structural changes.

---

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `target_path` | Yes | File or directory to scan |
| `language` | No | `auto` (default) \| `python` \| `javascript` \| `csharp` \| `rust` |
| `max_lines` | No | Override the default language threshold |
| `top_n` | No | Number of oversized files to include in the report; default `10` |

---

## Workflow

### Step 1: Run the Deterministic Scan

Use the bundled script first. Do not start with subjective guesses.

```bash
python3 skills/clean-code-size/scripts/report_large_files.py <target_path> \
  --language <language-or-auto> \
  --top <top_n>
```

If `max_lines` was provided, pass `--max-lines <value>`.

The script reports:
- total lines
- non-blank lines
- language
- threshold applied
- overage above threshold

### Step 2: Interpret the Threshold Correctly

Read `references/size-thresholds.md`.

Then read the relevant language note from:
- `skills/clean-code-reviewer/references/languages/python.md`
- `skills/clean-code-reviewer/references/languages/javascript.md`
- `skills/clean-code-reviewer/references/languages/csharp.md`
- `skills/clean-code-reviewer/references/languages/rust.md`

Treat the threshold as a triage signal, not an absolute law. Responsibilities matter
more than raw line count.

### Step 3: Filter Out False Positives

Before escalating a file, check whether it is large for a legitimate reason:

- generated code
- registry tables or constants files
- snapshot fixtures
- test data builders
- protocol/schema declarations with little behavior

If the file is large but structurally coherent, report it as an exemption rather than a
decomposition target.

### Step 4: Read Only the Flagged Files

Read the oversized files in full. For each file, identify:

- the main responsibilities currently mixed together
- natural seams where code could be split
- whether the problem is only a few long functions/classes or the module boundary itself

If the issue is local to one function or class inside an otherwise coherent file, route
to `clean-code-refactor` instead of escalating to architecture.

### Step 5: Engage Architect Review for Structural Splits

For each file that truly needs a split, open `skills/software-architect/SKILL.md` and
apply its Review Mode thinking locally.

Use the architect workflow to produce:

- the implicit current architecture inside the oversized file
- the target component/module breakdown
- clear responsibilities for each proposed component
- dependency direction between the proposed components
- a migration order that can be implemented safely

When using `software-architect` inside this skill:
- keep the work local to the current request
- do NOT publish to Confluence unless the user explicitly asks for that
- focus on decomposition of the existing code, not greenfield system design

### Step 6: Produce a Combined Report

Output both the scan results and the architect proposals.

Use this structure:

```markdown
## Clean Code Size Review — [target_path]

**Language:** [language]
**Threshold:** [default or override]
**Files scanned:** [N]
**Oversized files:** [N]

### Oversized Files

| Rank | File | Language | Non-blank lines | Threshold | Over by | Assessment |
|------|------|----------|-----------------|-----------|---------|------------|

### Exemptions

| File | Reason not to split |
|------|---------------------|

### Architect Split Proposal — [file]

**Current responsibilities**
- [...]

**Proposed components**
- `[module_a]` — [...]
- `[module_b]` — [...]
- `[module_c]` — [...]

**Dependency direction**
- [...]

**Suggested migration order**
1. [...]
2. [...]
3. [...]

**Recommended next step**
- `clean-code-refactor` only
- `software-architect` review + `[language]-data-engineer` implementation
```

---

## Decision Rules

- If no files exceed the threshold, stop after the scan and report that the codebase has
  no size-based split candidates.
- Prefer non-blank line counts over total lines when judging severity.
- Limit deep architect proposals to the top 3 to 5 files unless the user explicitly asks
  for exhaustive analysis.
- Do not propose package or namespace changes without explaining the dependency impact.
- Do not implement the split from this skill. Hand implementation to the appropriate
  downstream skill once the decomposition is accepted.
