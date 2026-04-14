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

Identity flows through the canonical CLEAR stages. **Always use the CLEAR
stage names** — do not introduce synonyms such as "Ingest", "Identify",
"Transform", or "Export". "Load" in CLEAR specifically means *computerising
the collected bytes*; it has caused drift in the past when readers have
mistaken it for an export step.

```
Stage 1c_collect (Collect)
  └── produces: file paths / raw bytes staged in Universe registers
                (no BIE IDs — nothing is BIE-identified yet)

Stage 2l_load (Load)
  └── produces: source-shaped in-memory mirror of the bytes
                (no BIE IDs — Load does not change the data)

Stage 3e_evolve (Evolve)  ← bie-data-engineer's factories are called here
  └── first sub-stage: BIE identity assignment — domain objects materialised
                       with bie_ids in Universe registries
  └── later sub-stages: transformation, enrichment, derivations, cross-slice
                        merges (all operate on BIE-identified objects)
  └── produces: a BIE-identified ontology fragment

Stage 4a_assimilate (Assimilate)
  └── injects the evolved BIE fragment into the master BORO ontology object
      store, reconciling non-compliance against the master compliance model
  └── produces: the fragment committed to the master store

Stage 5r_reuse (Reuse)
  └── receives: domain objects (and optional Assimilate report) from Universe
  └── writes: target format for downstream consumers (bie_id may be exported
              as a stable key)
```

The `bie_id` is the stable key that flows through the pipeline — it is
created in Evolve's first sub-stage and referenced in all subsequent stages.

**BIE vs BORO reminder**: a `bie_id` identifies a data-structure artefact,
not a real-world business object. The bridge to BORO identity happens at
Assimilate, where the fragment is injected into the master BORO ontology
object store. See
`skills/bie-component-ontologist/references/four-facet-architecture.md`
§ "BIE is not BORO".
