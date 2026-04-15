# JIRA Epic Template

Fields to populate when creating an epic from a feature spec.

## Summary
`{Feature Name} — {one-line description}`

Example: `Licence Data Extraction Pipeline — extract licence fields from uploaded documents into LegalEntities`

## Issue Type
Epic

## Description (ADF / markdown)

```
## Overview
{2–3 sentences: what the feature does, who it's for, why now}

## Spec
- Confluence: {spec page URL}
- Repo: `documentation/specs/{feature-name}/`
- Design: [design.md]({url-or-path})
- Requirements: [requirements.md]({url-or-path})
- Tasks: [tasks.md]({url-or-path})

## Scope
In scope:
- {item}

Out of scope:
- {item}

## Upstream Dependencies
- {other feature/epic/system, if any}

## Downstream Consumers
- {what this unlocks}

## Success Criteria
- {measurable outcome 1}
- {measurable outcome 2}
```

## Labels
- `feature:{feature-name}` (kebab-case)
- `ol-sdd`
- Optionally: `phase:{phase-number}` if part of a roadmap

## Estimate
Sum of child story estimates. Updated automatically as stories are created.

## Priority
Set by user at sprint planning time. Default: Medium.

## Assignee
Feature lead (typically the architect who authored the spec), or leave unassigned for team pickup.

## Custom Fields (if configured)
- **Epic Name:** short label (e.g., "Licence Extraction")
- **Epic Colour:** team convention
