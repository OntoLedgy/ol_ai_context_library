# Technology Stack Reference

This document describes the libraries available for use in solutions, their capabilities, and when to choose each.

> **Platform Note:** Python is the reference implementation platform. All library categories below have Python implementations in the bclearer stack. For other target platforms (JavaScript/TypeScript, C#, Rust), equivalent libraries must be constructed following the same architectural principles. Where a platform-specific equivalent does not yet exist, its construction should be included in the solution development plan.

---

## Python Reference Stack

### Library Overview

| Library | Package Root | Purpose |
|---------|-------------|---------|
| `bnop` | `bnop` | BORO upper ontology — object model, registries, naming |
| `interop_services` | `bclearer_interop_services` | Data I/O — formats, databases, file systems, graphs |
| `orchestration_services` | `bclearer_orchestration_services` | Pipelines, identification (BIE), logging, snapshots |

---

### bnop — Upper Ontology

**Location:** `/home/khanm/bclearer/ol_bclearer_pdk/libraries/ontology/`

**Use when:** You need to represent entities at the upper-ontology level — objects, types, names, tuples — especially when the domain is not yet formalised as a BIE component.

**Key modules:**

| Module | Contents |
|--------|---------|
| `bnop.core.object_model.objects` | `BnopObjects` — base for all BORO individuals |
| `bnop.core.object_model.places` | Place types for object construction |
| `bnop.core.factories` | Consistent object creation with registry management |
| `bnop.boxology` | BORO box ontology (spatial/temporal extents) |
| `bnop.mappings` | Cross-system identity mappings |
| `bnop.bnop_io` | Persistence / serialisation |
| `bnop.rdf_jena` | RDF/SPARQL integration |
| `bnop.migrations` | XML export for external systems |

**Avoid when:** The domain is already formalised as a BIE component — use `orchestration_services.identification_services` instead.

---

### interop_services — Data I/O

**Location:** `/home/khanm/bclearer/ol_bclearer_pdk/libraries/interop_services/`

**Use when:** Reading from or writing to external data sources — files, databases, APIs, graph stores.

**Service catalogue:**

| Service | When to use |
|---------|------------|
| `excel_services` | Reading/writing Excel workbooks; includes orchestrators and facades |
| `delimited_text` | CSV and other delimited flat files |
| `parquet_service` | Parquet files; includes Delta Lake support |
| `relational_database_services` | PostgreSQL, SQLite, SQL Server, Access |
| `graph_services` | Neo4j, NetworkX, Raphtory, CoZoDB |
| `document_store_services` | JSON documents, XML, MongoDB |
| `file_system_service` | File path operations, directory traversal, file metadata |
| `pyspark_service` | Distributed processing via PySpark + Delta |
| `hdf5_service` | HDF5 hierarchical data format |
| `real_time_database_services` | InfluxDB time-series |
| `ea_interop_service` | Enterprise Architect model import/export |
| `b_dictionary_service` | Dictionary-based tabular data representation |
| `dataframe_service` | DataFrame operations (pandas/PySpark abstraction) |

**Design note:** Interop services should be **adapters** in the architecture — they sit at system boundaries and translate between external formats and internal domain objects. Domain logic should never depend directly on a specific interop service implementation.

---

### orchestration_services — Pipelines and Identification

**Location:** `/home/khanm/bclearer/ol_bclearer_pdk/libraries/orchestration_services/`

**Use when:** Building pipelines, working with BIE identity, orchestrating multi-step processes.

**Service catalogue:**

| Service | When to use |
|---------|------------|
| `identification_services.b_identity_ecosystem` | BIE framework — deterministic identity for domain objects |
| `file_system_snapshot_service` | BIE canonical example; also a production snapshot service |
| `snapshot_universe_service` | Universe-level snapshot orchestration |
| `logging_service` | Structured logging with BIE integration |
| `log_environment_utility_service` | Environment and configuration logging |
| `datetime_service` | Timezone-aware datetime operations |
| `string_service` | String normalisation, parsing |
| `unicode_service` | Unicode-safe text operations |
| `unit_of_measure_services` | Dimensional analysis, unit conversion |
| `version_control_services` | Git integration (blame, log, diff) |
| `static_code_analysis_service` | Code quality tooling integration |
| `bclearer_load_service` | Package loading and initialisation |
| `container_services` | Docker/containerisation support |
| `b_app_runner_service` | Application entry point management |
| `reporting_service` | Structured report generation |

**BIE identification — key imports:**

```python
# Core identity types
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import BieIds
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import BieEnums
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_domain_types import BieDomainTypes

# Identity creation
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import BieIdCreationFacade
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.identity_vectors.common_identity_vector import CommonIdentityVector

# Base object classes
from bclearer_core.bie.top.bie_objects import BieObjects
from bclearer_core.bie.domain.bie_domain_objects import BieDomainObjects
from bclearer_core.bie.top.bie_base_identities import BieBaseIdentities, create_bie_base_identity_from_bie_identity_vector
```

---

## UI Library

UI elements are Infrastructure layer components and must not carry domain logic.

| Platform | Library | Status |
|----------|---------|--------|
| Python (and general) | [`ol_ui_library`](https://github.com/OntoLedgy/ol_ui_library) | Reference implementation — pending clean-coding refactor |
| JavaScript / TypeScript | TBD — to be constructed following ol_ui_library principles | Not yet available |
| C# | TBD — to be constructed following ol_ui_library principles | Not yet available |
| Rust | TBD — to be constructed following ol_ui_library principles | Not yet available |

When a solution requires UI components on a platform without an existing library, the construction of that UI library should be included as an explicit phase in the solution development plan.

---

## Cross-Platform Equivalents

When designing solutions for non-Python platforms, each bclearer library category requires an equivalent. Use this as a planning checklist:

| Capability | Python Reference | Required for Other Platforms |
|------------|-----------------|------------------------------|
| Upper ontology objects | `bnop` | Equivalent BORO object model library |
| BIE identity | `orchestration_services.identification_services` | Deterministic identity library |
| File / DB I/O | `interop_services` | Platform-specific adapter library |
| Pipeline orchestration | `orchestration_services` | Pipeline / workflow library |
| Logging | `orchestration_services.logging_service` | Structured logging library |
| UI components | `ol_ui_library` | Platform UI component library |

If a required equivalent does not exist, flag it as a dependency in the solution development plan and include a phase to build it.

---

## Decision Guide

Use this to choose the right library for a given concern:

| Concern | Recommended Library/Service |
|---------|-----------------------------|
| Representing a domain entity with stable identity | `orchestration_services` → BIE |
| Representing an upper-ontology entity (pre-BIE) | `bnop` |
| Reading an Excel file | `interop_services` → `excel_services` |
| Reading a CSV | `interop_services` → `delimited_text` |
| Writing to PostgreSQL | `interop_services` → `relational_database_services` |
| Graph traversal (NetworkX) | `interop_services` → `graph_services` |
| Pipeline orchestration | `orchestration_services` → `b_app_runner_service` or custom orchestrator |
| Structured logging | `orchestration_services` → `logging_service` |
| File metadata/snapshot | `orchestration_services` → `file_system_snapshot_service` |
| Distributed data (Spark) | `interop_services` → `pyspark_service` |
| Canonical BIE example | `orchestration_services` → `file_system_snapshot_service` |
| UI / dashboard | `ol_ui_library` (Python) or platform equivalent |
