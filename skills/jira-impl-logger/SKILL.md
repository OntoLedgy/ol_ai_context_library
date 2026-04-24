---
name: jira-impl-logger
description: >
  Post a structured implementation log as a comment on a JIRA issue after a task
  is completed. Captures files created/modified, code statistics, and structured
  artifacts (API endpoints, components, functions, classes, integrations) so that
  future engineers and AI agents can discover existing code and avoid duplication.
  Adapted from the spec-workflow-mcp log-implementation schema but publishes to
  JIRA comments rather than repo files. Use when: a task has been committed and
  the implementation needs to be recorded. Phase 5 of the ol-sdd-workflow
  orchestrator. Invoked once per completed task by sprint-executor.
---

# JIRA Implementation Logger

## Role

You record what was implemented for a task as a structured comment on the JIRA issue. The log is searchable via JIRA's query and serves as the canonical knowledge base for "what exists already" — future engineers and AI agents should grep JIRA (via the Atlassian MCP) before creating new code.

You are invoked by `sprint-executor` once per completed task, or directly if someone needs to backfill a log.

**Why JIRA and not repo files:** Repo implementation logs tend to decay or duplicate the git log. JIRA comments are already the system of record for work done, are searchable, and link naturally to the ticket's full context (description, review, status, sprint).

## Inputs

- **Ticket key** (e.g., `TI-101`)
- **Summary** — one-line description of what was implemented
- **Files created** — list of paths
- **Files modified** — list of paths
- **Statistics** — linesAdded, linesRemoved (from `git diff --shortstat`)
- **Artifacts** — structured data about what was built (see schema below)
- **Commit hash(es)** — for back-reference

## Artifact Schema

Structured data, adapted from spec-workflow-mcp. Each artifact type is optional — include the ones relevant to this task.

### apiEndpoints
```
method: GET | POST | PUT | DELETE | PATCH
path: "/api/specs/:name/logs"
purpose: "What this endpoint does"
requestFormat: "Query params or body schema"
responseFormat: "Response structure"
location: "file:line"
```

### components
```
name: "LogsPage"
type: "React" | "Vue" | "Svelte" | ...
purpose: "What the component does"
location: "file path"
props: "Props interface"
exports: ["name1", "name2"]
```

### functions
```
name: "searchLogs"
purpose: "What it does"
location: "file:line"
signature: "(term: string) => Promise<LogEntry[]>"
isExported: true
```

### classes
```
name: "ImplementationLogManager"
purpose: "What the class does"
location: "file path"
methods: ["method1", "method2"]
isExported: true
```

### integrations
```
description: "LogsPage fetches via REST and subscribes to WebSocket"
frontendComponent: "LogsPage"
backendEndpoint: "GET /api/specs/:name/logs"
dataFlow: "mount → fetch → display → subscribe → realtime update"
```

### dataModels
```
name: "LegalEntity"
kind: "SQLAlchemy model" | "Pydantic schema" | "TypeScript interface"
location: "file:line"
fields: ["id: int", "name: str", ...]
migrations: ["alembic/versions/xxx_add_licence_columns.py"]
```

### pipelineStages
```
name: "web_search"
position: 3
purpose: "Search the web for presence info"
inputs: ["entity_id"]
outputs: ["web_search_results"]
location: "file path"
```

## Workflow

### Step 1 — Validate Inputs

- Confirm ticket exists (Atlassian MCP `getJiraIssue`)
- Confirm at least one artifact category is provided — empty artifacts is a failure mode
- Confirm files lists are non-empty (a task that created/modified no files is suspicious)

If inputs are thin, ask the caller for more detail before posting. A sparse log is worse than no log — it pollutes search results.

### Step 2 — Render the Comment

Use the template at `prompts/coding/templates/jira-impl-log-template.md`. Structure:

```markdown
## Implementation Log — {ticket-key}

**Summary:** {one-line summary}
**Commit:** {hash} — {commit message first line}
**Date:** {ISO date}

### Files
- Created: {file1}, {file2}
- Modified: {file3}, {file4}
- Stats: +{linesAdded} / -{linesRemoved} across {N} files

### Artifacts

#### API Endpoints
| Method | Path | Purpose | Location |
| ... | ... | ... | ... |

#### Components
| Name | Type | Purpose | Location | Props |

#### Functions
| Name | Purpose | Location | Signature | Exported |

#### Classes
| Name | Purpose | Location | Methods | Exported |

#### Integrations
| Description | Frontend | Backend | Data flow |

#### Data Models
...

#### Pipeline Stages
...

### Searchable Keywords
{comma-separated list of class/function/endpoint names for JIRA full-text search}
```

### Step 3 — Post Comment

Use `mcp__claude_ai_Atlassian__addCommentToJiraIssue` with the rendered markdown.

### Step 4 — Label Ticket

Add label `impl-logged` to the ticket via `editJiraIssue`. This lets dashboards filter tickets that have logs vs. those still missing them.

### Step 5 — Return

Return to caller:
- JIRA comment URL
- Confirmation that ticket is labelled

## Why Structured Artifacts Matter

Future AI agents will query the JIRA comments via the Atlassian MCP (`searchJiraIssuesUsingJql` with text search) before writing new code. Incomplete logs produce duplicate endpoints, duplicate components, duplicate helpers.

Minimum quality bar:
- If the task created an API endpoint, `apiEndpoints` MUST be populated
- If the task created a UI component, `components` MUST be populated
- If the task created a class, `classes` MUST be populated
- A pure refactor (no new API surface) may have empty artifacts but MUST explain in summary: "Refactor only — no new public surface"

## Backfilling Logs

If invoked on a closed ticket that never got a log:
1. Read the ticket description and commits referenced
2. `git log --follow` and `git show` to identify files and stats
3. Infer artifacts from the diff (grep for `def `, `class `, `@app.route`, React component exports)
4. Offer the draft log to the user for confirmation before posting

## What This Skill Does NOT Do

- Does not evaluate code quality (that's `clean-code-reviewer`)
- Does not close the JIRA ticket (that's `sprint-executor`)
- Does not write logs to the repo (deliberately — JIRA is the log surface)
- Does not add commits or run tests

## References

- `prompts/coding/templates/jira-impl-log-template.md`
- Atlassian MCP: `addCommentToJiraIssue`, `editJiraIssue`, `getJiraIssue`
- Origin schema: https://github.com/Pimzino/spec-workflow-mcp `log-implementation` tool


---

## Feedback

If the user corrects this skill's output due to a misinterpretation or missing rule **in the skill itself** (not a one-off preference), invoke `skill-feedback` to capture structured feedback and optionally post a GitHub issue.

If `skill-feedback` is not installed, ask the user: *"This looks like a skill defect. Would you like to install the `skill-feedback` skill to report it?"* If the user declines, continue without feedback capture.
