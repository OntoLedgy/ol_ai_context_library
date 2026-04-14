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
1c_collect  →  2l_load       →  3e_evolve    →  4a_assimilate           →  5r_reuse
  Gather       Computerise      Transform       Inject into master BORO    Output
                                                ontology object store
```

The critical distinctions:

- **Collect** gathers raw data sources into the pipeline's control — it does NOT
  read or parse file contents.
- **Load** computerises the collected bytes — it lifts them into in-memory
  structures that faithfully mirror the source. Load does NOT change the data:
  no normalisation, no validation beyond "can it be parsed at all?", no schema
  enforcement, no BIE identity assignment.
- **Evolve** is where data is changed — typing, normalising, BIE identity
  assignment, business logic, enrichment.
- **Assimilate** injects the evolved BIE fragment into the **master BORO
  ontology object store**. It typically reconciles a not-yet-compliant
  fragment against the master compliance model. This is semantic integration
  against a persistent master store — not a pipeline-local merge. See
  `skills/bie-component-ontologist/references/four-facet-architecture.md`
  § "BIE is not BORO" for the ontology distinction.

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

**Computerise the collected bytes.** Load lifts the raw data collected in
stage 1 into in-memory structures that **faithfully mirror the source**. Load
is about making the data programmatically addressable — it is **not** about
changing the data. If a value, column name, type, or shape differs between
the source and the Universe register after Load, Load has over-reached.

### What Load Does

- Reads file contents from paths collected in stage 1 (e.g. `pd.read_excel()`,
  `json.load()`, `read_csv()`)
- Deserialises raw bytes into the most direct in-memory representation of the
  source (DataFrame for tabular, dict/list for tree-shaped, string blob for
  opaque formats)
- Stores the source-shaped structures in Universe registers with enum-based
  keys

### What Load Does NOT Do

- Does NOT acquire data from external sources (Collect's job)
- Does NOT rename, retype, or normalise columns (Evolve's job)
- Does NOT validate beyond "can this be parsed at all?" — no required-field
  checks, no schema enforcement, no range/domain validation (Evolve's job)
- Does NOT drop, fill, coerce, or otherwise transform values (Evolve's job)
- Does NOT assign BIE identities or attach BIE tracking metadata (Evolve's
  job — identity assignment is the *first* act of Evolve, not the last act of
  Load)
- Does NOT apply business logic, enrichment, or derivations (Evolve's job)
- Does NOT create domain objects (Evolve's job)
- Does NOT write to external targets (Reuse's job)

### Output

An in-memory mirror of the source bytes, held in Universe registers and ready
for Evolve to begin transforming. The shape and content of each register must
round-trip cleanly back to the source form; if it does not, a transformation
has leaked into Load.

### Scenario Guide

| Source Format | Load Action | Load Output |
|--------------|------------|-------------|
| **Excel file** (path from Collect) | Read workbook with `excel_services`, deserialise sheets as-is | DataFrames mirroring source sheets in Universe registers |
| **CSV file** (path from Collect) | Read with `delimited_text`, deserialise rows as-is | DataFrame mirroring source rows in Universe register |
| **JSON file** (path from Collect) | Read with `json_service`, deserialise into dict/list mirroring the JSON tree | Source-shaped structure in Universe register |
| **Parquet file** (path from Collect) | Read with `parquet_service` or `dataframe_service` | DataFrame mirroring source in Universe register |
| **Raw database result** (from Collect) | Hold the result set as-returned by the interop service | Source-shaped DataFrame in Universe register |
| **Raw API response** (from Collect) | Deserialise JSON/XML payload as-is | Source-shaped structure in Universe register |

Note: any column renaming, type coercion, schema enforcement, or payload
extraction belongs in **Evolve**, not Load.

### Pattern

**Adapter (inbound parse)** — uses `bclearer_interop_services` to deserialise
locally-staged files into in-memory mirrors. Holds no domain logic and
applies no transformation beyond what the underlying parser emits.

### Exemplar

In bie_core_graph, the 2l_load stage reads JSON files from the collected file
paths into a DataFrame of raw strings (`LoadJsonFileAsStringBUnits`). That is
all Load does. The subsequent `BieizeJsonStringBUnits` — which wraps the raw
string data with BIE identity tracking metadata — is the **first sub-stage
of Evolve**, not part of Load. Attaching BIE identities is an act of
transformation; Load does not transform.

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

**Inject the evolved BIE-identified fragment into the master BORO ontology
object store.** Assimilate takes the ontology fragment produced in Evolve —
which is typically not yet compliant with the master ontology's compliance
model — and integrates it into the authoritative master store, reconciling
any non-compliance on the way in.

Assimilate is the semantic bridge between the pipeline's local BIE ontology
(identity for data-structure artefacts) and the **master BORO ontology
object store** (identity for real-world business objects). See
`skills/bie-component-ontologist/references/four-facet-architecture.md`
§ "BIE is not BORO" for the ontology distinction.

### What Assimilate Does

- Opens a write boundary onto the master BORO ontology object store
- Injects the evolved BIE fragment (objects, relations, identities) produced
  by Evolve into the master store
- Reconciles the fragment against the master ontology's compliance model —
  detects and resolves violations of extensionality, identity, typing,
  whole-part, or any domain-specific compliance rules enforced by the master
- Reconciles the fragment's BIE-identified artefacts against pre-existing
  BORO individuals in the master store (same-as resolution, coupling,
  upgrade of BIE identities to their BORO counterparts where applicable)
- Commits the assimilated fragment into the master store

### What Assimilate Does NOT Do

- Does NOT build new BIE identities for the fragment (Evolve's job — the
  fragment arrives at Assimilate already BIE-identified)
- Does NOT apply source-specific business rules (Evolve's job)
- Does NOT perform the pipeline's own cross-slice merges (Evolve's job —
  merging two thin slices produced by the same pipeline is a transformation,
  not an injection into the master store)
- Does NOT write the pipeline's own outputs (Reuse's job — Reuse writes to
  downstream consumers, Assimilate writes to the master BORO store)

### Output

The master BORO ontology object store now contains the assimilated fragment
(after compliance reconciliation). The Universe registers may also record a
report of what was injected, rejected, or amended, for downstream Reuse.

### Pattern

**Outbound adapter (to the master BORO store)** + **compliance reconciler**.
The adapter owns the connection to the master store; the reconciler owns the
compliance logic. Analogous in shape to Reuse (both cross a boundary out of
the pipeline universe), but distinct in target — Reuse writes to downstream
consumers, Assimilate writes into the master ontology.

### When to Use

Include an Assimilate stage when the pipeline produces a BIE/BORO fragment
that must land in the master BORO ontology object store. Typical triggers:

- The pipeline discovers or derives new business individuals that the
  organisation's master ontology needs to know about
- The pipeline produces an ontology fragment that must be reconciled against
  the master compliance model before downstream systems can rely on it
- The pipeline materialises relations or classifications that extend the
  master ontology

**Not a trigger for Assimilate**: needing to merge multiple thin slices or
multiple source feeds inside the pipeline. That is a transformation and
belongs in Evolve (typically a late Evolve sub-stage).

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

### Anti-Pattern: Normalisation / Validation / BIE-ing in Load

**Wrong** — changing the shape or content of the data during Load:
```python
# WRONG: la_load_and_normalise_b_units.py (in 2l_load)
def b_unit_process_function(self):
    dataframe = pd.read_csv(source_path)
    dataframe.columns = [c.lower().strip() for c in dataframe.columns]  # Evolve's job
    dataframe = dataframe.dropna(subset=['customer_id'])                # Evolve's job
    dataframe['bie_id'] = dataframe.apply(make_bie_id, axis=1)          # Evolve's job
    self.universe.set_register(RegistryEnums.CUSTOMERS, dataframe)
```

**Right** — Load mirrors the source, Evolve does the rest:
```python
# RIGHT: la_load_csv_b_units.py (in 2l_load)
def b_unit_process_function(self):
    dataframe = pd.read_csv(source_path)
    self.universe.set_register(RegistryEnums.RAW_CUSTOMERS, dataframe)

# RIGHT: ea1_normalise_customers_b_units.py (in 3e_evolve)
# RIGHT: ea2_bieize_customers_b_units.py  (in 3e_evolve)
```

Rule of thumb: if the register after Load does not round-trip back to the
source bytes (modulo parser-intrinsic representation choices), Load has
over-reached.

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
