---
name: feature-spec-author
description: >
  Author a full feature specification — requirements, design, and tasks — for a single
  feature in the ol-sdd-workflow. Wraps software-architect in feature-design mode and
  extends it to produce all three artifacts (requirements.md, design.md, tasks.md)
  with three in-phase approval gates. Use when: designing a new feature, breaking a
  feature from the development plan into implementable tasks, or re-specifying an
  existing feature. Phase 1 of the ol-sdd-workflow orchestrator. Outputs land in
  .claude/specs/{feature-name}/ and on Confluence.
---

# Feature Spec Author

## Role

You author the full specification for one feature. A feature spec is three documents, in strict order, with an approval gate between each. You delegate the design-level analysis to `software-architect` (feature-design mode) and wrap it with the requirements and tasks phases.

You are invoked by the `ol-sdd-workflow` orchestrator at Phase 1, or directly by a user or architect.

## Deliverables

| File | Template | Produced by | Gate |
|------|----------|-------------|------|
| `.claude/specs/{feature}/requirements.md` | `requirements-template.md` | This skill | 1a — requirements approval |
| `.claude/specs/{feature}/design.md` | `design-template.md` | `software-architect` (feature mode) | 1b — design approval |
| `.claude/specs/{feature}/tasks.md` | `tasks-template.md` | This skill | 1c — tasks approval |

All three are published as a single Confluence page (with sub-sections) or three child pages, under the project's parent page.

## Workflow

### Step 1 — Load Steering and Release Context

Read `.claude/steering/product.md`, `tech.md`, `structure.md`. If absent, stop and route the user back to `product-vision-steering` (Phase 0). A feature spec cannot be authored without steering context.

Also read `.claude/releases/*/epic-map.md` if any release is active. If the target feature appears in a release's epic-map, note the linked JIRA epic key — the spec will attach to that existing epic rather than create a new one downstream.

### Step 2 — Confirm Feature Scope

Confirm with the user:
- Feature name (kebab-case, e.g., `licence-data-extraction`)
- One-line description (or read from the release's features.md if present)
- Release epic to attach to (if a release plan exists): confirm the JIRA epic key from `epic-map.md`
- Upstream feature dependencies
- Known constraints (deadline, scope exclusions, must-not-change areas)

Create the directory `.claude/specs/{feature}/` and initialise empty files.

### Step 3 — Gate 1a: Requirements

Populate `requirements.md` from `requirements-template.md`. Each requirement:
- User story: "As a [role], I want [feature], so that [benefit]"
- Acceptance criteria in EARS format ("WHEN...THEN the system SHALL...")
- Numbered so tasks can reference them later (1.1, 1.2, 2.1, …)

Include the non-functional requirements section (performance, security, reliability, usability) — cut any that don't apply.

Present to user. **Gate 1a: user approves requirements before design work begins.**

### Step 4 — Gate 1b: Design

Invoke `software-architect` in feature-design mode with:
- The approved requirements
- Steering context
- Feature scope and dependencies

The `software-architect` skill produces `design.md` from `design-template.md`, including:
- Overview
- Steering alignment (how design follows tech.md and structure.md)
- Code reuse analysis
- Architecture diagram (Mermaid)
- Components and interfaces
- Data models
- Error handling
- Testing strategy
- BORO grounding (if OL/bclearer project)
- Identity design (if BIE domain)

Return the design to the user. **Gate 1b: user approves design before task breakdown.**

### Step 5 — Gate 1c: Tasks

Break the design into atomic tasks using `tasks-template.md`. Enforce the atomic task requirements:
- **File scope**: 1–3 related files maximum
- **Time boxing**: completable in 15–30 minutes
- **Single purpose**: one testable outcome per task
- **Specific files**: exact paths to create or modify
- **Agent-friendly**: clear input/output

Each task must reference:
- `_Requirements: X.Y_` — which acceptance criteria it fulfils (links back to requirements.md)
- `_Leverage: path/to/file_` — existing code to reuse (reinforces reuse-over-reinvention)
- `_Skill: {skill-name}_` — **new field** — which engineer skill should implement it. Use the skill-routing table in `references/skill-routing.md`.

Estimate each task in hours (for JIRA backlog in Phase 2).

Present to user. **Gate 1c: user approves tasks before the spec is published and JIRA tickets are created.**

### Step 6 — Publish

On all three gates passing:
1. Commit the three files to `.claude/specs/{feature}/`
2. Publish a Confluence page (use Atlassian MCP). Page structure:
   - H1: `{Feature Name} — Spec`
   - H2: Requirements (embed requirements.md)
   - H2: Design (embed design.md)
   - H2: Tasks (embed tasks.md)
3. If a release epic exists for this feature:
   - Update the JIRA epic description to include a link to the Confluence spec page
   - Update `.claude/releases/{release}/epic-map.md` — change the Spec Status column for this feature from "not specced" to "specced" (or "specced, ready for backlog")
   - Do NOT create a new epic; the spec attaches to the existing release skeleton
4. If no release plan exists: a standalone epic will be created later by `backlog-manager` (Phase 2)
5. Record the Confluence page URL in the workflow config
6. Return to caller with links (including the release epic key if applicable)

---

## Task Format with Skill Routing

```markdown
- [ ] 1. Add licence columns to LegalEntities model
  - File: trade_analysis_services/common/models/legal_entities.py
  - Add 11 licence columns per spec §3
  - Purpose: Persist licence data extracted by pipeline
  - _Leverage: trade_analysis_services/common/models/base.py_
  - _Requirements: 1.1, 1.2_
  - _Skill: python-data-engineer_
  - _Estimate: 2h_
```

The `_Skill:` hint is consumed by `backlog-manager` (as a JIRA label) and by `sprint-executor` (as the delegation target).

## What This Skill Does NOT Do

- Does not do BORO or BIE ontology analysis — delegate to `ontologist` / `ob-ontologist` / `bie-component-ontologist` when needed
- Does not create JIRA tickets (Phase 2 / `backlog-manager`)
- Does not implement tasks (Phase 4 / `sprint-executor`)
- Does not refresh steering docs (Phase 0 / `product-vision-steering`)

## References

- `prompts/coding/templates/requirements-template.md`
- `prompts/coding/templates/design-template.md`
- `prompts/coding/templates/tasks-template.md`
- `skills/software-architect/SKILL.md` (feature-design mode)
- `references/skill-routing.md` — skill routing table for `_Skill:` field
