# Interop Service Conventions

> **Status: Skeleton** — populate with bclearer-specific conventions as they are confirmed from pipeline implementations. Base service catalogue is in `software-architect/references/technology-stack.md`.

---

## Principle

Interop services are **boundary adapters only**. They appear in Stage 1 (Ingest) and Stage 4 (Load/Export). Domain logic — stages 2 and 3 — must not import or depend on any `bclearer_interop_services` module directly.

```
Stage 1 Adapter   ─── bclearer_interop_services ───→  domain data
domain objects    ───────────────────────────────→  Stage 4 Adapter  ─── bclearer_interop_services ───→  external target
```

---

## Format Selection Guide

> Populate with bclearer-confirmed choices as pipelines are built.

| Source/Target Type | Recommended Service | Notes |
|--------------------|--------------------|----|
| Excel workbooks | `excel_services` | Use facade; do not call openpyxl directly |
| CSV / delimited flat files | `delimited_text` | |
| Parquet / Delta Lake | `parquet_service` | Prefer for analytical pipelines |
| PostgreSQL | `relational_database_services` | |
| File system traversal | `file_system_service` | Use for snapshot-style pipelines |
| Graph data | `graph_services` | Choose NetworkX for in-process; Neo4j for persisted |
| Distributed data (large scale) | `pyspark_service` | |

---

## Conventions to Document (TODO)

- [ ] Standard Excel ingestion pattern (facade vs. orchestrator vs. raw service)
- [ ] Preferred DataFrame representation for inter-stage data transfer
- [ ] When to use `b_dictionary_service` vs. dataframes
- [ ] File path convention for pipeline input/output locations
- [ ] Error handling at adapter boundaries (what to do when a file is missing, malformed, etc.)
- [ ] Connection and credential management conventions
