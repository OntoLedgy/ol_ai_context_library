# bclearer Pipeline Patterns

Grounded in the bclearer PDK source at `ol_bclearer_pdk/libraries/core/bclearer_core/`.

---

## Core Concepts

### The Data Hierarchy

Every bclearer pipeline uses a three-level containment hierarchy to carry state:

```
Universe  (pipeline-run scope — top-level container)
  └── Registry  (logical group of related data)
        └── Register  (single piece of content: DataFrame, dict, graph, etc.)
```

The Universe is passed through all stages. B-units read from and write to it.
Stages do not communicate directly — they use the Universe as shared state.

### The Execution Hierarchy

```
Domain
  └── Pipeline(s)
        └── Thin Slice(s)           ← a horizontal slice of work through the pipeline
              └── Stage(s)          ← fixed bclearer stages (see below)
                    └── Sub-Stage(s) (optional, for complex stages)
                          └── B-Unit(s)  ← atomic unit of work
```

A **thin slice** is the recommended way to structure a pipeline — it represents one
complete pass of data through all stages. Multiple thin slices handle multiple data
shapes or pass types within a single pipeline.

---

## Standard 5-Stage Topology

bclearer pipelines follow a **fixed 5-stage structure**. Not all stages are required
for every pipeline — include only the stages that apply.

```
1c_collect   →  2l_load         →  3e_evolve    →  4a_assimilate            →  5r_reuse
   Collect        Load                Evolve          Assimilate                   Reuse
  (gather)     (computerise —       (transform)    (inject into master BORO     (output)
                faithful mirror                     ontology object store)
                of the source)
```

### Stage 1 — `1c_collect` (Collect)

- **Responsibility**: Gather data from external sources into the pipeline's staging area
- **Input**: External source (file system, database, API, message queue)
- **Output**: File paths, URIs, or raw extracted data registered in Universe registers
- **Pattern**: Adapter — wraps a `bclearer_interop_services` module; no domain logic
- **Must NOT**: Read or parse file contents, create DataFrames from files, create BIE objects, apply transformations, or write to external targets

For file-based sources (Excel, CSV, JSON, Parquet), Collect acquires the file — it does
NOT open or parse it. For database sources where the query IS the acquisition step,
Collect may return result sets directly. See `references/stage-guidelines.md` for
detailed scenario guidance.

### Stage 2 — `2l_load` (Load)

- **Responsibility**: Computerise collected bytes — deserialise them into an in-memory mirror of the source. Load does not change the data.
- **Input**: File paths or raw data from stage 1 in Universe registers
- **Output**: Source-shaped in-memory structures in Universe registers (round-trip to the source bytes, modulo parser-intrinsic representation)
- **Pattern**: Inbound adapter — uses `bclearer_interop_services` to deserialise locally-staged files; no domain logic, no transformation beyond what the parser emits
- **Must NOT**: Acquire data from external sources; rename/retype/normalise columns; validate beyond "can this be parsed at all?"; drop/fill/coerce values; assign BIE identities or attach BIE tracking metadata; apply business logic; write to external targets

### Stage 3 — `3e_evolve` (Evolve)

- **Responsibility**: Apply business logic, enrichment, derivations, and BIE identity construction
- **Input**: Prepared data from stage 2; BIE factory functions are called here if applicable
- **Output**: Enriched domain objects with BIE IDs registered in Universe registries
- **Pattern**: Service (processing) + Factory (BIE construction)
- **Must NOT**: Perform I/O; operates only on in-memory objects

### Stage 4 — `4a_assimilate` (Assimilate)

- **Responsibility**: Inject the evolved BIE-identified fragment into the **master BORO ontology object store**, reconciling non-compliance against the master compliance model
- **Input**: BIE-identified objects and relations from stage 3 (the evolved ontology fragment)
- **Output**: Fragment committed into the master BORO ontology object store; optional report of injected/rejected/amended items in Universe registers for downstream Reuse
- **Pattern**: Outbound adapter (to the master BORO store) + compliance reconciler. Analogous to Reuse in that it crosses a boundary out of the pipeline universe, but targets the master ontology rather than downstream consumers
- **Must NOT**: Build new BIE identities (Evolve); apply source-specific business rules (Evolve); perform pipeline-local cross-slice merges (Evolve); write the pipeline's own outputs (Reuse)

### Stage 5 — `5r_reuse` (Reuse)

- **Responsibility**: Write results to an external target for consumption
- **Input**: Final processed data from Universe registers
- **Output**: Persisted or published records (file, database, message queue)
- **Pattern**: Adapter — wraps a `bclearer_interop_services` module; no domain logic
- **Must NOT**: Modify data or apply business logic; pure write-out

---

## Sub-Stages

A stage can be decomposed into **sub-stages** for complex processing. Each sub-stage:
- Has its own orchestrator file
- Contains its own B-units
- Is called in order by the parent stage orchestrator

Sub-stages are optional. Use them when a stage has more than ~3 B-units or when there
are distinct logical phases within a stage that benefit from independent orchestration.

Sub-stage naming: `{pipeline_name}_{stage_name}_{sub_stage_name}` (e.g. `my_pipeline_3e_evolve_parse_headers`).

---

## B-Unit Types

### Bare B-Unit (`b_units`)

Stateless — no shared Universe object. Each B-unit is independent.

```python
class CollectCsvDataBUnits(BUnits):
    def __init__(self):
        pass

    def run(self) -> None:
        log_inspection_message(
            message='Running bUnit: {}'.format(
                self.__class__.__name__),
            logging_inspection_level_b_enum=\
                LoggingInspectionLevelBEnums.INFO)
        self.b_unit_process_function()

    def b_unit_process_function(
            self) \
            -> None:
        # implement here
        pass
```

**When to use**: Simple, side-effect-free units; no state to pass between B-units.

### Object-Passing B-Unit (`b_units_with_object_passing_and_returning`)

Receives a Universe (or any typed object) and mutates it.

```python
class LoadTransactionsBUnits(
        BUnitsWithObjectPassingAndReturning):

    def __init__(
            self,
            input_object=None):
        super().__init__(
            input_object=input_object)

    def _b_unit_process_function(
            self) \
            -> None:
        # self.input_object is the Universe
        # read from and write to registries here
        pass
```

**When to use**: Most pipelines — the Universe pattern lets B-units share and
accumulate state across a stage without direct coupling. Strongly preferred for any
pipeline that builds BIE objects or aggregates data across multiple B-units.

---

## B-Unit Naming Convention

B-units are named with a stage-letter prefix + sequential letter + optional descriptor:

| Stage | Prefix | Example B-unit names |
|-------|--------|---------------------|
| `1c_collect` | `c` | `ca_b_unit`, `cb_b_unit`, `ca_read_csv` |
| `2l_load` | `l` | `la_b_unit`, `lb_b_unit` |
| `3e_evolve` | `e` | `ea_b_unit`, `eb_b_unit` |
| Sub-stage of `3e_evolve` | `ea`, `eb`… | `ea1_b_unit`, `ea2_b_unit` |
| `4a_assimilate` | `a` | `aa_b_unit`, `ab_b_unit` |
| `5r_reuse` | `r` | `ra_b_unit`, `rb_b_unit` |

---

## Universe Wiring

- Universe is created at the **top of the runner** — not inside a stage or B-unit
- Passed as a named parameter through every orchestrator level (pipeline → thin slice → stage → sub-stage) and then as `input_object` to all object-passing B-units
- Holds all registries and registers for the lifetime of the pipeline run
- Never stored in global or module-level state
- Disposed (or serialised via `export_to_disk()`) after the final stage

### Universe Naming Between Stages

**Do not rename the universe parameter between stages.** Use a single, consistent
parameter name at every orchestrator level from the pipeline orchestrator downward.

The exemplar pattern (from `bie_core_graph`):

| Level | Parameter Name | Type Hint |
|-------|---------------|-----------|
| Runner (creation) | `{domain_specific_name}` (e.g. `neo4j_import_spoke_bclearer_run_universe`) | Specific subclass |
| Pipeline orchestrator | `bclearer_run_universe` | `BClearerRunUniverses` (base class) |
| Stage orchestrator | `bclearer_run_universe` | `BClearerRunUniverses` |
| Sub-stage orchestrator | `bclearer_run_universe` | `BClearerRunUniverses` |
| B-unit creation call | `bclearer_run_universe=bclearer_run_universe` | `BClearerRunUniverses` |

The runner may use a domain-specific variable name when creating the universe, but once
it is passed into the pipeline orchestrator, the parameter name becomes the generic
`bclearer_run_universe` and **stays the same through every stage and sub-stage**.

---

## Pipeline Design Workflow

The recommended sequence when designing a new bclearer pipeline:

```
Step 1: Design the Universes (inputs and outputs)
  - What registries does the Universe need?
  - What registers does each registry contain?
  - What types of content does each register hold?

Step 2: Design the Pipeline Topology (architecture)
  - Which of the 5 stages are needed?
  - What are the thin slices?
  - Are any stages complex enough to need sub-stages?
  - Which stages involve BIE identity construction?

Step 3: Define the B-units / Operations
  - One B-unit per atomic piece of work within each stage
  - Name each B-unit following stage-prefix convention
  - Decide: bare or object-passing?

Step 4: Build out B-units using data engineering skills
  - Implement each B-unit, beginning with stage 1c_collect
  - Delegate BIE domain work to bie-data-engineer
  - Wire orchestrators once B-units are complete
```

---

## Pipeline Configuration (CLI-driven)

New pipelines are scaffolded with the pipeline builder CLI:

```bash
# 1. Generate a sample config to start from
python -m bclearer_core.pipeline_builder sample --output my_config.json

# 2. Edit my_config.json to define your domain, pipelines, thin slices, stages, b-units

# 3. Scaffold the pipeline
python -m bclearer_core.pipeline_builder create --config my_config.json --output /path/to/output

# 4. Add new components to an existing pipeline
python -m bclearer_core.pipeline_builder update --config updated_config.json --pipeline path/to/domain_pipelines
```

### Configuration JSON structure

```json
{
  "domain_name": "example_domain",
  "b_unit_type": "b_units_with_object_passing_and_returning",
  "pipelines": [
    {
      "name": "pipeline_name",
      "thin_slices": [
        {
          "name": "thin_slice_1",
          "stages": [
            {
              "name": "1c_collect",
              "sub_stages": [],
              "b_units": ["ca_read_source", "cb_validate"]
            },
            {
              "name": "3e_evolve",
              "sub_stages": [
                {
                  "name": "parse_headers",
                  "b_units": ["ea1_b_unit", "ea2_b_unit"]
                }
              ],
              "b_units": []
            },
            {
              "name": "5r_reuse",
              "sub_stages": [],
              "b_units": ["ra_export_results"]
            }
          ]
        }
      ]
    }
  ]
}
```

`b_unit_type` choices:
- `"b_units"` — bare (default)
- `"b_units_with_object_passing_and_returning"` — object-passing (preferred for most pipelines)

---

## Generated Directory Structure

The CLI scaffolds this layout under `{domain_name}_pipelines/`:

```
{domain_name}_pipelines/
└── b_source/
    ├── common/
    │   └── operations/
    │       └── b_units/
    │           └── b_unit_creator_and_runner.py    ← create_and_run_b_unit()
    ├── app_runners/
    │   ├── {domain_name}_b_clearer_pipeline_b_application_runner.py  ← entry point
    │   └── runners/
    │       ├── {domain_name}_b_clearer_pipelines_runner.py            ← all pipelines
    │       └── {pipeline_name}_runner.py                               ← one pipeline
    └── {pipeline_name}/
        ├── objects/
        │   ├── enums/                              ← domain enums for the pipeline
        │   └── b_units/
        │       ├── {pipeline_name}_1c_collect/
        │       │   └── {bunit_name}_b_units.py
        │       ├── {pipeline_name}_2l_load/
        │       ├── {pipeline_name}_3e_evolve/
        │       ├── {pipeline_name}_4a_assimilate/
        │       └── {pipeline_name}_5r_reuse/
        └── orchestrators/
            ├── pipeline/
            │   └── {pipeline_name}_orchestrator.py
            ├── thin_slices/
            │   └── {thin_slice_name}_orchestrator.py
            ├── stages/
            │   ├── {pipeline_name}_1c_collect_orchestrator.py
            │   ├── {pipeline_name}_2l_load_orchestrator.py
            │   ├── {pipeline_name}_3e_evolve_orchestrator.py
            │   ├── {pipeline_name}_4a_assimilate_orchestrator.py
            │   └── {pipeline_name}_5r_reuse_orchestrator.py
            └── sub_stages/
                └── {pipeline_name}_{stage}_{sub_stage}/
                    └── {pipeline_name}_{stage}_{sub_stage}_orchestrator.py
```

Note: `bie/` folder (for BIE domain objects) is not scaffolded by the CLI — it is
created by `bie-data-engineer` under `{pipeline_name}/` when the pipeline requires
BIE identity construction.
