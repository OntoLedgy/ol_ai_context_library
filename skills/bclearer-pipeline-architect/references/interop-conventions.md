# Interop Service Conventions

Grounded in the bclearer PDK source at `ol_bclearer_pdk/libraries/interop_services/bclearer_interop_services/`.

---

## Principle

Interop services are **boundary adapters only**. They appear in stages that
cross a boundary out of (or into) the pipeline universe:

- **Stage 1c_collect** — gathering data from an external source into the pipeline's staging area
- **Stage 2l_load** — deserialising locally-staged bytes into a source-shaped in-memory mirror (the file is already under the pipeline's control after Collect). Load does not change the data — it only computerises it.
- **Stage 4a_assimilate** — writing the evolved BIE fragment into the **master BORO ontology object store**. This is a boundary — the master store lives outside the pipeline universe — so Assimilate uses a master-store adapter. Apart from this master-store adapter, Assimilate does not import other `bclearer_interop_services` modules.
- **Stage 5r_reuse** — writing the pipeline's own outputs to downstream consumers

The **pure in-memory domain stage** is **3e_evolve**. Evolve must NOT import
or depend on any `bclearer_interop_services` module — all transformation,
BIE identity assignment, business logic, and cross-slice merging happens
entirely on in-memory Universe state.

```
External Source
    ↓
[1c_collect B-unit] ── bclearer_interop_services ──→ Universe registers
                                                       (file paths / raw bytes)
    ↓
[2l_load B-unit] ── bclearer_interop_services ──→ Universe registers
                                                    (source-shaped in-memory mirror)
    ↓
[3e_evolve B-units]           (pure in-memory — NO interop imports)
    ↓                          transformation, BIE identity, enrichment,
Universe registers             cross-slice merges
    ↓
[4a_assimilate B-unit] ── master-store adapter ──→ Master BORO ontology object store
    ↓                                              (plus optional injection report
Universe registers                                  back into Universe for Reuse)
    ↓
[5r_reuse B-unit] ── bclearer_interop_services ──→ External Target
```

This boundary makes Evolve independently testable — it can be exercised with
mock Universe data without any I/O. Assimilate can also be tested with a
mock master-store adapter, keeping the compliance-reconciliation logic
independently verifiable.

---

## Service Catalogue

All services live under `bclearer_interop_services`:

| Service Package | Use For | Notes |
|----------------|---------|-------|
| `delimited_text` | CSV, TSV, other delimited flat files | Standard choice for tabular text input |
| `excel_services` | Excel workbooks (.xlsx, .xls) | Use the service facade; do not call `openpyxl` directly |
| `dataframe_service` | Pandas DataFrame operations and Parquet via DataFrame | Helpers, checks, register types |
| `parquet_service` | Parquet files directly | Includes reduce-and-export orchestrators |
| `hdf5_service` | HDF5 files | Use for large numerical datasets |
| `document_store_services.json_service` | JSON files | |
| `document_store_services.xml_service` | XML files | |
| `document_store_services.mongo_db_service` | MongoDB | |
| `relational_database_services.postgresql` | PostgreSQL | |
| `relational_database_services.sqlite_service` | SQLite | |
| `relational_database_services.sql_server_service` | MS SQL Server | |
| `relational_database_services.access_service` | MS Access | |
| `relational_database_services.sqlalchemy_service` | SQLAlchemy-compatible databases | |
| `graph_services.network_service` | NetworkX in-process graphs | Preferred for analytical pipelines |
| `graph_services.neo4j_service` | Neo4j persisted graphs | For production graph persistence |
| `graph_services.raphtory_service` | Raphtory temporal graphs | For time-aware graph analytics |
| `file_system_service` | File system traversal, path operations, zip | Use for snapshot-style pipelines |
| `b_dictionary_service` | Python dict ↔ table/DataFrame conversions | Use when data arrives as dicts |
| `list_services` | List utilities | |
| `tuple_service` | Tuple utilities | |
| `pyspark_service` | PySpark for large-scale distributed data | Only when data does not fit in memory |
| `ea_interop_service` | Enterprise Architect model files | |
| `real_time_database_services.influxdb_service` | InfluxDB time-series | |
| `yxdb_service` | Alteryx YXDB files | |

---

## Format Selection Guide

| Source / Target Type | Recommended Service | Notes |
|---------------------|--------------------|----|
| CSV / TSV / delimited | `delimited_text` | Standard choice |
| Excel workbook | `excel_services` | Use service facade; never call `openpyxl` directly |
| Parquet | `parquet_service` or `dataframe_service.parquet_as_dataframe_services` | Prefer `dataframe_service` if operating on DataFrames throughout |
| JSON | `document_store_services.json_service` | |
| XML | `document_store_services.xml_service` | |
| PostgreSQL / SQLite / SQL Server | `relational_database_services.[db]` | Pick the specific sub-service for the database |
| File system traversal / snapshots | `file_system_service` | Includes BIE-ready file system domain objects |
| In-process graph analysis | `graph_services.network_service` | NetworkX |
| Persistent graph | `graph_services.neo4j_service` | |
| Data arriving as dicts | `b_dictionary_service` | Convert to typed registers before passing to domain stages |
| Large-scale tabular (> memory) | `pyspark_service` | Last resort; prefer Parquet + chunked processing first |

---

## DataFrame vs. Dictionary — When to Use Each

| Situation | Use |
|-----------|-----|
| Tabular data with homogeneous rows (e.g. CSV, database result set) | `dataframe_service` — keeps data as DataFrame in registers |
| Heterogeneous or nested data (e.g. JSON, config files) | `b_dictionary_service` — convert to flat dict, then to domain objects in 3e_evolve |
| Data that will be used for BIE identity construction | Either — but convert to typed domain objects in 3e_evolve before calling BIE factories |
| Data that will be exported as a table | `dataframe_service` — keep as DataFrame through to 5r_reuse |

---

## Adapter Boundary Rules

1. **Import interop services only in B-units inside `1c_collect`, `2l_load`, and `5r_reuse` stages.**
2. **Never import interop services in orchestrators, services, or BIE modules.**
3. **Data leaving a collect B-unit enters the Universe as file paths, URIs, or raw extracted data** — Load parses it into typed structures.
4. **Data leaving a load B-unit enters the Universe as typed, in-memory structures** (DataFrames, typed dicts) — domain stages receive it from there.
5. **Data entering a reuse B-unit is read from Universe registers** — the B-unit calls the interop service to write it out.
6. **Error handling at adapter boundaries**: raise a specific exception type (not bare `Exception`) if a source file is missing, malformed, or a target write fails. Log the specific path or query that failed.

---

## File Path Conventions

- All input/output paths are passed through Universe configuration registers (not hardcoded in B-units)
- Use `os.path.join()` for path construction; never string concatenation
- Input folder paths go into Universe configuration at pipeline startup (before stage 1)
- Output folder paths are similarly injected at startup

---

## Connection and Credential Management

- Credentials are **never hardcoded** — inject via environment variables or a config file path passed into the Universe at startup
- Database connections are opened inside the B-unit that needs them and closed within the same B-unit (no connection objects stored on the Universe)
- Use context managers (`with`) for connection lifecycle management
