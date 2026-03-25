# BIE Integration Reference

This reference defines when and how the `bclearer-pipeline-engineer` delegates to
`bie-component-ontologist` and `bie-data-engineer` for BIE domain work within a pipeline.

---

## When to Delegate

| Situation | Delegate To |
|-----------|------------|
| Pipeline requires domain objects with stable BIE IDs and no component model exists | `bie-component-ontologist` → get approved model → then `bie-data-engineer` |
| Approved BIE component model exists; need Python implementation | `bie-data-engineer` |
| Reviewing existing BIE domain code within a pipeline | `bie-component-ontologist` (review mode) |
| General pipeline stage code (adapters, services, orchestrators) | Handle directly as `bclearer-pipeline-engineer` |

**Rule of thumb:** If the task involves `BieDomainObjects`, `CommonIdentityVector`,
three-tier creator functions, or BIE factory functions — delegate to `bie-data-engineer`.
Everything else (adapters, services, orchestrators, runner wiring) stays in scope.

---

## Boundary Within a Pipeline

```
Pipeline package
│
├── bie/                   ← bie-data-engineer owns this folder
│   ├── common_knowledge/  (domain types enum)
│   ├── bie_id_creators/   (identity vectors, creator functions)
│   └── objects/           (domain object classes, factories, universe)
│
├── adapters/              ← bclearer-pipeline-engineer owns these
├── services/              ← bclearer-pipeline-engineer owns these
├── orchestrators/         ← bclearer-pipeline-engineer owns these
└── runners/               ← bclearer-pipeline-engineer owns these
```

---

## Handoff Protocol

### When handing off to bie-data-engineer

Provide:
1. The approved BIE component ontology (4 deliverables — from `bie-component-ontologist`)
2. The target package path (`bie/` folder within the pipeline package)
3. Any existing code in that folder to avoid conflicts

### When receiving output from bie-data-engineer

After `bie-data-engineer` completes:
1. Read the factory function signatures (they define what the pipeline's Identify stage calls)
2. Read the Universe class (it defines what registries are available to other stages)
3. Wire these into the Identify orchestrator and pipeline universe

---

## Identity Flow Through Pipeline Stages

```
Stage 1 (Ingest)
  └── produces: raw data (no BIE IDs)

Stage 2 (Identify) ← bie-data-engineer's factories are called here
  └── produces: domain objects with bie_ids in Universe registries

Stage 3 (Transform)
  └── receives: domain objects looked up from Universe by bie_id
  └── produces: enriched domain objects (same bie_ids, new relations)

Stage 4 (Export)
  └── receives: domain objects from Universe
  └── writes: target format (bie_id may be exported as stable key)
```

The `bie_id` is the stable key that flows through the pipeline — it is created once in
Stage 2 and referenced in all subsequent stages.
