# JIRA Story Template

A story groups related subtasks that together fulfil one requirement from `requirements.md`.

## Summary
Use the user-story form from the requirement:
`As a {role}, I want {feature}, so that {benefit}`

Example: `As an investigator, I want licence data extracted from uploaded documents so that I can verify entity regulation status without manual entry`

## Issue Type
Story

## Parent
The feature epic (e.g., `TI-100`)

## Description

```
## Acceptance Criteria
(copied from requirements.md, EARS format preserved)

1. WHEN {event} THEN the system SHALL {response}
2. IF {precondition} THEN the system SHALL {response}
3. WHEN {event} AND {condition} THEN the system SHALL {response}

## Spec Reference
- Requirement ID: {e.g. 1.1}
- Spec section: [Confluence link with anchor]

## Subtasks
- [ ] {subtask summary 1} — {JIRA key when created}
- [ ] {subtask summary 2} — {JIRA key when created}
```

## Labels
- `feature:{feature-name}`
- `req:{requirement-number}` (e.g., `req:1.1`)

## Estimate
Sum of child subtask estimates (hours).

## Priority
Inherit from epic unless user overrides.
