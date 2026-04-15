# Phase Flow — I/O Contracts

Each phase has a defined input contract (what must exist before it starts) and output contract (what it produces). This file is the reference for orchestration.

## Phase 0 — Steering

**Input:**
- A codebase directory (existing or empty)
- Optionally: user-provided product goals, known tech stack, known directory preferences

**Output:**
- `.claude/steering/product.md` (from `prompts/coding/templates/product-template.md`)
- `.claude/steering/tech.md` (from `prompts/coding/templates/tech-template.md`)
- `.claude/steering/structure.md` (from `prompts/coding/templates/structure-template.md`)
- Confluence page: "Project Steering — {project name}" with three child pages

**Approval gate output:** Three documents committed to repo and published to Confluence.

## Phase 1 — Feature Spec

**Input:**
- Approved steering docs (Phase 0 output)
- Feature name and brief scope from user (or development plan)
- Upstream feature dependencies (optional)

**Output:**
- `.claude/specs/{feature-name}/requirements.md` (from `requirements-template.md`)
- `.claude/specs/{feature-name}/design.md` (from `design-template.md`)
- `.claude/specs/{feature-name}/tasks.md` (from `tasks-template.md`)
- Confluence page: feature spec under project parent

**Sub-gates within Phase 1:**
1. Requirements approval (before design starts)
2. Design approval (before tasks breakdown)
3. Tasks approval (before Phase 2)

## Phase 2 — Backlog

**Input:**
- Approved `.claude/specs/{feature}/tasks.md`
- JIRA project key
- Confluence URL for the spec (for back-link)

**Output:**
- One JIRA epic (feature-level)
- N JIRA stories (one per top-level requirement or task group)
- M JIRA subtasks (one per atomic task in tasks.md)
- Ticket map file: `.claude/specs/{feature}/ticket-map.md` (task_id → JIRA key)
- Each ticket has:
  - Description with spec back-link
  - Estimate (from tasks.md or user input)
  - Labels (feature name, skill routing tag)

## Phase 3 — Sprint Plan

**Input:**
- JIRA epic(s) to pull tickets from
- Sprint capacity (engineer-days or hours)
- Sprint length (days)
- Sprint goal (one sentence)

**Output:**
- JIRA sprint created (or ticket list if permissions don't allow)
- `.claude/sprints/sprint-{N}-kickoff.md` — markdown sprint plan document modelled on `sprint1_kickoff.md`, containing:
  - Sprint goal
  - Architecture spec links (Confluence)
  - Skill routing table
  - Execution waves (dependency order)
  - Review checklist
  - Task execution order

## Phase 4 — Execution

**Input:**
- Approved sprint plan (`.claude/sprints/sprint-{N}-kickoff.md`)
- JIRA sprint in "active" state

**Output (per ticket):**
- Code changes in the repo (delegated via engineer skill)
- A commit with conventional-commits message
- JIRA ticket transitioned to "Done"
- Implementation log comment on JIRA ticket (via Phase 5)

**Output (per sprint):**
- All scoped tickets Done or explicitly deferred
- Sprint retrospective notes appended to `.claude/sprints/sprint-{N}-kickoff.md`

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
