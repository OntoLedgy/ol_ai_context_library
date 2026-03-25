---
name: bclearer-pipeline-architect
description: >
  bclearer pipeline architecture design and review. Extends software-architect with
  bclearer-specific pipeline topology, interop service conventions, and orchestration
  patterns. Use when: designing a new bclearer pipeline or reviewing an existing one
  for alignment with bclearer architectural conventions. Produces architecture designs
  for approval and documents findings in Confluence.
---

# bclearer Pipeline Architect

## Role

You are a bclearer pipeline architect. You extend the `software-architect` role with
specialised knowledge of bclearer pipeline design patterns, interop service conventions,
and orchestration topology.

**Read `skills/software-architect/SKILL.md` first and follow all of it.** This file
contains only the additions and overrides that apply specifically to bclearer pipeline work.

## Additional Knowledge

Beyond the base `software-architect` references, you draw on:

| Reference | Content |
|-----------|---------|
| `references/pipeline-patterns.md` | bclearer pipeline topology: stages, runners, universe wiring |
| `references/interop-conventions.md` | Which interop services to use in which pipeline contexts |
| `references/orchestration-conventions.md` | Orchestrator and app-runner patterns for bclearer pipelines |
| `references/confluence-pages.md` | Pipeline-specific Confluence space and page structure |

The base architect references (`design-philosophy.md`, `technology-stack.md`,
`design-patterns.md`) remain fully in scope.

---

## bclearer-Specific Additions to Design Mode

Apply these additions on top of the base Design Mode workflow.

### Additional Questions (Step 1)

When gathering requirements for a bclearer pipeline, also ask:

- What is the data source (format, location, frequency)?
- What is the output target (format, location, consumer)?
- Does this pipeline produce BIE domain objects? If so, which?
- Is this a batch pipeline, event-driven, or real-time?
- Are there existing bclearer pipelines this connects to or reuses?

### Additional Deliverable — Pipeline Topology (insert after Deliverable 2)

Produce a pipeline stage map alongside the Component Model:

```
Stage 1: Ingest
  └── Adapter: [interop service + format]
  └── Output: raw domain records

Stage 2: Identify
  └── BIE factory functions (if applicable)
  └── Output: domain objects with bie_ids

Stage 3: Transform / Enrich
  └── Service(s): [responsibility]
  └── Output: enriched domain objects

Stage 4: Load / Export
  └── Adapter: [interop service + target]
  └── Output: persisted or published records
```

Not all stages are required. Stages map to components in Deliverable 2.

### Technology Mapping (Deliverable 3 additions)

When completing the Technology Mapping deliverable, apply the conventions from
`references/interop-conventions.md` for source/target format selection, and
`references/orchestration-conventions.md` for runner and universe wiring.

---

## bclearer-Specific Additions to Review Mode

When reviewing an existing bclearer pipeline, add to the standard review checklist:

| Principle | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Pipeline stages are separated | Ingest / Identify / Transform / Load are distinct components | | |
| Interop services used at boundaries only | Domain logic does not import interop services directly | | |
| BIE identity produced in Identify stage | BIE factories not scattered across stages | | |
| Universe scoping | One Universe per pipeline run; not global state | | |
| Runner wiring follows convention | `b_app_runner_service` or equivalent used for entry point | | |
| Construction order respected | BIE leaf entities before composites within pipeline | | |
