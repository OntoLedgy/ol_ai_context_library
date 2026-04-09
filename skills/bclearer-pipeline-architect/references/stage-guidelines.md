# Stage Guidelines

Detailed per-stage guidance for bclearer pipeline design. Grounded in the bCLEARer
Pipeline Architecture Framework (`ol_bclearer_pdk/documentation/bclearer_pipeline_framework.md`)
and the bie_core_graph exemplar pipeline.

---

## Overview — The CLEAR Stages

The bCLEARer digital journey processes data through five sequential stages. Each stage
has a distinct responsibility. Mixing responsibilities across stages undermines the
framework's transparency, testability, and separation of concerns.

```
1c_collect  →  2l_load  →  3e_evolve  →  4a_assimilate  →  5r_reuse
  Gather        Read        Transform      Integrate         Output
```

The critical distinction:

- **Collect** gathers raw data sources into the pipeline's control — it does NOT
  read or parse file contents.
- **Load** reads and parses the collected data into in-memory structures ready for
  processing.

---

## Stage 1 — `1c_collect` (Collect)

### Purpose

**Gather data from external sources into the pipeline's staging area.** Collect is
about acquisition — bringing data under the pipeline's control. It is not about
understanding, parsing, or transforming the data.

### What Collect Does

- Copies or moves files from an external location to the pipeline's input area
- Fetches data from remote APIs and saves the raw response
- Queries a remote database and extracts raw table data (when direct database access
  is available and there is no intermediate staging area)
- Collects pre-exported files (CSV, JSON, etc.) from a database staging area (when
  direct database access is not available)
- Registers source file references (paths, URIs) in Universe registers

### What Collect Does NOT Do

- Does NOT open or read file contents (no `pd.read_excel()`, no `json.load()`,
  no `open().read()`)
- Does NOT parse or deserialise data formats
- Does NOT create DataFrames from file content
- Does NOT validate, clean, or normalise data
- Does NOT apply any domain logic or business rules
- Does NOT create BIE objects

### Output

File paths, URIs, or raw byte streams registered in Universe registers. For database
sources where the query IS the acquisition step, the output may be raw result sets or
DataFrames — but only because the interop service returns data in that form as part of
the extraction.

### Scenario Guide

| Source Type | Collect Action | Collect Output |
|-------------|---------------|----------------|
| **Local file** (Excel, CSV, JSON, Parquet) | Copy file to pipeline input folder | File path in Universe register |
| **Remote file** (SFTP, S3, HTTP download) | Download file to pipeline input folder | File path in Universe register |
| **Remote database** (direct access) | Query and extract table data via interop service | Raw result set / DataFrame in Universe register |
| **Database staging area** (exported file) | Collect the exported file (CSV, etc.) from staging area | File path in Universe register |
| **REST API** | Fetch raw response payload, save to staging | File path or raw response in Universe register |
| **Message queue** | Consume messages, persist to staging | File path or raw message data in Universe register |

### Pattern

**Adapter** — wraps a `bclearer_interop_services` module for the specific source type.
Contains no domain logic.

### Exemplar Note

The bie_core_graph pipeline handles collection during universe initialisation (the
source JSON file is copied to an `inputs/A_COLLECT/` folder structure and registered
in `source_table_dictionary`). The pipeline stages then begin at 2l_load.

---

## Stage 2 — `2l_load` (Load)

### Purpose

**Read, parse, and prepare the collected data for processing.** Load turns raw data
sources into typed, validated, in-memory structures that downstream stages can work
with.

### What Load Does

- Reads file contents from paths collected in stage 1 (e.g. `pd.read_excel()`,
  `json.load()`, `read_csv()`)
- Parses raw data into typed in-memory structures (DataFrames, dicts, lists)
- Validates data types, required fields, and structural constraints
- Normalises column names, data types, and formats
- Assigns BIE tracking metadata where applicable (as in the exemplar's
  `BieizeJsonStringBUnits`)
- Stores prepared data in Universe registers with enum-based keys

### What Load Does NOT Do

- Does NOT acquire data from external sources (that is Collect's job)
- Does NOT apply business logic, enrichment, or derivations
- Does NOT create domain objects or BIE entities
- Does NOT write to external targets

### Output

Cleaned, typed, validated in-memory structures (DataFrames, typed dicts) in Universe
registers, ready for Evolve.

### Scenario Guide

| Source Format | Load Action | Load Output |
|--------------|------------|-------------|
| **Excel file** (path from Collect) | Read workbook with `excel_services`, parse sheets into DataFrames | DataFrames in Universe registers |
| **CSV file** (path from Collect) | Read with `delimited_text`, parse into DataFrame | DataFrame in Universe register |
| **JSON file** (path from Collect) | Read with `json_service`, parse into dict or DataFrame | Typed structure in Universe register |
| **Parquet file** (path from Collect) | Read with `parquet_service` or `dataframe_service` | DataFrame in Universe register |
| **Raw database result** (from Collect) | Validate types, normalise column names, enforce schema | Cleaned DataFrame in Universe register |
| **Raw API response** (from Collect) | Parse JSON/XML response, extract relevant payload, validate | Typed structure in Universe register |

### Pattern

**Service** — pure transformation on in-memory data. May use `bclearer_interop_services`
to read files collected in stage 1 (this is reading locally-staged files, not reaching
out to external systems).

### Exemplar

In bie_core_graph, the 2l_load stage has two B-units:
1. `LoadJsonFileAsStringBUnits` — reads JSON files from the collected file paths into
   a DataFrame of raw strings
2. `BieizeJsonStringBUnits` — wraps the raw string data with BIE identity tracking
   metadata

---

## Stage 3 — `3e_evolve` (Evolve)

### Purpose

**Transform, enrich, and evolve data through business logic and domain processing.**
Evolve is the core of the bCLEARer digital journey — where information is made fitter
for its intended purpose. This is where BIE identity construction happens.

### What Evolve Does

- Applies business rules, derivations, and enrichment logic
- Constructs BIE domain objects and assigns BIE identities
- Performs structural transformations (splitting, merging, pivoting, flattening)
- Derives new fields, classifications, or relationships from existing data
- Builds domain-specific object models from prepared data

### What Evolve Does NOT Do

- Does NOT perform I/O — operates only on in-memory objects already in the Universe
- Does NOT read from or write to external sources or targets
- Does NOT acquire or parse raw data
- Does NOT import `bclearer_interop_services`

### Output

Enriched domain objects with BIE IDs, derived fields, and transformed structures in
Universe registries.

### Pattern

**Service** (processing) + **Factory** (BIE construction). Complex Evolve stages are
typically decomposed into sub-stages.

### Exemplar

In bie_core_graph, the 3e_evolve stage has two sub-stages:
1. `3e_evolve_2` (13 B-units) — parses JSON strings into structured tables: nodes,
   relationships, properties, labels
2. `3e_evolve_3` (3 B-units) — materialises Neo4j entity objects from the structured
   tables

---

## Stage 4 — `4a_assimilate` (Assimilate)

### Purpose

**Integrate and reconcile results across multiple pipelines, sources, or processing
passes.** Assimilate merges, cross-references, and reconciles data that has been
independently evolved.

### What Assimilate Does

- Merges data from multiple thin slices or pipelines
- Reconciles duplicates and conflicts between sources
- Cross-references domain objects across processing passes
- Aggregates or consolidates related records
- Resolves entity matching across different source systems

### What Assimilate Does NOT Do

- Does NOT perform I/O — operates only on in-memory objects
- Does NOT apply source-specific business logic (that belongs in Evolve)
- Does NOT import `bclearer_interop_services`

### Output

Reconciled, merged, or cross-referenced data in Universe registers, ready for Reuse.

### Pattern

**Service** — stateless reconciliation logic.

### When to Use

Not all pipelines need an Assimilate stage. Include it when:
- The pipeline processes data from multiple independent sources
- Multiple thin slices produce overlapping domain objects that need reconciliation
- Entity resolution or deduplication is required across sources

---

## Stage 5 — `5r_reuse` (Reuse)

### Purpose

**Write processed results to an external target for downstream consumption.** Reuse
is the mirror of Collect — it pushes data out of the pipeline's boundary.

### What Reuse Does

- Writes DataFrames to files (CSV, Parquet, Excel, JSON)
- Persists records to databases
- Publishes to message queues or event streams
- Exports to external APIs
- Generates output reports or snapshots

### What Reuse Does NOT Do

- Does NOT modify, transform, or enrich data
- Does NOT apply business logic
- Does NOT create BIE objects
- Does NOT read from external sources

### Output

Persisted or published records at the external target (file system, database, message
queue, API endpoint).

### Pattern

**Adapter** — wraps a `bclearer_interop_services` module for the specific target type.
Contains no domain logic. Pure write-out.

---

## Common Anti-Patterns

### Anti-Pattern: Reading Files in Collect

**Wrong** — reading and parsing an Excel file in a Collect B-unit:
```python
# WRONG: ca_read_excel_b_units.py (in 1c_collect)
def b_unit_process_function(self):
    dataframe = pd.read_excel(self.input_path)  # This is Load's job
    self.universe.set_register(RegistryEnums.RAW_DATA, dataframe)
```

**Right** — Collect acquires the file, Load reads it:
```python
# RIGHT: ca_collect_excel_file_b_units.py (in 1c_collect)
def b_unit_process_function(self):
    collected_path = copy_file_to_staging(
        source_path=self.input_path,
        staging_folder=self.staging_folder)
    self.universe.set_register(RegistryEnums.SOURCE_FILE_PATH, collected_path)

# RIGHT: la_read_excel_b_units.py (in 2l_load)
def b_unit_process_function(self):
    source_path = self.universe.get_register(RegistryEnums.SOURCE_FILE_PATH)
    dataframe = pd.read_excel(source_path)
    self.universe.set_register(RegistryEnums.RAW_DATA, dataframe)
```

### Anti-Pattern: Business Logic in Load

**Wrong** — applying business rules during Load:
```python
# WRONG: la_load_and_classify_b_units.py (in 2l_load)
def b_unit_process_function(self):
    dataframe = pd.read_csv(source_path)
    dataframe['category'] = dataframe['type'].map(BUSINESS_CLASSIFICATION)  # Evolve's job
```

### Anti-Pattern: I/O in Evolve

**Wrong** — reading from an external source during Evolve:
```python
# WRONG: ea_enrich_from_api_b_units.py (in 3e_evolve)
def b_unit_process_function(self):
    response = requests.get(API_URL)  # Collect's job
```

---

## Database Sources — Special Guidance

When the data source is a database, the boundary between Collect and Load requires
careful consideration:

### Direct Database Access Available

If the pipeline can connect directly to the source database:
- **Collect** queries the database and extracts the raw result set. The interop service
  (e.g. `relational_database_services.postgresql`) handles the connection and query
  execution. The output may be a DataFrame because that is how the interop service
  returns data — this is acceptable because the query IS the acquisition step.
- **Load** validates, normalises, and prepares the extracted data for Evolve.

### No Direct Database Access

If the pipeline receives pre-exported files from a database staging area:
- **Collect** fetches the exported file (CSV, Parquet, etc.) from the staging location.
- **Load** reads and parses the file into in-memory structures.

### Key Principle

The question is: **"Am I acquiring data from outside the pipeline's boundary, or am I
parsing data already under the pipeline's control?"**

- Acquiring from outside → Collect
- Parsing data already collected → Load
