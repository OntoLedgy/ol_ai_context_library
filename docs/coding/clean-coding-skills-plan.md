# Coding Skills — Development Plan

## Overview

This document defines the modular skill architecture for software design and data engineering. Skills are organised into three tiers:

1. **General roles** (`software-architect`, `data-engineer`) — foundation skills grounded in design philosophy and clean coding standards
2. **Specialised inheriting roles** (`bclearer-pipeline-architect`, `bclearer-pipeline-engineer`, `bie-component-ontologist`, `bie-data-engineer`) — extend general roles with domain/platform-specific knowledge
3. **Sub-skills** (`clean-code-*`) — focused tools that engineer roles delegate to for specific tasks

Sub-skills are tools a role *uses*. Inheriting roles are specialisations of the same persona — they extend their parent's full workflow and add context-specific knowledge on top.

---

## Inheritance Design Decision

> **Decision:** bclearer pipeline roles and language-specific roles inherit from general roles; they do not become sub-skills.

**Rationale:** A bclearer pipeline architect IS a software architect (same modes, same deliverable format, same design philosophy) — it extends the persona with bclearer pipeline knowledge. A `python-data-engineer` IS a `data-engineer` — it extends the persona with Python-specific conventions. Sub-skills are tools with a narrow scope (e.g. `clean-code-reviewer`). The "IS A" vs "USES A" distinction maps directly to role inheritance vs sub-skill delegation.

**Inheritance mechanism:** Each child `SKILL.md` opens with: *"Read `skills/[parent]/SKILL.md` first and follow all of it. This file contains only the additions and overrides."* No duplication of parent content.

Note: the `extends:` frontmatter field is not supported by the skill loader. The inheritance relationship is expressed in the `description` field and in the body text only.

**Precedent:** `bie-component-ontologist` and `bie-data-engineer` already follow this pattern implicitly — they are now formally classified as inheriting roles.

---

## Skill Hierarchy

```
skills/
│
├── software-architect/                    ← TIER 1: General design role
│   ├── SKILL.md
│   └── references/
│       ├── design-philosophy.md           (BORO, BNOP, BIE identity concepts)
│       ├── technology-stack.md            (bnop, interop_services, orchestration_services)
│       ├── design-patterns.md             (factory, registry, adapter, leaf-before-whole...)
│       └── confluence-pages.md            (where to document designs)
│
├── bclearer-pipeline-architect/           ← TIER 2: Inherits software-architect
│   ├── SKILL.md
│   └── references/
│       ├── pipeline-patterns.md           (stage topology, universe wiring)
│       ├── interop-conventions.md         (which services in which contexts)
│       ├── orchestration-conventions.md   (runner, universe lifecycle)
│       └── confluence-pages.md            (pipeline-specific Confluence space)
│
├── bie-component-ontologist/              ← TIER 2: Inherits software-architect (implicit)
│   └── ...                                (BIE component ontology design)
│
├── ob-architect/                          ← TIER 2: Inherits software-architect
│   ├── SKILL.md
│   └── references/
│       ├── boro-coding-principles.md      (actor-action, orchestration, contract, fail-fast patterns)
│       └── ob-library-selection.md        (boro: nf_common | ontoledgy: bclearer_pdk + ai + ui)
│
├── data-engineer/                         ← TIER 1: General implementation role (language-agnostic)
│   ├── SKILL.md
│   └── references/
│       ├── clean-coding-index.md          (map: concern → standard document)
│       └── testing-index.md               (testing philosophy, structure, quality gates)
│
├── python-data-engineer/                  ← TIER 2: Inherits data-engineer
│   ├── SKILL.md
│   └── references/
│       ├── language-standards.md          (PEP 8, type hints, naming, idioms)
│       ├── tooling.md                     (ruff, mypy, pytest, pyproject.toml)
│       └── patterns.md                    (context managers, dataclasses, generators, protocols)
│
├── javascript-data-engineer/              ← TIER 2: Inherits data-engineer
│   ├── SKILL.md
│   └── references/
│       ├── language-standards.md          (TypeScript conventions, type system, modules)
│       ├── tooling.md                     (eslint, prettier, tsc, vitest)
│       └── patterns.md                    (async/await, Result type, DI, functional)
│
├── csharp-data-engineer/                  ← TIER 2: Inherits data-engineer
│   ├── SKILL.md
│   └── references/
│       ├── language-standards.md          (C# naming, records, nullable, LINQ, async)
│       ├── tooling.md                     (dotnet CLI, xUnit, Roslyn, .editorconfig)
│       └── patterns.md                    (Result, DI, Options pattern, async streams)
│
├── rust-data-engineer/                    ← TIER 2: Inherits data-engineer
│   ├── SKILL.md
│   └── references/
│       ├── language-standards.md          (ownership, borrowing, traits, naming)
│       ├── tooling.md                     (cargo, clippy, rustfmt, tarpaulin)
│       └── patterns.md                    (Result/Option, builder, newtype, iterators, async)
│
├── bclearer-pipeline-engineer/            ← TIER 3: Inherits ob-engineer (bclearer is an OB framework)
│   ├── SKILL.md
│   └── references/
│       ├── pipeline-implementation.md     (stage file layout, class/function conventions)
│       ├── bclearer-code-style.md         (overrides Python style for bclearer conventions)
│       └── bie-integration.md             (when/how to delegate to bie-data-engineer)
│
├── bie-data-engineer/                     ← TIER 3: Inherits python-data-engineer (implicit)
│   └── ...                                (BIE domain implementation)
│
├── ob-engineer/                           ← TIER 2: Inherits python-data-engineer
│   ├── SKILL.md
│   └── references/
│       ├── boro-quick-style-guide.md      (BORO Quick Style Guide + overrides vs PEP8)
│       └── ob-library-selection.md        (boro: nf_common | ontoledgy: bclearer_pdk + ai + ui)
│
├── clean-code-reviewer/                   ← Sub-skill: Detect violations
├── clean-code-refactor/                   ← Sub-skill: Fix violations
├── clean-code-naming/                     ← Sub-skill: Naming focus
├── clean-code-tests/                      ← Sub-skill: Test generation/review
└── clean-code-commit/                     ← Sub-skill: Commit messages
```

**Inheritance chain for bclearer pipeline work:**
```
data-engineer → python-data-engineer → ob-engineer → bclearer-pipeline-engineer
```

> bclearer is an OB-specific framework — `bclearer-pipeline-engineer` now inherits from `ob-engineer`, not `python-data-engineer` directly. This means bclearer pipeline code inherits the full BORO Quick Style Guide and OB library conventions before adding bclearer-specific patterns on top.

**Inheritance chain for OB (Ontoledgy/BORO) work:**
```
software-architect → ob-architect
data-engineer → python-data-engineer → ob-engineer
```

OB skills fill the **Ontology scope gap** identified in `SKILL-ARCHITECTURE.md`. Both `ob-architect` and `ob-engineer` are variant-aware: they consult `ob-library-selection.md` to determine whether the target codebase is BORO (`nf_common`) or Ontoledgy (`bclearer_pdk + ai + ui`).

**Language tier** sits at Tier 2, between the language-agnostic `data-engineer` and any platform-specific engineer (bclearer, etc.). Each language skill adds: naming conventions, error handling idioms, tooling, and language-specific patterns.

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

### OB Architect (`ob-architect`)

Extends `software-architect`. Adds BORO coding conventions at the design level:
- Actor-action module naming in all component designs
- Explicit orchestration layer in every multi-step solution
- Mandatory constants/enum configuration layer
- Explicit type contracts on all component interfaces
- Fail-fast validation gates at ingress boundaries
- Platform library inventory check before designing custom components (reads `ob-library-selection.md` to determine which libraries apply)

Scope: **Ontology** — fills the `architect:design:ontology:agnostic` gap in the SKILL-ARCHITECTURE matrix.

### OB Engineer (`ob-engineer`)

Extends `python-data-engineer`. Adds BORO Quick Style Guide as the coding standard, overriding PEP8 where they conflict. Reads `ob-library-selection.md` at the start of every session to determine the active library set.

| Variant | Platform Libraries |
|---------|-------------------|
| BORO | `nf_common` — `Files`, `Folders`, and all general utilities |
| Ontoledgy | `bclearer_pdk`, `ai`, `ui` libraries |

Scope: **Ontology** — fills the `engineer:implement:ontology:python` gap in the SKILL-ARCHITECTURE matrix.

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

**Input:** `mode` + `target_path` + optional `severity_threshold` + optional `standard`

| `standard` value | Convention set loaded |
|-----------------|----------------------|
| `general` _(default)_ | `prompts/coding/standards/clean_coding/` |
| `ob` | OB overrides from `ob-engineer/references/boro-quick-style-guide.md` layered on top of `general`; OB wins on conflicts |

**Output:** Violation list — location, rule, convention (`general` or `ob`), severity (HIGH/MEDIUM/LOW), suggested fix

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

**Input:** `mode` + `target_path` + optional `violations_report` + optional `standard`

| `standard` value | Convention set applied |
|-----------------|----------------------|
| `general` _(default)_ | `prompts/coding/standards/clean_coding/` |
| `ob` | OB overrides from `ob-engineer/references/boro-quick-style-guide.md` layered on top of `general`; OB wins on conflicts |

When `standard=ob` and a `violations_report` is passed from `clean-code-reviewer`, the standards must match — pass the same `standard` value to both skills.

**Output:** Refactored file(s) with change summary (each change + rule applied + convention source: `general` or `ob`)

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

## Refactoring Workflow

The skill set supports a complete refactoring workflow for dirty code. Apply steps
in order — skipping early steps produces lower quality results.

```
Step 1: ARCHITECTURAL REVIEW
  software-architect (Review Mode)
  → reads existing code
  → produces: gap analysis + target architecture design
  → use when: wrong structure, missing abstractions, wrong dependency direction

Step 2: CODE-LEVEL VIOLATION SCAN
  [language]-data-engineer (Review Mode)  OR  clean-code-reviewer
  → reads same code
  → produces: violation report (HIGH/MEDIUM/LOW, with suggested fixes)
  → use when: function size, naming, error handling, smells

Step 3: STRUCTURAL REFACTOR (if Step 1 found issues)
  [language]-data-engineer (Implement Mode)
  → input: architect's target design from Step 1
  → implements structural changes (module layout, class splits, dependency inversion)
  → does NOT fix code-level violations — leave those for Step 4

Step 4: CODE-LEVEL REFACTOR (if Step 2 found violations)
  clean-code-refactor
  → input: violation report from Step 2 (or re-scan after Step 3)
  → fixes: function size, naming, error patterns, smells
  → flags anything structural it cannot fix (those go back to Step 3)

Step 5: VERIFY
  Run language quality gates (ruff+mypy+pytest / tsc+eslint+vitest / dotnet / cargo clippy+test)
  Re-run clean-code-reviewer to confirm violations resolved
```

**Shortcut for code-only dirty code (no architectural issues):**
```
clean-code-reviewer → clean-code-refactor → verify
```

**Shortcut for architectural-only problems (structure is wrong, code style is fine):**
```
software-architect (Review Mode) → [language]-data-engineer (Implement Mode) → verify
```

---

## Implementation Order

### Phase 1 — Foundation (complete)

1. `software-architect` — **DONE** (SKILL.md + 4 references)
2. `data-engineer` — **DONE** (SKILL.md + 2 references)
3. `bclearer-pipeline-architect` — **DONE** (skeleton — 4 references, TODOs to populate)
4. `bclearer-pipeline-engineer` — **DONE** (skeleton — 4 references, TODOs to populate)
5. `python-data-engineer` — **DONE** (SKILL.md + 3 references)
6. `javascript-data-engineer` — **DONE** (SKILL.md + 3 references)
7. `csharp-data-engineer` — **DONE** (SKILL.md + 3 references)
8. `rust-data-engineer` — **DONE** (SKILL.md + 3 references)

### Phase 2 — Core clean coding pair (complete)

9. `clean-code-reviewer` — **DONE** (SKILL.md + report template + 4 language refs)
10. `clean-code-refactor` — **DONE** (SKILL.md + change summary template + 4 language refs)

### Phase 3 — High-frequency standalone (complete)

11. `clean-code-naming` — **DONE** (SKILL.md — modes: review, fix, suggest; supports general + ob standards)
12. `clean-code-tests` — **DONE** (SKILL.md — modes: generate, review, coverage-check)

### Phase 4 — Workflow integration (complete)

13. `clean-code-commit` — **DONE** (SKILL.md — modes: validate, generate)

### Phase 5 — Fill bclearer skeletons (complete)

Populated from `ol_bclearer_pdk/libraries/core/bclearer_core/pipeline_builder/` source code:
- `bclearer-pipeline-architect/references/pipeline-patterns.md` — **DONE** (5-stage topology, B-unit types, Universe wiring, design workflow, CLI config, generated directory structure)
- `bclearer-pipeline-architect/references/interop-conventions.md` — **DONE** (full service catalogue, format selection guide, adapter boundary rules, credential conventions)
- `bclearer-pipeline-architect/references/orchestration-conventions.md` — **DONE** (full call chain, all orchestrator templates, Universe lifecycle, environment setup, testing convention)
- `bclearer-pipeline-engineer/references/pipeline-implementation.md` — **DONE** (file/class naming conventions, all code templates: B-unit, orchestrators, runner, entry point, Universe, test patterns, verification checklist)
- `bclearer-pipeline-engineer/SKILL.md` — **UPDATED** inheritance from `python-data-engineer` → `ob-engineer` (bclearer is an OB-specific framework)

### Phase 6 — OB (Ontoledgy/BORO) skills (complete)

Fills the **Ontology scope gap** identified in `SKILL-ARCHITECTURE.md`. See `docs/coding/boro-skills-plan.md` for full design.

14. `ob-architect` — **DONE** (SKILL.md + `boro-coding-principles.md` + `ob-library-selection.md`)
15. `ob-engineer` — **DONE** (SKILL.md + `boro-quick-style-guide.md` + `ob-library-selection.md`)

Both skills carry their own copy of `ob-library-selection.md` (variant → platform library mapping).

### Phase 7 — Migrate `bie-data-engineer` inheritance to `ob-engineer` _(deferred)_

`bie-data-engineer` should eventually inherit from `ob-engineer` (BIE is an OB-specific framework, just as bclearer is). This is deferred because:
- `bie-data-engineer` is already battle-hardened and in active use
- `ob-engineer` must be built and validated in production first (Phase 6)
- Changing `bie-data-engineer`'s inheritance chain carries regression risk until `ob-engineer` is proven

**Trigger:** Begin this phase only after `ob-engineer` has been tested on real OB codebases and is considered stable.

When ready:
- Update `bie-data-engineer/SKILL.md` inheritance declaration from `python-data-engineer` → `ob-engineer`
- Update `SKILL-ARCHITECTURE.md` inheritance diagram
- Re-test `bie-data-engineer` to confirm no regressions from the added OB conventions

---

## bclearer Pipeline Skills (Tier 2 — Skeletons Created)

### `bclearer-pipeline-architect` — **SKELETON DONE**

Extends `software-architect`. Adds:
- Pipeline topology (4-stage: Ingest / Identify / Transform / Load)
- Additional Design Mode deliverable: Pipeline Stage Map
- Additional Review Mode checklist items (stage separation, interop boundaries, universe scoping)
- bclearer interop service conventions (`references/interop-conventions.md`)
- bclearer orchestration conventions — runner, universe lifecycle (`references/orchestration-conventions.md`)
- Pipeline-specific Confluence page structure

Reference files marked `Status: Skeleton` — populate as pipeline patterns are confirmed from the codebase.

### `bclearer-pipeline-engineer` — **SKELETON DONE** _(inheritance update pending)_

Extends `ob-engineer` (not `data-engineer` directly — bclearer is an OB-specific framework; the SKILL.md inheritance declaration needs updating when `ob-engineer` is built). Adds:
- Pipeline code layout convention (`bie/`, `adapters/`, `services/`, `orchestrators/`, `runners/`)
- Construction order for pipelines (common knowledge → BIE objects → adapters → services → orchestrators → runner)
- bclearer code style overrides (backslash continuations, named kwargs, verbose naming, class plurals)
- BIE integration protocol — when to delegate to `bie-data-engineer`, handoff format, identity flow through stages
- Additional verification checklist (stage independence, interop boundary, universe scoping)

Reference files marked `Status: Skeleton` — populate as implementation patterns are confirmed.

---

## Open Questions

1. **References strategy** — Copy standards into each skill's `references/` dir, or reference the shared `prompts/coding/standards/` path? Current approach: index files in `data-engineer/references/` point to shared path; no duplication.
2. **Refactor output mode** — Should `clean-code-refactor` write changes directly or propose as a diff? Recommendation: default to proposing, with `apply` mode for direct writes.
3. **Phase 2 priority** — `clean-code-reviewer` before or after `clean-code-naming`? Naming has higher daily use but reviewer covers a broader surface area. Recommendation: reviewer first.
