# Phase Flow — I/O Contracts

Each phase has a defined input contract (what must exist before it starts) and output contract (what it produces). This file is the reference for orchestration.

## Phase 0 — Steering

**Input:**
- A codebase directory (existing or empty)
- Optionally: user-provided product goals, known tech stack, known directory preferences

**Output:**
- `documentation/steering/product.md` (from `prompts/coding/templates/product-template.md`)
- `documentation/steering/tech.md` (from `prompts/coding/templates/tech-template.md`)
- `documentation/steering/structure.md` (from `prompts/coding/templates/structure-template.md`)
- Confluence page: "Project Steering — {project name}" with three child pages

**Approval gate output:** Three documents committed to repo and published to Confluence.

## Phase 0.5 — Release Plan

**Input:**
- Approved steering docs (Phase 0 output)
- Release target (name + date)
- Capacity (engineer-days or hours across the release window)
- Optional: stakeholder feature requests, carry-over from prior releases

**Output:**
- `documentation/releases/{release-name}/features.md` (from `release-plan-template.md`): prioritised feature list with MoSCoW, T-shirt sizes, dependencies, three scope tiers
- `documentation/releases/{release-name}/epic-map.md`: feature → JIRA epic key mapping, with a Spec Status column that downstream skills update
- Confluence page: "Release Plan — {release-name}" under the project parent
- JIRA epic per in-scope feature (skeleton: summary, description, `release:{name}` label, priority label — no stories or subtasks yet)

**Approval gate output:** feature list approved; skeleton epics created. Features with empty epics are ready for Phase 1 specification.

This phase is optional. If skipped, Phase 1 creates standalone epics per feature (no release grouping). Recommended for any release larger than 2–3 features.

## Phase 1 — Feature Spec

**Input:**
- Approved steering docs (Phase 0 output)
- Feature name and brief scope from user
- Optional but preferred: release epic from Phase 0.5 — if `documentation/releases/{release}/epic-map.md` has an epic for this feature, the spec attaches to that existing epic rather than creating a new one
- Upstream feature dependencies (optional)

**Output:**
- `documentation/specs/{feature-name}/requirements.md` (from `requirements-template.md`)
- `documentation/specs/{feature-name}/design.md` (from `design-template.md`)
- `documentation/specs/{feature-name}/tasks.md` (from `tasks-template.md`)
- Confluence page: feature spec under project parent (linked from the release page if applicable)
- If a release epic exists: its description is updated with a link to the spec, and `epic-map.md` Spec Status column is updated to "specced"

**Sub-gates within Phase 1:**
1. Requirements approval (before design starts)
2. Design approval (before tasks breakdown)
3. Tasks approval (before Phase 2)

## Phase 2 — Backlog

**Input:**
- Approved `documentation/specs/{feature}/tasks.md`
- JIRA project key
- Confluence URL for the spec (for back-link)
- Optional: existing release epic from Phase 0.5 (`documentation/releases/{release}/epic-map.md`)

**Output:**
- One JIRA epic — either the existing release-skeleton epic (fleshed out with full description + story/subtask children) or a new standalone epic if no release plan exists
- N JIRA stories (one per top-level requirement or task group), children of the epic
- M JIRA subtasks (one per atomic task in tasks.md), children of stories
- Ticket map file: `documentation/specs/{feature}/ticket-map.md` (task_id → JIRA key)
- If a release is active: `documentation/releases/{release}/epic-map.md` Spec Status column updated to "in backlog"
- Each ticket has:
  - Description with spec back-link
  - Estimate (from tasks.md or user input)
  - Labels (feature name, skill routing tag, release name if applicable)

## Phase 3 — Sprint Plan

**Input:**
- JIRA epic(s) to pull tickets from
- Sprint capacity (engineer-days or hours)
- Sprint length (days)
- Sprint goal (one sentence)

**Output:**
- JIRA sprint created (or ticket list if permissions don't allow)
- `documentation/sprints/sprint-{N}-kickoff.md` — markdown sprint plan document modelled on `sprint1_kickoff.md`, containing:
  - Sprint goal
  - Architecture spec links (Confluence)
  - Skill routing table
  - Execution waves (dependency order)
  - Review checklist
  - Task execution order

## Phase 4 — Execution

**Input:**
- Approved sprint plan (`documentation/sprints/sprint-{N}-kickoff.md`)
- JIRA sprint in "active" state

**Output (per ticket):**
- Code changes in the repo (delegated via engineer skill)
- A commit with conventional-commits message
- JIRA ticket transitioned to "Done"
- Implementation log comment on JIRA ticket (via Phase 5)

**Output (per sprint):**
- All scoped tickets Done or explicitly deferred
- Sprint retrospective notes appended to `documentation/sprints/sprint-{N}-kickoff.md`

## Phase 5 — Implementation Log

**Input:**
- JIRA ticket key
- Task summary
- List of files created
- List of files modified
- Code stats (lines added/removed)
- Artifacts (apiEndpoints, components, functions, classes, integrations — schema from spec-workflow-mcp)

**Output:**
- JIRA issue comment on the ticket with the structured log
- Ticket labelled `impl-logged` (or similar) for traceability

The JIRA comment format is defined in `prompts/coding/templates/jira-impl-log-template.md`.
