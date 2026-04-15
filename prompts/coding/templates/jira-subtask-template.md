# JIRA Subtask Template

One subtask per atomic task in `tasks.md`. This is the unit an engineer skill implements in Phase 4.

## Summary
Task title from tasks.md (concise, action-first).

Example: `Add licence columns to LegalEntities model`

## Issue Type
Subtask (child of a Story)

## Parent
The story covering the referenced requirement.

## Description

```
## Purpose
{one-line purpose from tasks.md}

## Files
**Create:**
- `{exact path}` — {what it will contain}

**Modify:**
- `{exact path}` — {what to change}

## Implementation Hints
(from the linked design.md section — pulled by backlog-manager)

## Leverage (existing code to reuse)
- `{path}` — {what to reuse from it}
- `{path}`

## Requirements Covered
- {requirement ID(s), e.g. 1.1, 1.2}

## Spec Reference
- Feature spec: [Confluence link]
- tasks.md: `documentation/specs/{feature-name}/tasks.md` — task #{N}
- design.md section: [Confluence anchor link]

## Acceptance
- [ ] Files match the spec
- [ ] Language syntax check passes
- [ ] New or existing tests still pass
- [ ] Passes clean-code-reviewer
```

## Labels
- `feature:{feature-name}`
- `skill:{skill-name}` — e.g., `skill:python-data-engineer`, `skill:ui-engineer`
- `req:{requirement-number}`
- Optional: `wave:{wave-number}` (added by sprint-planner)

## Estimate
Hours, from tasks.md `_Estimate:` field.

## Assignee
Default assignee from workflow-config, or unassigned.

## Status Workflow
`To Do → In Progress → In Review → Done`
(Or `To Do → In Progress → Done` if team doesn't use In Review)
