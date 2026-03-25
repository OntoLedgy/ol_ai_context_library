# Confluence Pages Reference — bclearer Pipeline Architect

Cloud ID: `c62e56c2-b224-4d4e-a859-afa7de01241e`

> **Status: Skeleton** — pipeline-specific Confluence page IDs to be confirmed. The base architecture pages from `software-architect/references/confluence-pages.md` remain in scope.

---

## Inherited Pages (from software-architect)

Always fetch these for architectural context:

| Page | Page ID | When to Fetch |
|------|---------|--------------|
| Table of Contents | `6471319553` | Always — system overview |
| Foundation Model | `6472269834` | When BIE patterns are in scope |
| Domain Model General | `6471680023` | When domain components are in scope |

---

## Pipeline-Specific Pages

> Populate page IDs once the pipeline architecture space is established in Confluence.

| Page | Page ID | When to Fetch |
|------|---------|--------------|
| bclearer Pipeline Overview | `TBD` | Always in pipeline design/review mode |
| Pipeline Stage Conventions | `TBD` | When designing stage topology |
| Interop Service Usage Guide | `TBD` | When selecting adapters |
| Orchestration Patterns | `TBD` | When designing runner and wiring |

---

## Target Page Hierarchy for New Designs

```
Architecture
└── bclearer Pipelines
    └── Pipeline Designs
        └── [Pipeline Name] — Design vN
    └── Pipeline Reviews
        └── [Pipeline Name] — Review vN
```

---

## Page Creation

Use the same `mcp__atlassian__createConfluencePage` approach as `software-architect/references/confluence-pages.md`. Title format:

- Design: `[Pipeline Name] — Pipeline Architecture Design v[N]`
- Review: `[Pipeline Name] — Pipeline Architecture Review v[N]`

Labels: `architecture`, `pipeline`, `bclearer`, and the pipeline name (snake_case).
