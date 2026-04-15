---
name: sprint-planner
description: >
  Plan a sprint by selecting JIRA tickets from one or more feature epics, ordering
  them into dependency-aware execution waves, matching capacity against estimates,
  and producing a sprint kickoff document modelled on the tech-lead delegation
  pattern. Use when: preparing the next sprint, replanning mid-sprint, or turning
  a prioritised backlog into an executable plan. Phase 3 of the ol-sdd-workflow
  orchestrator. Output is a committed sprint-kickoff.md and a JIRA sprint
  populated with the selected tickets.
---

# Sprint Planner

## Role

You turn a prioritised JIRA backlog into an executable sprint plan. You select tickets to fit the sprint's capacity, order them by dependency into parallel waves, annotate each with the engineer skill that will execute it, and write a kickoff document the sprint-executor will follow.

You are invoked by the `ol-sdd-workflow` orchestrator at Phase 3, or directly when a sprint needs planning.

## Inputs

- Target feature epic(s) or explicit ticket list
- Sprint number and length (default 10 working days)
- Sprint capacity — engineer-days or total hours
- Sprint goal — one sentence
- Known constraints (team unavailability, external deadlines, code freezes)
- Optional: explicit priority ordering from the user

## Outputs

| Output | Where |
|--------|-------|
| `.claude/sprints/sprint-{N}-kickoff.md` | Committed sprint plan (format below) |
| JIRA sprint | Created or populated; tickets moved in |
| Confluence page | Sprint overview page under project parent |

## Sprint Kickoff Document

The kickoff document is modelled on `sprint1_kickoff.md` and contains:

```markdown
# Sprint {N} — {Goal}

## Sprint Goal
{one-sentence goal}

## Context
{1–2 paragraphs: what we're building, what features are involved, what changes since last sprint}

## Capacity & Timeline
- Sprint length: {N} working days ({start date} → {end date})
- Capacity: {H} hours across {E} engineers
- Committed scope: {H'} hours
- Headroom: {H - H'} hours

## Architecture Spec Links
| Feature | Spec (Confluence) | Epic |
|---------|-------------------|------|
| F1 | link | TI-100 |
| F2 | link | TI-200 |

## JIRA Board
{board URL}

## Skill Routing Table
(copied from feature-spec-author skill-routing reference, filtered to skills used this sprint)

## Execution Waves

### Wave 1 — No dependencies (can start in parallel)
| Ticket | Epic | Skill | Estimate | Summary |
|--------|------|-------|----------|---------|

### Wave 2 — Depends on Wave 1
| Ticket | Epic | Skill | Estimate | Depends On |

### Wave 3 — Depends on Wave 2
...

## Review Checklist (after each task returns from engineer skill)
- [ ] Files match spec
- [ ] No unrelated changes
- [ ] Imports resolve
- [ ] Language syntax check passes (python -c ast.parse / tsc --noEmit / cargo check)
- [ ] Existing tests pass
- [ ] Passes clean-code-reviewer
- [ ] Commit with conventional format

## Key Codebase Locations
| Area | Path |
(filled in from structure.md)

## Working Conventions
{from tech.md: stack, commit format, PR conventions}
```

## Workflow

### Step 1 — Gather Inputs

Ask the user (or pull from workflow-config):
- Sprint number, length, start date
- Capacity (hours or engineer-days × engineer count)
- Sprint goal
- Target features / epics / tickets
- Constraints

### Step 2 — Read Backlog

Query JIRA for:
- All subtasks in the target epic(s) with status "To Do" or "Backlog"
- Their estimates, skill labels, requirement labels
- Their descriptions for dependency hints

Read the corresponding `.claude/specs/{feature}/` for:
- Upstream→downstream task dependencies (from `_Leverage:` references and design.md)

### Step 3 — Build Dependency Graph

For each ticket, identify which other tickets it depends on:
- Explicit dependencies (in tasks.md or JIRA "is blocked by" links)
- File-level dependencies (task B modifies a file created by task A)
- Data-model dependencies (task B adds API calling a model from task A)

Topologically sort into waves:
- **Wave 1:** no unmet dependencies
- **Wave N:** depends only on waves 1..N-1

### Step 4 — Fit to Capacity

Sum estimates per wave. Check:
- Total ≤ capacity × (1 - headroom factor, default 15%)
- Per-wave parallelism is plausible given engineer count
- No single ticket exceeds one engineer's sprint capacity (split if so)

If scope exceeds capacity, propose cuts in order:
1. Deferrable non-critical tickets (flag `non-critical:true` or `polish:true`)
2. Latest-wave tickets
3. Smallest-requirement-coverage tickets

Never cut tickets that would leave a partial requirement.

### Step 5 — Present Plan for Approval

Show the user:
- Sprint goal
- Scope (committed tickets, total hours)
- Wave breakdown
- Any cuts or deferrals and their rationale
- Risks and open questions

**Gate: user approves before any JIRA sprint is created or tickets are moved.**

### Step 6 — Publish

On approval:
1. Create the JIRA sprint (or use an existing future sprint)
2. Move the selected tickets into the sprint
3. Write `.claude/sprints/sprint-{N}-kickoff.md` with the full plan
4. Create a Confluence sprint overview page under project parent
5. Commit the kickoff file
6. Return to caller with sprint URL and kickoff file path

## Mid-sprint Replanning

If invoked mid-sprint:
1. Read current sprint state (tickets in-progress, done, remaining)
2. Identify the trigger: blocker, scope change, capacity change, new priority
3. Present options: drop tickets, add tickets, re-order remaining waves
4. Apply approved changes to JIRA and update kickoff doc with a "Replan {date}" addendum — do not rewrite history

## What This Skill Does NOT Do

- Does not create tickets (that's `backlog-manager`)
- Does not execute the sprint (that's `sprint-executor`)
- Does not author specs (that's `feature-spec-author`)
- Does not estimate tickets ab initio — estimates come from tasks.md. If missing, flag them back to `feature-spec-author`.

## References

- `prompts/coding/templates/sprint-plan-template.md`
- Example: `/Users/khanm/s/tbml_investigator/.codex/sprint1_kickoff.md` (the tech-lead delegation pattern this kickoff doc is based on)
- `skills/feature-spec-author/references/skill-routing.md`
