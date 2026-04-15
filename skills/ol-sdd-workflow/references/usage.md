# Usage Guide — ol-sdd-workflow

How to invoke the workflow and the skills it orchestrates, from first-time project setup through sprint execution.

## Quick start (end-to-end, new project)

```
You: "use ol-sdd-workflow to take this project end to end — we want to ship Feature X in the next sprint"
```

The orchestrator will walk through:
1. Phase 0 — steering docs (product, tech, structure)
2. Phase 0.5 — release plan (feature list, Confluence roadmap, empty JIRA epics)
3. Phase 1 — feature spec for each in-scope feature (requirements → design → tasks)
4. Phase 2 — JIRA backlog (stories + subtasks added under the release epic)
5. Phase 3 — sprint plan
6. Phase 4 — sprint execution (with Phase 5 impl logs per task)

At each phase gate it will pause and ask for approval.

## Invoking by phase

You don't have to start at Phase 0. Jump in wherever you are.

| Situation | Say |
|-----------|-----|
| New project, no steering yet | "use product-vision-steering to set up steering docs for this project" |
| Steering exists, scoping an MVP or release | "use release-planner to plan the MVP / release {name}" |
| Release plan exists, need to spec a feature | "use feature-spec-author to spec out feature {name}" (attaches to its release epic) |
| Steering exists, one-off feature (no release grouping) | "use feature-spec-author to spec feature {name}" (creates standalone epic) |
| Spec approved, need stories and subtasks | "use backlog-manager to publish `.claude/specs/{feature}/` to JIRA" |
| Backlog exists, planning next sprint | "use sprint-planner to plan sprint {N} with {H} hours of capacity" |
| Sprint planned, ready to execute | "use sprint-executor to run sprint {N}" |
| Task committed, need to log it | "use jira-impl-logger to log {TICKET-KEY} implementation" |

## Resuming mid-workflow

```
You: "use ol-sdd-workflow — where are we?"
```

The orchestrator reads `.claude/steering/`, `.claude/specs/`, active JIRA sprints, and in-flight tickets, then summarises state and proposes the next action. You can approve or redirect.

## Prerequisites

Before you can run the workflow end-to-end you need:

- **Atlassian MCP configured** — the skill creates/reads JIRA issues and Confluence pages via `mcp__claude_ai_Atlassian__*` tools. Without it, backlog-manager and jira-impl-logger cannot publish.
- **A JIRA project** with epic → story → subtask hierarchy enabled, and a board with sprints
- **A Confluence space** with a project parent page (for steering and spec documents)
- Optional: a `.claude/workflow-config.md` at repo root with:
  ```markdown
  confluence_space: TBMLI
  confluence_parent_page: 6500000000
  jira_project: TI
  jira_board: 100
  default_assignee: khanm@ontoledgy.io
  sprint_length_days: 10
  ```
  If absent, the skills will ask for these values on first run.

## Repo layout the workflow creates

```
your-repo/
├── .claude/
│   ├── workflow-config.md              (JIRA/Confluence config; Phase 0)
│   ├── steering/
│   │   ├── product.md                  (Phase 0)
│   │   ├── tech.md                     (Phase 0)
│   │   └── structure.md                (Phase 0)
│   ├── releases/
│   │   └── {release-name}/
│   │       ├── features.md             (Phase 0.5; prioritised feature list)
│   │       └── epic-map.md             (Phase 0.5; feature → JIRA epic mapping)
│   ├── specs/
│   │   └── {feature-name}/
│   │       ├── requirements.md         (Phase 1, gate 1a)
│   │       ├── design.md               (Phase 1, gate 1b)
│   │       ├── tasks.md                (Phase 1, gate 1c)
│   │       └── ticket-map.md           (Phase 2; task_id → JIRA key)
│   └── sprints/
│       └── sprint-{N}-kickoff.md       (Phase 3)
└── (your code)
```

Implementation logs (Phase 5) do **not** go in the repo — they are comments on JIRA issues.

## Approval gates — what to expect

At every gate the orchestrator will:
1. Show you the deliverable (file contents, JIRA preview, sprint plan)
2. Ask explicitly: *"approve to proceed to Phase {N+1}, or tell me what to change"*
3. Wait. It does not advance on silence or ambiguous replies.

Acceptable approvals: `approve`, `yes proceed`, `looks good`, `go`.

On rejection with feedback, the orchestrator re-invokes the current phase's skill with your feedback, then re-presents.

## Delegation: who actually writes the code

In Phase 4, `sprint-executor` is the tech lead. For each JIRA subtask it reads the `skill:{name}` label and delegates to that engineer skill (or to Codex via the `mcp__codex__codex` MCP, if your environment uses Codex as the implementation engine).

Routing table: see [skills/feature-spec-author/references/skill-routing.md](../../feature-spec-author/references/skill-routing.md).

After the engineer skill returns, `sprint-executor` reviews via `clean-code-reviewer`, commits with conventional-commits format (via `clean-code-commit`), transitions the JIRA ticket, and invokes `jira-impl-logger` to post the impl log — all before moving to the next ticket.

## Implementation logs — format and why JIRA

Each completed task gets a structured comment on its JIRA subtask containing:
- Files created / modified and line stats
- Structured artifacts: `apiEndpoints`, `components`, `functions`, `classes`, `integrations`, `dataModels`, `pipelineStages`
- Searchable keywords (for future AI agents grepping JIRA before writing new code)
- Back-links to spec, commit, related tickets

Template: [prompts/coding/templates/jira-impl-log-template.md](../../../prompts/coding/templates/jira-impl-log-template.md).

We chose JIRA comments over repo files because:
- JIRA is already the work-done system of record; repo logs duplicate git log
- JIRA is searchable via `mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql`
- Comments naturally link to the ticket's full context (description, review, sprint)
- Repo log files tend to decay and rot

## Replanning mid-sprint

```
You: "we have a blocker on TI-102, replan the rest of the sprint"
```

This re-invokes `sprint-planner` in replan mode. It reads current sprint state (done, in-flight, remaining), you describe the trigger (blocker, new priority, capacity change), and it proposes changes. On approval it updates JIRA and appends a "Replan {date}" addendum to the kickoff doc — history is preserved, never rewritten.

## Adding tasks to an in-flight feature

If a new task surfaces during execution:

1. Add it to `.claude/specs/{feature}/tasks.md` with full metadata (`_Requirements:`, `_Leverage:`, `_Skill:`, `_Estimate:`)
2. Re-invoke `backlog-manager` with "add new task to existing epic {KEY}"
3. It creates a new subtask and appends to `ticket-map.md` — existing tickets are unchanged
4. Decide whether the new task goes in this sprint (re-invoke `sprint-planner` replan) or the backlog

Never delete JIRA tickets — use "Won't Do" status with a reason.

## Not using all phases?

Every phase skill is independently callable. Common partial uses:

- **Steering-only**: `product-vision-steering` alone to document an existing codebase
- **Release-planning-only**: `release-planner` alone to enumerate and prioritise features for stakeholder review (produces Confluence roadmap + skeleton epics without forcing spec work)
- **Spec-only**: `feature-spec-author` to produce spec docs without JIRA publishing (useful for exploratory specs)
- **JIRA-only**: `backlog-manager` to publish an externally-authored tasks.md to JIRA
- **Exec-only**: `sprint-executor` against an existing JIRA sprint, without going through planning (useful when someone else planned the sprint)
- **Log-only**: `jira-impl-logger` to backfill impl logs on already-done tickets

The master `ol-sdd-workflow` skill is only needed when you want gated end-to-end orchestration.

## When NOT to use this workflow

- One-liner bug fixes — too much overhead. Use a direct engineer skill and `clean-code-commit`.
- Exploratory spikes / R&D — specs constrain; spikes need freedom. Do the spike first, then write a feature spec if you keep any of it.
- Already-agreed work without external stakeholders — if the team knows the scope and trusts each other, you may not need Confluence/JIRA overhead. Use just the engineer skills.

## Further reading

- [SKILL.md](../SKILL.md) — the orchestrator behaviour spec
- [phase-flow.md](phase-flow.md) — I/O contracts for each phase
- [workflow-state.md](workflow-state.md) — how state is detected for resumption
- [skills/feature-spec-author/references/skill-routing.md](../../feature-spec-author/references/skill-routing.md) — engineer-skill routing table
- Upstream inspiration: https://github.com/Pimzino/spec-workflow-mcp
