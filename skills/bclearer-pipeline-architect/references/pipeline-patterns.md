# bclearer Pipeline Patterns

> **Status: Skeleton** — populate with specific bclearer pipeline topology patterns as they are formalised from the codebase. See `bclearer_orchestration_services` for existing examples.

---

## Standard Pipeline Topology

bclearer pipelines follow a four-stage structure. Not all stages are required for every pipeline; include only the stages that apply.

```
┌─────────────────────────────────────────────────────┐
│  Pipeline Runner (entry point)                      │
│  ├── Stage 1: Ingest        (reads raw data)        │
│  ├── Stage 2: Identify      (creates BIE objects)   │
│  ├── Stage 3: Transform     (enriches/processes)    │
│  └── Stage 4: Load/Export   (writes output)         │
└─────────────────────────────────────────────────────┘
```

### Stage 1 — Ingest

- Responsibility: Read raw data from an external source via an interop adapter
- Input: external data source (file, database, API)
- Output: raw Python data structures (dicts, dataframes, or lightweight data objects)
- Pattern: **Adapter** — wraps an `interop_services` module; no domain logic here
- **Does not** create BIE objects or perform transformations

### Stage 2 — Identify

- Responsibility: Construct domain objects with BIE identity from raw data
- Input: raw data from Stage 1
- Output: domain objects with `bie_id`s, registered in the Universe
- Pattern: **Factory** — calls BIE factory functions in leaf-before-whole order
- **Does not** read from external sources or write to external targets

### Stage 3 — Transform / Enrich

- Responsibility: Apply business logic, enrichment, or derivations to domain objects
- Input: identified domain objects from Stage 2 (or a subset)
- Output: enriched/transformed domain objects or derived results
- Pattern: **Service** — stateless functions or classes with single responsibility
- **Does not** perform I/O; operates only on in-memory domain objects

### Stage 4 — Load / Export

- Responsibility: Write results to an external target
- Input: transformed domain objects or derived data structures
- Output: persisted records (file, database, message queue)
- Pattern: **Adapter** — wraps an `interop_services` module; no domain logic
- **Does not** modify domain objects

---

## Universe Wiring

Each pipeline run operates within a **Universe** — a scoped container that holds all registries and domain objects for that run.

- Universe is created at the top of the runner
- Passed down through all stages
- Disposed (or serialised) at the end of the run
- Never stored in global or module-level state

---

## Reference Implementation

The canonical bclearer pipeline example is the File System Snapshot service:

```
bclearer_orchestration_services.file_system_snapshot_service.universe
```

Study this when designing a new pipeline — it demonstrates Stage 2 (identify) and Stage 4 (export) patterns against a real domain.

---

## Patterns to Document (TODO)

The following should be populated from the codebase as patterns are confirmed:

- [ ] Batch vs. event-driven pipeline topology differences
- [ ] Incremental / delta pipeline patterns (only process new/changed records)
- [ ] Error handling and retry patterns at the pipeline level
- [ ] Multi-source fan-in patterns (merging records from several adapters)
- [ ] Fan-out / broadcast patterns (same domain objects to multiple targets)
- [ ] Snapshot vs. streaming universe lifecycle
