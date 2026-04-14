# bUnit Design Guidelines

Grounded in the bCLEARer Pipeline Architecture Framework
(`ol_bclearer_pdk/documentation/bclearer_pipeline_framework.md`) and the
bie_core_graph exemplar pipeline (`ol_bclearer_pdk/pipelines/bie_core_graph/`).

---

## Foundational Principles

### bUnits as Atomic Pipeline Components

In the bCLEARer Pipeline Architecture Framework (bCFAP), bUnits are the **leaf
nodes** of the multi-level nesting structure. They sit at the lowest boundary of
the pipeline architecture and cannot be further decomposed within the framework.

```
Pipeline  (root)
  └── Stage  (CLEAR boundary)
        └── Sub-Stage  (optional grouping)
              └── bUnit  (atomic leaf — indivisible)
```

Every bUnit is a **filter** in the pipe-and-filter architecture. It receives input
via pipes (Universe registers), applies exactly one transformation, and writes
output via pipes (Universe registers). Data flows acyclically through the pipeline
— bUnits never flow back to themselves.

### The Single Transformation Principle (STP)

The bCLEARer framework's Single Transformation Principle is the governing design
rule for bUnits:

> **Each bUnit performs one well-defined transformation — no more, no less.**

This is analogous to the Single Responsibility Principle (SRP) but scoped
specifically to data transformations in a pipeline context. A bUnit has exactly
one reason to change: its single transformation changes.

**What "single transformation" means in practice:**

| Acceptable (one transformation) | Violation (multiple transformations) |
|---------------------------------|--------------------------------------|
| Split a JSON object into key-value rows | Split JSON AND classify the resulting rows |
| Merge two DataFrames on a shared key | Merge DataFrames AND derive new columns |
| Read a file from disk into a string | Read a file AND parse JSON AND validate schema |
| Classify entities by type | Classify entities AND filter invalid ones |
| Materialise Neo4j node entities from structured data | Materialise nodes AND relationships together |

### Atomicity

A bUnit is **atomic** in two senses:

1. **Indivisible**: It is the smallest unit of work in the pipeline. If you can
   meaningfully decompose a bUnit into two sequential steps that each produce a
   useful intermediate result, it should be two bUnits.

2. **All-or-nothing**: A bUnit either completes its transformation or fails
   entirely. There is no partial execution — the output registers are populated
   completely or not at all.

### Separation of Transformation Concerns

Each bUnit handles exactly one transformation concern. This means:

- **No mixed I/O and logic**: A bUnit that reads a file should not also parse it.
  A bUnit that transforms data should not also write it to a database.
- **No mixed domain concerns**: A bUnit that processes nodes should not also
  process relationships. A bUnit that splits rows should not also merge columns.
- **No cross-stage responsibility**: A bUnit belongs to one and only one CLEAR
  stage. Its transformation must fall entirely within that stage's responsibility
  (see `references/stage-guidelines.md`).

### Immutability and Idempotence

- **Immutability**: bUnits write new output registers — they do not mutate input
  registers. The input data remains available at its gate for inspection.
- **Idempotence**: Running a bUnit twice with the same Universe state produces
  the same output. bUnits must not depend on external mutable state.

---

## bUnit Design Process

When designing bUnits for a new pipeline, follow this sequence:

### Step 1 — Identify the Transformations

For each stage in the pipeline topology, list every distinct transformation that
must happen. Each transformation should be expressible as a single sentence:

```
"Transform X into Y by doing Z"
```

If you need "and" in the sentence, you likely have two bUnits.

**Examples from bie_core_graph:**

- "Load JSON files from collected file paths into raw string content"
- "Wrap raw string content with BIE identity tracking metadata"
- "Split graph entities from JSON object sets into individual rows"
- "Classify graph entities into nodes and relationships"
- "Split classified entities into separate rows per entity"
- "Extract node IDs from JSON strings"
- "Materialise Neo4j node entities from structured node data"

### Step 2 — Verify Atomicity

For each candidate bUnit, apply the decomposition test:

> **Can this bUnit be split into two sequential bUnits where the intermediate
> result is meaningful and useful for inspection?**

- If **yes** — split it. The intermediate result becomes a gate point for
  transparency.
- If **no** — it is correctly atomic.

**Example — should split:**
> "Read JSON file and parse into DataFrame" → Split into:
> 1. "Read JSON file into raw string" (Load)
> 2. "Parse raw string into structured DataFrame" (Load)

**Example — should NOT split:**
> "Merge two DataFrames on BIE_ID column" — The intermediate state of a
> half-merged DataFrame has no meaningful interpretation.

### Step 3 — Verify Stage Assignment

Each bUnit must belong to exactly one CLEAR stage. Verify that its transformation
falls within the stage's responsibility:

| Stage | bUnit's transformation must... |
|-------|-------------------------------|
| `1c_collect` | Acquire data from outside the pipeline boundary only |
| `2l_load` | Computerise already-collected bytes into a source-shaped in-memory mirror only — no normalisation, no validation, no BIE-ing |
| `3e_evolve` | Apply business logic, enrichment, BIE identity assignment, or structural transformation only |
| `4a_assimilate` | Inject the evolved BIE fragment into the master BORO ontology object store (reconciling non-compliance) only |
| `5r_reuse` | Write results to external targets only |

If a bUnit's transformation spans two stages, it must be split across those
stages.

### Step 4 — Define Input/Output Contracts

For each bUnit, specify:

1. **Input registers** — which Universe registers it reads from (by enum)
2. **Output registers** — which Universe registers it writes to (by enum)
3. **Transformation description** — what the bUnit does to turn inputs into outputs

This forms the bUnit's **gate contract** — the input gate and output gate that
enable inspection and data object accounting.

### Step 5 — Name the bUnits

Follow the naming convention:

```
{stage_prefix}{sequence_letter}_{description}_b_units
```

| Stage | Prefix | Examples |
|-------|--------|----------|
| `1c_collect` | `c` | `ca_fetch_api_response_b_units` |
| `2l_load` | `l` | `la_read_json_file_b_units`, `lb_bieize_json_string_b_units` |
| `3e_evolve` | `e` | `ea_split_graph_entities_b_units` |
| `4a_assimilate` | `a` | `aa_assimilate_fragment_into_master_boro_store_b_units` |
| `5r_reuse` | `r` | `ra_write_to_neo4j_b_units` |

For sub-stages, extend the prefix: `ea1_`, `ea2_`, `eb1_`, etc.

The name should describe the transformation, not the implementation detail.

---

## bUnit Type Design — Generalisation Through Inheritance

### The Problem: Duplicated Transformation Patterns

As bclearer pipelines grow, common transformation patterns emerge across
pipelines. For example:

- Multiple pipelines may have a "read JSON file" bUnit
- Multiple pipelines may have a "split cell into rows" bUnit
- Multiple pipelines may have a "merge DataFrames on key" bUnit
- Multiple Evolve stages may have a "classify entities by type" bUnit

Without generalisation, each pipeline implements its own version of these
patterns, leading to:

- **Code duplication** across pipelines
- **Inconsistent behaviour** for the same logical transformation
- **Higher maintenance cost** when the pattern needs to change
- **Harder onboarding** as engineers must learn each pipeline's variant

### The Solution: bUnit Types

A **bUnit Type** is an abstract, reusable bUnit class that encapsulates a common
transformation pattern. Pipeline-specific bUnits inherit from the appropriate
bUnit Type and provide only the pipeline-specific configuration (dataset enums,
column names, domain-specific parameters).

```
BUnits[TUniverse]                          ← framework base (bclearer_core)
  └── {Pipeline}BUnits                     ← pipeline specialisation (post-processing hooks)
        └── {BUnitType}BUnits              ← reusable transformation pattern (NEW)
              └── {Pipeline}{Specific}BUnits ← pipeline-specific instance
```

### bUnit Type Design Principles

#### 1. Abstract the Transformation, Not the Domain

A bUnit Type captures the **shape of the transformation** — not the domain
objects it operates on. It should be parameterised by:

- Input/output dataset enums (what to read/write)
- Column names or keys (what fields to operate on)
- Transformation parameters (thresholds, mappings, split criteria)

It should NOT contain:

- Hard-coded dataset enums from any specific pipeline
- Domain-specific business rules
- Pipeline-specific post-processing logic

#### 2. Preserve the Single Transformation Principle

A bUnit Type must still represent exactly one transformation. Do not create
"super-types" that combine multiple transformations with feature flags.

**Good**: `CellToRowSliceBUnitType` — splits a cell column into individual rows
**Bad**: `DataTransformBUnitType` — does splitting OR merging OR filtering based
on a mode parameter

#### 3. Parameterise via Constructor, Not Configuration Files

bUnit Types receive their pipeline-specific parameters through constructor
arguments, not through external configuration files or environment variables.
This keeps the dependency explicit and type-safe.

```
# Conceptual pattern (not yet in codebase — guidance for future implementation)

class CellToRowSliceBUnits(PipelineBUnits):
    """Reusable bUnit Type: splits a cell column into individual rows."""
    
    def __init__(self,
                 universe,
                 input_dataset_enum,
                 output_dataset_enum,
                 cell_column_name,
                 ...):
        ...
    
    def b_unit_process_function(self):
        # Generic cell-to-row-slice logic using parameterised enums/columns
        ...
```

#### 4. Layer the Inheritance Correctly

The inheritance hierarchy should follow:

```
BUnits[TUniverse]                      ← framework (bclearer_core)
  └── CoreGraphBUnits                  ← pipeline base (post-processing hooks)
        └── CellToRowSliceBUnits       ← bUnit Type (reusable transformation)
              └── CellToRowSliceJsonNeo4jGraphsToGraphEntitiesBUnits
                                       ← concrete pipeline bUnit (specific enums)
```

The pipeline base class (`CoreGraphBUnits`) handles pipeline-specific concerns
like BIE registration and post-processing. The bUnit Type handles the generic
transformation logic. The concrete bUnit provides only the specific dataset
enums and column names.

#### 5. Place bUnit Types in the Core Library

Reusable bUnit Types should live in the core library, not in any specific
pipeline:

```
libraries/core/bclearer_core/objects/b_units/
  ├── b_units.py                       ← base BUnits class
  └── types/                           ← reusable bUnit Types (NEW)
      ├── cell_to_row_slice_b_units.py
      ├── row_split_by_column_values_b_units.py
      ├── row_merge_b_units.py
      ├── dataframe_join_b_units.py
      └── ...
```

Pipeline-specific bUnits then inherit from these types and live in their
pipeline's `objects/b_units/` directory as usual.

---

## Identifying bUnit Types from Existing Code

### Recognition Heuristics

When reviewing existing bclearer pipelines, look for these indicators of
candidate bUnit Types:

#### 1. Structural Similarity

Two or more bUnits across pipelines (or within a pipeline) that:
- Call the same helper function or a very similar one
- Differ only in which dataset enums and column names they pass
- Have the same shape of `b_unit_process_function()` body

**Exemplar pattern from bie_core_graph:**

The following bUnits all call a "cell-to-row-slice" helper with different
parameters:
- `CellToRowSliceJsonNeo4jGraphsToGraphEntitiesBUnits`
- `CellToRowSliceJsonNeo4jClassifiedGraphEntitiesToNodesBUnits`
- `CellToRowSliceJsonNeo4jClassifiedGraphEntitiesToRelationshipsBUnits`

These are candidates for a `CellToRowSliceBUnits` type.

#### 2. Naming Pattern Similarity

bUnits whose names follow the same pattern with different domain nouns:
- `RowSplitJsonNeo4jNodeKeyValuesBUnits`
- `RowSplitJsonNeo4jRelationshipKeyValuesBUnits`
- `RowSplitJsonNeo4jClassifiedGraphEntitiesBUnits`

The "RowSplit" pattern is the reusable transformation; the domain noun varies.

#### 3. Helper Function Reuse

A single helper function called by multiple bUnits with different parameters
is a strong signal. The helper function's signature often defines the natural
parameterisation of the bUnit Type:

```python
# This helper is called by multiple bUnits with different enum arguments
split_row_by_column_values(
    domain_dataset_wrapper_register=...,
    input_json_object_sets_dataset_enum=...,      # varies per bUnit
    column_names_dictionary=...,                    # varies per bUnit
    output_..._dataset_enum=...,                    # varies per bUnit
)
```

The varying parameters become constructor arguments of the bUnit Type.

---

## Review Mode: bUnit Type Identification and Design

### Purpose

When reviewing an existing bclearer pipeline in **Review/Refactor Mode**, use
this checklist to identify opportunities for bUnit Type extraction.

### bUnit Type Identification Checklist

| Check | Question | If Yes |
|-------|----------|--------|
| **Structural duplication** | Do two or more bUnits have nearly identical `b_unit_process_function()` bodies, differing only in enum/column parameters? | Candidate for bUnit Type extraction |
| **Helper function fan-in** | Does a single helper function serve multiple bUnits with different parameters? | The helper's parameter signature suggests the bUnit Type interface |
| **Cross-pipeline similarity** | Does another pipeline have bUnits that perform the same transformation shape on different data? | Candidate for a shared bUnit Type in the core library |
| **Name pattern clustering** | Do multiple bUnit names share a common verb/pattern (e.g., "RowSplit", "CellToRowSlice", "RowMerge")? | The shared pattern names the bUnit Type |
| **Copy-paste evolution** | Was a bUnit created by copying another and changing enums/columns? | Strong signal for bUnit Type extraction |

### bUnit Type Design Deliverable

When identifying bUnit Types during review, produce:

```
bUnit Type: {TypeName}BUnits
  Transformation: {single-sentence description}
  Parameters:
    - {param_1}: {description} (e.g., input_dataset_enum)
    - {param_2}: {description} (e.g., output_dataset_enum)
    - {param_3}: {description} (e.g., column_names)
  Instances Found:
    - {Pipeline1}/{ConcreteUnit1} (enums: X, Y, Z)
    - {Pipeline1}/{ConcreteUnit2} (enums: A, B, C)
    - {Pipeline2}/{ConcreteUnit3} (enums: D, E, F)
  Proposed Location: libraries/core/bclearer_core/objects/b_units/types/
  Refactoring Impact: {number} bUnits across {number} pipelines
```

### Refactoring Workflow

Once bUnit Types are identified and approved:

```
Step 1: Design the bUnit Type interface
  - Define the constructor parameters (what varies between instances)
  - Define the transformation logic (what is common)
  - Define the trace configuration pattern (if applicable)

Step 2: Implement the bUnit Type in the core library
  - Create the abstract bUnit Type class
  - Implement the generic b_unit_process_function()
  - Extract and parameterise the helper function logic

Step 3: Refactor concrete bUnits to inherit from the type
  - Replace b_unit_process_function() body with constructor parameterisation
  - Verify each concrete bUnit's behaviour is preserved
  - Run stage-level and pipeline-level tests

Step 4: Verify gate contracts are unchanged
  - Input/output registers must remain identical
  - Data lineage traces must remain identical
  - BIE registration behaviour must remain identical
```

---

## Design Quality Checklist

When reviewing bUnit designs, verify each bUnit against:

| Principle | Question | Expected |
|-----------|----------|----------|
| **Single Transformation** | Does this bUnit perform exactly one transformation? | Yes — describable in one sentence without "and" |
| **Atomicity** | Can this bUnit be meaningfully decomposed? | No — intermediate state would not be useful |
| **Stage assignment** | Does the transformation fall within its CLEAR stage? | Yes — no cross-stage responsibility |
| **Input/output contract** | Are input and output registers clearly defined? | Yes — by enum, with types specified |
| **Immutability** | Does the bUnit write new registers, not mutate inputs? | Yes — inputs remain available at gate |
| **Idempotence** | Does rerunning with same state produce same output? | Yes — no external mutable dependencies |
| **Naming** | Does the name describe the transformation? | Yes — follows `{prefix}{letter}_{description}` convention |
| **Type candidacy** | Is this transformation pattern reusable across pipelines? | If yes — document as bUnit Type candidate |
| **Loose coupling** | Does this bUnit depend only on Universe registers? | Yes — no direct imports from other bUnits |
| **Tight cohesion** | Is everything in this bUnit related to its single transformation? | Yes — no unrelated helper logic |

---

## Exemplar Reference: bie_core_graph

The bie_core_graph pipeline demonstrates these principles throughout:

### Atomicity in Practice

The Evolve stage decomposes Neo4j JSON processing into 16+ bUnits, each
performing exactly one transformation:

```
3e_evolve_2 (JSON parsing — 13 bUnits):
  ├── Split graph entities from JSON sets          (cell-to-row)
  ├── Classify entities into nodes/relationships   (cell-to-column)
  ├── Split classified entities into rows           (row-split)
  ├── Extract node objects from JSON                (cell-to-row)
  ├── Extract relationship objects from JSON        (cell-to-row)
  ├── Split node key-values                         (row-split)
  ├── Split relationship key-values                 (row-split)
  ├── Extract node IDs                              (json-string-parse)
  ├── Extract node labels                           (json-string-parse)
  ├── Extract node properties                       (json-string-parse)
  ├── Extract relationship IDs                      (json-string-parse)
  ├── Merge node components                         (row-merge)
  └── Merge relationship components                 (row-merge)

3e_evolve_3 (Entity materialisation — 3 bUnits):
  ├── Materialise Neo4j graph entities
  ├── Materialise Neo4j node entities
  └── Materialise Neo4j relationship entities
```

Each bUnit produces an inspectable intermediate result at its output gate. This
enables:
- **Transparency**: Inspect data at any transformation step
- **Problem isolation**: Find the first gate where an issue appears
- **Independent testing**: Test each transformation in isolation
- **Evolution safety**: Change one transformation without affecting others

### bUnit Type Candidates Visible in the Exemplar

| Pattern | Instances | Candidate Type |
|---------|-----------|---------------|
| Cell-to-row slice | 3 bUnits | `CellToRowSliceBUnits` |
| Row split by column values | 3 bUnits | `RowSplitByColumnValuesBUnits` |
| JSON string parse | 4 bUnits | `JsonStringParseBUnits` |
| Row merge | 2 bUnits | `RowMergeBUnits` |
| Entity materialisation | 3 bUnits | `EntityMaterialisationBUnits` |
