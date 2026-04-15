# Workflow State Detection

When invoked without explicit phase direction, infer the current phase by probing these surfaces in order.

## State probes

```
probe 0: .claude/steering/product.md + tech.md + structure.md
  present & non-empty  → steering complete
  missing/empty        → Phase 0 required

probe 0.5: .claude/releases/{release}/epic-map.md
  present                    → release plan in place; read epic-map to identify
                               candidate features and their spec status
  absent and user is scoping → Phase 0.5 required (MVP, v1, roadmap language)
  absent and single-feature  → Phase 0.5 skippable; proceed to Phase 1 directly
    work                     

probe 1: .claude/specs/{feature}/ directory
  with requirements.md only              → Phase 1 mid, gate 1
  with requirements.md + design.md       → Phase 1 mid, gate 2
  with all three (incl. tasks.md)        → Phase 1 complete, ready for Phase 2
  absent                                  → Phase 1 not started

probe 2: JIRA epic state for target feature
  release-skeleton epic (no children)       → Phase 0.5 done, Phase 2 not yet
  epic with stories and subtasks            → Phase 2 complete
  no epic at all                             → neither Phase 0.5 nor Phase 2 done

probe 3: JIRA sprint containing epic's subtasks
  absent                 → Phase 3 required
  present, state=future  → Phase 3 complete, awaiting start
  present, state=active  → Phase 4 in progress

probe 4: tickets in sprint with status transitions
  all To-Do              → Phase 4 not started
  mixed                  → Phase 4 in progress
  all Done (or deferred) → Sprint complete
```

## Multi-feature state

A project can have several features in flight simultaneously. When multiple `.claude/specs/*/` exist:

1. List all feature folders
2. For each, report phase (use probe sequence above)
3. Ask the user which feature to operate on

## Configuration file

If `.claude/workflow-config.md` exists, read it for project-level config:

```markdown
# Workflow Config

confluence_space: TBMLI
confluence_parent_page: 6500000000
jira_project: TI
jira_board: 100
default_assignee: khanm@ontoledgy.io
sprint_length_days: 10
```

These values flow into the downstream skill invocations so the user isn't asked repeatedly.

## Unknown state

If probes return inconsistent results (e.g., JIRA epic exists but no `.claude/specs/`), flag to the user:

> "I see a JIRA epic {KEY} for {feature} but no spec folder in the repo. Did the spec live elsewhere, or should we reverse-engineer one from the epic description?"

Do not assume; ask.
