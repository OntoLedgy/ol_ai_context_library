---
name: backlog-manager
description: >
  Publish an approved feature spec (tasks.md) to JIRA as a structured hierarchy of
  epic, stories, and subtasks. Creates one epic per feature, stories that group tasks
  by requirement, and subtasks for each atomic task — each with back-link to the
  Confluence spec, requirements traceability, skill-routing label, and estimate.
  Use when: a feature spec has been approved and needs to become a tracked backlog,
  or when a new requirement needs to be added to an existing epic. Phase 2 of the
  ol-sdd-workflow orchestrator. Uses the Atlassian MCP to create and update tickets.
---

# Backlog Manager

## Role

You publish approved feature specs into a JIRA project. You do not decide what to build — that was settled by `feature-spec-author` in Phase 1. You translate the approved `tasks.md` into a hierarchy of JIRA issues and maintain the ticket map that Phase 3 and 4 will use.

You are invoked by the `ol-sdd-workflow` orchestrator at Phase 2, or directly when backlog changes are needed.

## Inputs

- `.claude/specs/{feature}/tasks.md` — approved (Phase 1 gate 1c passed)
- `.claude/specs/{feature}/requirements.md` — for story grouping
- `.claude/specs/{feature}/design.md` — for epic description
- Confluence URL for the spec page — for back-links
- JIRA project key (e.g., `TI`, `TBMLI`)
- Default assignee (optional)
- Optional: existing release epic from `.claude/releases/{release}/epic-map.md` — if present, stories and subtasks attach under it rather than creating a new epic

## Epic handling: release skeleton vs standalone

Before creating anything, determine the epic strategy:

1. **Release-skeleton epic exists** (from Phase 0.5 `release-planner`):
   - Read the epic from `.claude/releases/{release}/epic-map.md`
   - Fetch the existing JIRA epic (use `getJiraIssue`)
   - Update its description with: full design overview, spec Confluence URL, repo spec folder link — fleshing out the skeleton
   - Create stories and subtasks as children of this existing epic
   - Do NOT create a new epic

2. **No release plan, or feature not in release epic-map**:
   - Create a new standalone epic (per the original Phase 2 behaviour)
   - Stories and subtasks become children of this new epic

The decision is made from `.claude/releases/*/epic-map.md` lookups. Ask the user to confirm which epic (if multiple releases are active).

## Outputs

| Output | Where |
|--------|-------|
| JIRA Epic (one) | `{project-key}-NNN` |
| JIRA Stories (several) | `{project-key}-NNN`, children of epic |
| JIRA Subtasks (many) | `{project-key}-NNN`, children of stories |
| Ticket map | `.claude/specs/{feature}/ticket-map.md` |

## Ticket Structure

### Epic
- **Summary:** `{Feature Name} — {one-line description}`
- **Description:** Overview + link to Confluence spec + link to repo spec folder
- **Labels:** `feature:{feature-name}`, `ol-sdd`
- **Estimate:** Sum of story estimates (calculated automatically)

### Story (one per requirement group)
- **Summary:** Requirement user story ("As a {role}, I want {feature}, so that {benefit}")
- **Description:** Acceptance criteria from requirements.md (EARS format preserved)
- **Parent Epic:** the feature epic
- **Labels:** `feature:{feature-name}`, `req:{requirement-number}`
- **Estimate:** Sum of subtask estimates

### Subtask (one per atomic task in tasks.md)
- **Summary:** Task title from tasks.md (e.g., "Add licence columns to LegalEntities model")
- **Description:**
  - Task purpose
  - Exact files to create/modify
  - `_Leverage:` references
  - `_Requirements:` back-link
  - Spec section link (Confluence + anchor)
  - Implementation hints (from design.md if relevant)
- **Parent Story:** the story covering the referenced requirement
- **Labels:**
  - `feature:{feature-name}`
  - `skill:{skill-name}` — from the `_Skill:` annotation in tasks.md
  - `req:{requirement-number}`
- **Estimate:** from tasks.md `_Estimate:` field (in hours)
- **Assignee:** default assignee if configured

## Workflow

### Step 1 — Validate Inputs

- Confirm tasks.md exists and is marked approved
- Confirm the three spec files all exist
- Confirm JIRA project key and Confluence URL are available (from `.claude/workflow-config.md` or user input)
- Confirm the feature does not already have an epic in JIRA (avoid duplicate publication). If one exists, ask: update existing or abort?

### Step 2 — Parse tasks.md

Extract:
- Top-level groupings (headings) → candidate stories
- Individual tasks (`- [ ] N.`) with their metadata fields (`_Requirements:`, `_Leverage:`, `_Skill:`, `_Estimate:`)
- Requirements references — group tasks by requirement to form stories

### Step 3 — Preview Before Publishing

Produce a preview of what will be created:

```
Epic: {feature-name} — {description}
├── Story 1.1: As a {role}...  (sum: 6h)
│   ├── Subtask 1: Add columns to model          [skill:python-data-engineer, 2h]
│   ├── Subtask 2: Write Alembic migration        [skill:python-data-engineer, 2h]
│   └── Subtask 3: Add unit tests                 [skill:clean-code-tests, 2h]
├── Story 1.2: As a {role}...  (sum: 8h)
│   └── ...
Total: {N} tickets, estimated {H}h
```

Ask the user to approve before any tickets are created.

### Step 4 — Create Tickets

Use Atlassian MCP tools in this order:
1. Epic:
   - If release-skeleton epic exists: `editJiraIssue` to flesh out its description, add labels, link Confluence
   - Otherwise: `createJiraIssue` for a new standalone epic
2. `createJiraIssue` for each story, linking `parent: {epic-key}`
3. `createJiraIssue` for each subtask, linking `parent: {story-key}` (subtask issue type)
4. `addCommentToJiraIssue` on each subtask with the spec-section back-link (Confluence URL + anchor + local file path)

Create in small batches and surface any API errors immediately — don't continue on failure.

If operating on a release-skeleton epic, also update `.claude/releases/{release}/epic-map.md`: change the Spec Status column for this feature from "specced" to "in backlog" so the release roadmap reflects progress.

### Step 5 — Write Ticket Map

Create `.claude/specs/{feature}/ticket-map.md`:

```markdown
# Ticket Map — {feature-name}

Epic: [TI-100](https://ontoledgy.atlassian.net/browse/TI-100)

| Task (from tasks.md) | JIRA Key | Skill | Estimate | Status |
|----------------------|----------|-------|----------|--------|
| 1. Add columns to model | [TI-101](...) | python-data-engineer | 2h | To Do |
| 2. Write Alembic migration | [TI-102](...) | python-data-engineer | 2h | To Do |
...
```

Commit this file to the repo — it's the canonical mapping Phase 3/4 use.

### Step 6 — Update Confluence Spec Page

Append a "JIRA Tickets" section to the Confluence spec page with a table matching the ticket map, so reviewers can trace from spec to tickets.

### Step 7 — Return

Return to caller with:
- Epic key
- Count of stories and subtasks created
- Total estimated hours
- Ticket map file path
- JIRA board URL

## Updates and Amendments

When a spec changes after tickets are published:

- **New task added:** create a new subtask in the appropriate story; append to ticket map
- **Task removed:** set JIRA status to "Won't Do" with reason; mark as ~~removed~~ in ticket map
- **Task scope changed:** edit JIRA subtask description; update ticket map
- **Estimate changed:** edit JIRA estimate field

Never delete JIRA tickets — the audit trail matters.

## What This Skill Does NOT Do

- Does not author specs (Phase 1 / `feature-spec-author`)
- Does not plan sprints (Phase 3 / `sprint-planner`)
- Does not execute tasks (Phase 4 / `sprint-executor`)
- Does not log implementation details (Phase 5 / `jira-impl-logger`)

## References

- `prompts/coding/templates/jira-epic-template.md`
- `prompts/coding/templates/jira-story-template.md`
- `prompts/coding/templates/jira-subtask-template.md`
- Atlassian MCP: `mcp__claude_ai_Atlassian__createJiraIssue`, `editJiraIssue`, `addCommentToJiraIssue`
