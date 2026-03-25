# Coding Skills — Development Plan

## Overview

This document defines the modular skill architecture for software design and data engineering. Skills are organised into two tiers:

1. **Software Architect** — designs solutions grounded in ontological methods; documents in Confluence
2. **Data Engineer** — implements and reviews code applying clean coding standards

The clean coding skills are modular sub-skills used by the Data Engineer. All skills are designed to be general-purpose and reusable at the bclearer pipeline level when bclearer-specific engineer/architect skills are introduced later.

---

## Skill Hierarchy

```
skills/
│
├── software-architect/              ← TIER 1: Design
│   ├── SKILL.md
│   └── references/
│       ├── design-philosophy.md     (BORO, BNOP, BIE identity concepts)
│       ├── technology-stack.md      (bnop, interop_services, orchestration_services)
│       ├── design-patterns.md       (factory, registry, adapter, leaf-before-whole...)
│       └── confluence-pages.md      (where to document designs)
│
├── data-engineer/                   ← TIER 2: Implementation
│   ├── SKILL.md
│   └── references/
│       ├── clean-coding-index.md    (map: concern → standard document)
│       └── testing-index.md         (testing philosophy, structure, quality gates)
│
├── clean-code-reviewer/             ← TIER 2 Sub-skill: Detect violations
├── clean-code-refactor/             ← TIER 2 Sub-skill: Fix violations
├── clean-code-naming/               ← TIER 2 Sub-skill: Naming focus
├── clean-code-tests/                ← TIER 2 Sub-skill: Test generation/review
└── clean-code-commit/               ← TIER 2 Sub-skill: Commit messages
│
├── bie-component-ontologist/        ← EXISTING: BIE domain ontology design
└── bie-data-engineer/               ← EXISTING: BIE domain implementation
```

---

## Role Responsibilities

### Software Architect

| Capability | Detail |
|-----------|--------|
| **Design Mode** | Given requirements: gather context, fetch Confluence reference, produce 5 architecture deliverables (overview, component model, technology mapping, integration design, open questions), present for approval, publish to Confluence |
| **Review Mode** | Review existing solution: extract implicit architecture, run review checklist, produce gap analysis, publish findings to Confluence |
| **Does NOT** | Write code, implement features, produce BIE component-level designs (that is `bie-component-ontologist`) |

Design philosophy grounded in:
- BORO upper ontology (4D individuals, types, wholes/parts, names)
- BNOP (Python implementation: `BnopObjects`, registries, tuples)
- BIE (deterministic identity, factory pattern, leaf-before-whole)
- bclearer technology stack (bnop, interop_services, orchestration_services)

### Data Engineer

| Capability | Detail |
|-----------|--------|
| **Implement Mode** | Build features from approved design: reads spec, reads existing code first, implements in construction order, writes tests, verifies (pytest/mypy/ruff) |
| **Review Mode** | Review code: applies clean coding checklist (functions, classes, naming, errors, smells, tests), produces violation report with severity and suggested fixes, delivers APPROVE/REQUEST CHANGES/REJECT verdict |
| **Does NOT** | Design architecture, produce ontology models |

Delegates specialised clean coding tasks to:
- `clean-code-reviewer`, `clean-code-refactor`, `clean-code-naming`, `clean-code-tests`, `clean-code-commit`

---

## Clean Coding Sub-Skills

### Source Material

All grounded in existing standards at `prompts/coding/standards/`:

| Standard Document | Concern |
|-------------------|---------|
| `clean_coding/functions.md` | Functions: size, single responsibility, argument count |
| `clean_coding/classes.md` | Classes: SRP, cohesion, coupling, size |
| `clean_coding/meaningful_names.md` | Naming: intent, conventions, searchability |
| `clean_coding/error_handling.md` | Exceptions, null patterns, context |
| `clean_coding/comments.md` | Comment necessity, TODOs, self-documenting code |
| `clean_coding/formatting.md` | Vertical/horizontal structure |
| `clean_coding/objects_and_data_structures.md` | Encapsulation, Law of Demeter |
| `clean_coding/boundaries.md` | Third-party interfaces, wrapping |
| `clean_coding/concurrency.md` | Thread safety, shared state |
| `clean_coding/emergence.md` | Run all tests, no duplication, minimalism |
| `clean_coding/systems.md` | Dependency injection, construction/use separation |
| `clean_coding/smells_and_heuristics.md` | Full smell catalogue |
| `clean_coding/clean_coding_full_details.md` | Complete reference |
| `testing/TESTING_GUIDELINES.md` | Testing philosophy, structure, what to test |
| `testing/TEST_QUALITY_REQUIREMENTS.md` | Coverage, quality gates, assertion patterns |
| `testing/unit_tests.md` | Isolation, mocking, test doubles |
| `cicd/commit_standards.md` | Conventional Commits specification |

---

### Sub-Skill Definitions

#### 1. `clean-code-reviewer`

**Purpose:** Analyse code and produce a structured violation report.

| Mode | Checks |
|------|--------|
| `full` | All standards combined |
| `functions` | Size, argument count, abstraction level, side effects, flag arguments |
| `classes` | SRP, cohesion, coupling, size, dependency direction |
| `naming` | Intent-revealing, noun/verb conventions, searchability, no encoding |
| `errors` | Exception patterns, null returns/params, context in exceptions |
| `smells` | Duplication, dead code, magic numbers, feature envy, large classes |

**Input:** `mode` + `target_path` + optional `severity_threshold`

**Output:** Violation list — location, rule, severity (HIGH/MEDIUM/LOW), suggested fix

---

#### 2. `clean-code-refactor`

**Purpose:** Rewrite code to fix clean coding violations. Operates on a file or on the output of `clean-code-reviewer`.

| Mode | What It Fixes |
|------|---------------|
| `functions` | Extract methods, reduce args, remove flag args, separate concerns |
| `classes` | Split responsibilities, improve cohesion, apply SRP |
| `naming` | Rename symbols to reveal intent across a file/module |
| `errors` | Convert return codes to exceptions, remove null returns/params |
| `smells` | DRY violations, dead code removal, magic number extraction |

**Input:** `mode` + `target_path` + optional `violations_report`

**Output:** Refactored file(s) with change summary (each change + rule applied)

---

#### 3. `clean-code-naming`

**Purpose:** Standalone naming skill — highest daily-use value.

| Mode | Description |
|------|-------------|
| `review` | Audit all names in a file/module; flags violations with explanation |
| `fix` | Rename symbols to comply with standards; before/after mapping |
| `suggest` | Given a purpose description, return 3 ranked candidate names with rationale |

**Input:** `mode` + `target_path` (review/fix) or `purpose_description` + `symbol_type` (suggest)

**Output:** Violation list (review), renamed file (fix), or 3 ranked name suggestions (suggest)

---

#### 4. `clean-code-tests`

**Purpose:** Generate and review tests following project testing standards.

| Mode | Description |
|------|-------------|
| `generate` | Create unit tests for a class or function — happy path, error conditions, edge cases |
| `review` | Review existing tests against quality requirements |
| `coverage-check` | Identify untested paths — produce gap analysis with recommended test cases |

**Input:** `mode` + `target_path` + optional `test_category` (unit/integration)

**Output:** Test file (generate), annotated review report (review), gap analysis (coverage-check)

---

#### 5. `clean-code-commit`

**Purpose:** Validate or generate commit messages per the Conventional Commits specification.

| Mode | Description |
|------|-------------|
| `validate` | Check a commit message — returns pass/fail with issues |
| `generate` | Generate a compliant commit message from a diff or change description |

**Input:** `mode` + `commit_message` (validate) or `diff_or_description` (generate) + optional `scope`

**Output:** Pass/fail with issue list (validate), or formatted commit message with type/scope/description (generate)

---

## Implementation Order

### Phase 1 — Foundation (implement first)

1. `software-architect` — **DONE** (SKILL.md + 4 references created)
2. `data-engineer` — **DONE** (SKILL.md + 2 references created)

### Phase 2 — Core clean coding pair (highest ROI)

3. `clean-code-reviewer` — establishes baseline; other skills build on its output
4. `clean-code-refactor` — acts on reviewer output; completes the detect-and-fix loop

### Phase 3 — High-frequency standalone

5. `clean-code-naming` — high daily use; narrow scope, easy to validate
6. `clean-code-tests` — critical for quality gates; ties into existing testing standards

### Phase 4 — Workflow integration

7. `clean-code-commit` — narrow scope; CI/CD integration point

---

## Future Extension Points

### bclearer Data Engineer (planned)

Extends `data-engineer` with:
- bclearer code style conventions (`bie-data-engineer/references/code-style.md`)
- BIE factory/identity patterns
- bclearer pipeline construction patterns
- Delegates to existing `bie-data-engineer` for BIE-specific domain implementation

### bclearer Architect (planned)

Extends `software-architect` with:
- bclearer pipeline design patterns
- Interop service selection patterns specific to bclearer contexts
- Deeper integration with BIE component ontology workflow

These future skills will import and extend (not duplicate) the general skills defined here.

---

## Open Questions

1. **References strategy** — Copy standards into each skill's `references/` dir, or reference the shared `prompts/coding/standards/` path? Current approach: index files in `data-engineer/references/` point to shared path; no duplication.
2. **Refactor output mode** — Should `clean-code-refactor` write changes directly or propose as a diff? Recommendation: default to proposing, with `apply` mode for direct writes.
3. **Phase 2 priority** — `clean-code-reviewer` before or after `clean-code-naming`? Naming has higher daily use but reviewer covers a broader surface area. Recommendation: reviewer first.
