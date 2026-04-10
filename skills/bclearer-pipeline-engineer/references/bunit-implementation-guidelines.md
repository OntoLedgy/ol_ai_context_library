# bUnit Implementation Guidelines

Grounded in the bCLEARer Pipeline Architecture Framework
(`ol_bclearer_pdk/documentation/bclearer_pipeline_framework.md`), the base
`BUnits` class (`ol_bclearer_pdk/libraries/core/bclearer_core/objects/b_units/b_units.py`),
and the bie_core_graph exemplar pipeline.

---

## bUnit Fundamentals

### What a bUnit Is

A bUnit is the **atomic unit of work** in a bclearer pipeline. It is a leaf node
in the pipeline's nesting hierarchy — the smallest indivisible component. Every
bUnit implements exactly one transformation following the Single Transformation
Principle (STP).

### The Base Class: `BUnits[TUniverse]`

All bUnits inherit from the generic abstract base class `BUnits[TUniverse]` in
`bclearer_core.objects.b_units.b_units`. It supports three usage levels:

| Level | Constructor Pattern | When to Use |
|-------|-------------------|-------------|
| **Level 0** (Bare) | `BUnits()` | Simple, stateless bUnit — no Universe, no BIE tracking |
| **Level 1** (Universe) | `BUnits(input_object=universe)` | bUnit needs Universe access but no BIE domain tracking |
| **Level 2** (Full BIE) | `BUnits(input_object=universe, b_unit_bie_enum=..., parent_bie_pipeline_component_enum=...)` | Full BIE identity and domain configuration with post-processing hooks |

**Level 2 is the standard for production pipelines** — it provides full data
lineage tracking, BIE registration, and pipeline component hierarchy.

### Execution Flow

```
bunit.run()
  └── _run_b_unit()                    [@run_and_log_function decorator]
        ├── b_unit_process_function()  [YOUR implementation — abstract]
        └── _post_process()            [called if domain configuration exists]
```

- `b_unit_process_function()` — **You implement this.** Contains the single
  transformation logic.
- `_post_process()` — Override in the pipeline base class (e.g., `CoreGraphBUnits`)
  to register outputs in the domain universe and BIE tracking universe. You do
  NOT override this in individual bUnits.

---

## Implementing a bUnit

### Step 1 — Create the Pipeline Base Class

Each pipeline defines a base bUnit class that specialises `BUnits[TUniverse]`
for the pipeline's Universe type and provides standard post-processing hooks.

**Pattern (from bie_core_graph exemplar):**

```python
# {pipeline_name}/objects/b_units/b_units.py

from bclearer_core.objects.b_units.b_units import BUnits
from bclearer_orchestration_services.identification_services \
    .b_identity_ecosystem.pipeline.universes \
    .b_clearer_run_universes import (
    BClearerRunUniverses,
)


class CoreGraphBUnits(
        BUnits[BClearerRunUniverses]):

    def __init__(
            self,
            bclearer_run_universe: BClearerRunUniverses,
            b_unit_bie_enum: BieEnums,
            parent_bie_pipeline_component_enum: BieEnums) \
            -> None:
        super().__init__(
            input_object=bclearer_run_universe,
            b_unit_bie_enum=b_unit_bie_enum,
            parent_bie_pipeline_component_enum=\
                parent_bie_pipeline_component_enum)

    def _post_process(
            self) \
            -> None:
        register_output_domain_dataframes_in_domain_universe(
            b_unit_domain_configuration=\
                self.b_unit_domain_configuration,
            domain_dataset_wrapper_register=\
                self.input_object.universe_graph_content
                    .domain_dataset_wrapper_register)

        if self.b_unit_domain_configuration.b_unit_bie_enum \
                != BClearerNeo4jEntificationBunits.LOAD_NEO4J:
            register_in_parallel_bie_universe(
                b_unit_domain_configuration=\
                    self.b_unit_domain_configuration,
                bclearer_run_universe=\
                    self.input_object)
```

**Key points:**
- One pipeline base class per pipeline (not per stage)
- Parameterises `BUnits` with the pipeline's Universe type
- `_post_process()` handles domain registration — concrete bUnits never touch this
- All concrete bUnits in this pipeline inherit from this class

### Step 2 — Define the bUnit Enum

Every bUnit must be registered in the pipeline's bUnit enum. This enum provides
the bUnit's identity in the BIE domain tracking system.

```python
# {pipeline_name}/objects/enums/reportable/bclearer_{pipeline_name}_bunits.py

from bclearer_orchestration_services.identification_services \
    .b_identity_ecosystem.common.objects.enums.bie_enums import (
    BieEnums,
)


class BClearerNeo4jEntificationBunits(
        BieEnums):
    LOAD_NEO4J = auto()
    BIEIZE_NEO4J = auto()
    CELL_TO_ROW_SLICE_JSON_NEO4J_GRAPHS_TO_GRAPH_ENTITIES = auto()
    # ... one entry per bUnit
```

### Step 3 — Implement the Concrete bUnit

Each concrete bUnit follows a strict pattern:

```python
# {pipeline_name}/objects/b_units/{pipeline_name}_{stage_name}/
#     {prefix}{letter}_{description}_b_units.py

from {pipeline_path}.objects.b_units.b_units import (
    CoreGraphBUnits,
)
from {pipeline_path}.objects.enums.reportable \
    .bclearer_neo4j_entification_bunits import (
    BClearerNeo4jEntificationBunits,
)


class CellToRowSliceJsonNeo4jGraphsToGraphEntitiesBUnits(
        CoreGraphBUnits):

    def __init__(
            self,
            bclearer_run_universe: BClearerRunUniverses,
            parent_bie_pipeline_component_enum: BieEnums) \
            -> None:
        super().__init__(
            bclearer_run_universe=bclearer_run_universe,
            b_unit_bie_enum=\
                BClearerNeo4jEntificationBunits
                    .CELL_TO_ROW_SLICE_JSON_NEO4J_GRAPHS_TO_GRAPH_ENTITIES,
            parent_bie_pipeline_component_enum=\
                parent_bie_pipeline_component_enum)

    def b_unit_process_function(
            self) \
            -> None:
        self.b_unit_domain_configuration \
            .b_unit_input_output_lists = \
            split_neo4j_graph_json_object_sets_into_graph_entities(
                domain_dataset_wrapper_register=\
                    self.input_object.universe_graph_content
                        .domain_dataset_wrapper_register,
                input_dataset_enum=\
                    BClearerNeo4JBDatasetsLoad
                        .AB_JSON_NEO4J_GRAPHS_JSON_OBJECT_SETS_TABLE,
                output_dataset_enum=\
                    BClearerNeo4JBDatasetsEvolve2
                        .DA_JSON_NEO4J_GRAPH_ENTITIES_JSON_OBJECTS_TABLE)

        self.__setup_trace_configuration()

    def __setup_trace_configuration(
            self) \
            -> None:
        trace_configuration = \
            BUnitDomainDataItemTraceConfigurations(
                dataset_base_bie_enum=\
                    BClearerNeo4JBDatasetsEvolve2
                        .DA_JSON_NEO4J_GRAPH_ENTITIES_JSON_OBJECTS_TABLE,
                data_trace_from_domain_column_name=\
                    BClearerNeo4JEntificationColumnNames
                        .OWNING_NEO4J_GRAPH_BIE_IDS.b_enum_item_name,
                data_trace_to_domain_column_name=\
                    BieColumnNames.BIE_IDS.b_enum_item_name)

        self.b_unit_domain_configuration \
            .b_unit_domain_data_item_trace_configurations \
            .append(trace_configuration)
```

**Anatomy of `b_unit_process_function()`:**

1. **Call a helper function** that performs the actual transformation — the bUnit
   delegates the work, it does not contain raw transformation logic inline
2. **Assign the result** to `self.b_unit_domain_configuration.b_unit_input_output_lists`
   — this is a `BUnitInputOutputLists` containing input dataset enums and output
   DataFrames
3. **Optionally set up trace configurations** for data lineage tracking via
   `BUnitDomainDataItemTraceConfigurations`

**Rules for `b_unit_process_function()`:**
- Must populate `b_unit_input_output_lists` (required for BIE registration)
- Must NOT perform I/O directly — delegate to helper functions
- Must NOT access `os.getenv()` or external configuration
- Must NOT import or call other bUnits
- Must NOT mutate input Universe registers — only write new output registers
- Trace configuration is optional but recommended for data lineage

### Step 4 — Register in Orchestrator via `create_and_run_b_unit()`

bUnits are **never instantiated directly**. Always use the factory function:

```python
# orchestrators/stages/{pipeline_name}_{stage_name}_orchestrator.py

@run_and_log_function()
def orchestrate_neo4j_entification_2l_load(
        bclearer_run_universe: BClearerRunUniverses,
        parent_pipeline_component_enum: BieEnums) \
        -> None:
    pipeline_component_enum = \
        set_and_log_pipeline_component_enum(
            bie_pipeline_component_enum=\
                BClearerStageBieEnums.B_LOAD,
            parent_bie_pipeline_component_enum=\
                parent_pipeline_component_enum)

    __run_contained_bie_pipeline_components(
        bclearer_run_universe=bclearer_run_universe,
        parent_pipeline_component_enum=pipeline_component_enum)

    summarise_bie_pipeline_component(...)


def __run_contained_bie_pipeline_components(
        bclearer_run_universe: BClearerRunUniverses,
        parent_pipeline_component_enum: BieEnums) \
        -> None:
    create_and_run_b_unit(
        b_unit_type=LoadJsonFileAsStringBUnits,
        bclearer_run_universe=bclearer_run_universe,
        parent_bie_pipeline_component_enum=\
            parent_pipeline_component_enum)

    create_and_run_b_unit(
        b_unit_type=BieizeJsonStringBUnits,
        bclearer_run_universe=bclearer_run_universe,
        parent_bie_pipeline_component_enum=\
            parent_pipeline_component_enum)
```

**The `create_and_run_b_unit()` function:**

```python
# common/operations/b_units/b_unit_creator_and_runner.py

def create_and_run_b_unit(
        b_unit_type,
        bclearer_run_universe: BClearerRunUniverses,
        parent_bie_pipeline_component_enum: BieEnums) \
        -> None:
    b_unit = \
        b_unit_type(
            bclearer_run_universe=bclearer_run_universe,
            parent_bie_pipeline_component_enum=\
                parent_bie_pipeline_component_enum)

    b_unit.run()
```

---

## The Domain Configuration System

### BUnitDomainConfigurations

Created automatically when a bUnit is initialised with `b_unit_bie_enum`. Holds:

| Property | Type | Purpose |
|----------|------|---------|
| `b_unit_bie_enum` | `BieEnums` | This bUnit's identity in the BIE system |
| `parent_bie_pipeline_component_enum` | `BieEnums` | Parent stage/sub-stage in the hierarchy |
| `b_unit_input_output_lists` | `BUnitInputOutputLists` | Input dataset enums + output DataFrames |
| `b_unit_domain_data_item_trace_configurations` | `list[BUnitDomainDataItemTraceConfigurations]` | Data lineage trace definitions |

### BUnitInputOutputLists

Returned by the helper function called in `b_unit_process_function()`:

```python
class BUnitInputOutputLists:
    b_unit_input_domain_dataset_enum_list: list[BieEnums]
    b_unit_output_domain_dataset_dictionary: dict[BieEnums, DataFrame]
```

- **Input list**: Which dataset enums were read as input
- **Output dict**: Mapping from output dataset enum to the resulting DataFrame

### BUnitDomainDataItemTraceConfigurations

Defines a single data lineage trace — connecting a column in the output dataset
back to a column in a source dataset:

```python
class BUnitDomainDataItemTraceConfigurations:
    dataset_base_bie_enum: BieEnums           # which dataset this trace is for
    data_trace_from_domain_column_name: str   # source column name
    data_trace_to_domain_column_name: str     # target column name (usually BIE_IDS)
```

---

## Implementing bUnit Types — Generalisation Pattern

### When to Create a bUnit Type

Create a bUnit Type when you identify two or more concrete bUnits (within or
across pipelines) that:

1. Call the same or structurally identical helper function
2. Differ only in dataset enums, column names, or similar parameters
3. Perform the same shape of transformation on different data

### Implementation Pattern

#### Step 1 — Define the bUnit Type

Place in the core library under `objects/b_units/types/`:

```python
# libraries/core/bclearer_core/objects/b_units/types/
#     cell_to_row_slice_b_units.py

from abc import abstractmethod
from bclearer_core.objects.b_units.b_units import BUnits


class CellToRowSliceBUnits(
        BUnits[TUniverse]):
    """Reusable bUnit Type: splits a cell column into individual rows.

    Subclasses provide pipeline-specific dataset enums and column names
    via constructor arguments. The transformation logic is generic.
    """

    def __init__(
            self,
            input_object: TUniverse,
            input_dataset_enum: BieEnums,
            output_dataset_enum: BieEnums,
            cell_column_name: str,
            row_id_column_name: str,
            b_unit_bie_enum: BieEnums = None,
            parent_bie_pipeline_component_enum: BieEnums = None) \
            -> None:
        super().__init__(
            input_object=input_object,
            b_unit_bie_enum=b_unit_bie_enum,
            parent_bie_pipeline_component_enum=\
                parent_bie_pipeline_component_enum)

        self._input_dataset_enum = input_dataset_enum
        self._output_dataset_enum = output_dataset_enum
        self._cell_column_name = cell_column_name
        self._row_id_column_name = row_id_column_name

    def b_unit_process_function(
            self) \
            -> None:
        self.b_unit_domain_configuration \
            .b_unit_input_output_lists = \
            split_cell_into_rows(
                domain_dataset_wrapper_register=\
                    self._get_domain_dataset_wrapper_register(),
                input_dataset_enum=self._input_dataset_enum,
                output_dataset_enum=self._output_dataset_enum,
                cell_column_name=self._cell_column_name,
                row_id_column_name=self._row_id_column_name)

    @abstractmethod
    def _get_domain_dataset_wrapper_register(self):
        """Override to return the pipeline-specific register."""
        ...
```

#### Step 2 — Create the Pipeline-Specific Intermediate Class

The pipeline base class still provides post-processing hooks:

```python
# {pipeline}/objects/b_units/types/cell_to_row_slice_b_units.py

class CoreGraphCellToRowSliceBUnits(
        CellToRowSliceBUnits[BClearerRunUniverses]):
    """Pipeline-specific specialisation of CellToRowSliceBUnits."""

    def __init__(
            self,
            bclearer_run_universe: BClearerRunUniverses,
            input_dataset_enum: BieEnums,
            output_dataset_enum: BieEnums,
            cell_column_name: str,
            row_id_column_name: str,
            b_unit_bie_enum: BieEnums,
            parent_bie_pipeline_component_enum: BieEnums) \
            -> None:
        super().__init__(
            input_object=bclearer_run_universe,
            input_dataset_enum=input_dataset_enum,
            output_dataset_enum=output_dataset_enum,
            cell_column_name=cell_column_name,
            row_id_column_name=row_id_column_name,
            b_unit_bie_enum=b_unit_bie_enum,
            parent_bie_pipeline_component_enum=\
                parent_bie_pipeline_component_enum)

    def _get_domain_dataset_wrapper_register(self):
        return self.input_object.universe_graph_content \
            .domain_dataset_wrapper_register

    def _post_process(self) -> None:
        register_output_domain_dataframes_in_domain_universe(...)
        register_in_parallel_bie_universe(...)
```

#### Step 3 — Refactor Concrete bUnits to Inherit from the Type

```python
# Before (direct implementation):
class CellToRowSliceJsonNeo4jGraphsToGraphEntitiesBUnits(CoreGraphBUnits):
    def b_unit_process_function(self):
        self.b_unit_domain_configuration.b_unit_input_output_lists = \
            split_neo4j_graph_json_object_sets_into_graph_entities(
                domain_dataset_wrapper_register=...,
                input_dataset_enum=BClearerNeo4JBDatasetsLoad.AB_...,
                output_dataset_enum=BClearerNeo4JBDatasetsEvolve2.DA_...)

# After (inheriting from bUnit Type):
class CellToRowSliceJsonNeo4jGraphsToGraphEntitiesBUnits(
        CoreGraphCellToRowSliceBUnits):
    def __init__(self, bclearer_run_universe, parent_bie_pipeline_component_enum):
        super().__init__(
            bclearer_run_universe=bclearer_run_universe,
            input_dataset_enum=BClearerNeo4JBDatasetsLoad.AB_...,
            output_dataset_enum=BClearerNeo4JBDatasetsEvolve2.DA_...,
            cell_column_name=BClearerNeo4JEntificationColumnNames.GRAPH_ENTITIES,
            row_id_column_name=BieColumnNames.BIE_IDS,
            b_unit_bie_enum=BClearerNeo4jEntificationBunits.CELL_TO_ROW_SLICE_...,
            parent_bie_pipeline_component_enum=parent_bie_pipeline_component_enum)
```

The concrete bUnit now contains **zero transformation logic** — only pipeline-
specific parameter binding. The transformation is fully encapsulated in the
bUnit Type.

---

## Review/Refactor Mode: bUnit Type Extraction

### Purpose

When reviewing existing bclearer pipeline code, identify bUnits that should be
refactored into reusable bUnit Types.

### Identification Process

#### 1. Catalogue the bUnits

List all bUnits in the pipeline with their:
- Class name
- Helper function called in `b_unit_process_function()`
- Parameters passed to the helper function
- Input/output dataset enums

#### 2. Group by Helper Function

Group bUnits that call the same helper function (or structurally identical
functions). Each group is a candidate bUnit Type.

#### 3. Extract the Varying Parameters

For each group, identify which parameters vary between bUnits. These become the
bUnit Type's constructor parameters.

#### 4. Verify STP Preservation

Ensure the proposed bUnit Type still represents a single transformation. If the
helper function has mode parameters or feature flags that change its behaviour
fundamentally, it may represent multiple bUnit Types rather than one.

### Refactoring Checklist

| Step | Action | Verification |
|------|--------|-------------|
| Catalogue | List all bUnits with helper functions and parameters | Complete inventory |
| Group | Cluster by transformation pattern | Each group has 2+ members |
| Design | Define bUnit Type interface (constructor params) | Parameters cover all variation |
| Implement | Create bUnit Type class in core library | Generic transformation logic works |
| Specialise | Create pipeline intermediate class | Post-processing hooks correct |
| Refactor | Update concrete bUnits to inherit from type | All tests pass |
| Verify gates | Confirm input/output registers unchanged | Data flow identical |
| Verify traces | Confirm data lineage traces unchanged | BIE registration identical |
| Cross-pipeline | Check if other pipelines can use this type | Document reuse opportunities |

---

## Common Patterns and Templates

### Pattern: bUnit with Trace Configuration

Most Evolve bUnits need data lineage tracing:

```python
def b_unit_process_function(self):
    self.b_unit_domain_configuration.b_unit_input_output_lists = \
        helper_function(
            domain_dataset_wrapper_register=...,
            input_dataset_enum=...,
            output_dataset_enum=...)

    self.__setup_trace_configuration()

def __setup_trace_configuration(self):
    trace_configuration = BUnitDomainDataItemTraceConfigurations(
        dataset_base_bie_enum=...,
        data_trace_from_domain_column_name=...,
        data_trace_to_domain_column_name=BieColumnNames.BIE_IDS.b_enum_item_name)

    self.b_unit_domain_configuration \
        .b_unit_domain_data_item_trace_configurations.append(
            trace_configuration)
```

### Pattern: bUnit without Trace Configuration

Simple transformations (especially in Load or late Evolve) may not need tracing:

```python
def b_unit_process_function(self):
    self.b_unit_domain_configuration.b_unit_input_output_lists = \
        helper_function(
            domain_dataset_wrapper_register=...,
            input_dataset_enum=...,
            output_dataset_enum=...)
```

### Pattern: bUnit with Multiple Output Datasets

Some transformations produce multiple outputs (e.g., row-split):

```python
def b_unit_process_function(self):
    self.b_unit_domain_configuration.b_unit_input_output_lists = \
        split_row_by_column_values(
            domain_dataset_wrapper_register=...,
            input_json_object_sets_dataset_enum=...,
            column_names_dictionary={
                ColumnNameEnum.KEY: ['"id"', '"labels"', '"properties"']},
            output_ids_dataset_enum=...,
            output_labels_dataset_enum=...,
            output_properties_dataset_enum=...)
```

This is still a single transformation (row-split) — the multiple outputs are
inherent to the operation, not a sign of multiple responsibilities.

---

## Implementation Verification Checklist

After implementing a bUnit, verify:

| Check | Expected |
|-------|----------|
| Inherits from pipeline base class (e.g., `CoreGraphBUnits`) | Yes |
| Constructor calls `super().__init__()` with correct enums | Yes |
| `b_unit_process_function()` populates `b_unit_input_output_lists` | Yes |
| Helper function handles actual transformation (not inline logic) | Yes |
| No direct I/O in `b_unit_process_function()` | Yes |
| No `os.getenv()` or external config access | Yes |
| No imports from other bUnits | Yes |
| No mutation of input registers | Yes |
| bUnit enum registered in pipeline's bUnit enum class | Yes |
| bUnit registered in orchestrator via `create_and_run_b_unit()` | Yes |
| Never instantiated directly (always via factory) | Yes |
| File placed in correct stage directory | Yes |
| File and class follow naming conventions | Yes |
| Trace configuration set up (if data lineage needed) | Yes |
| Single transformation only — no "and" in description | Yes |
