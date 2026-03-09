# Design Deliverables

The component ontologist produces 4 deliverables. Each must be completed before handoff to the data engineer.

## 1. BIE Component Object Types and Hierarchy

List all BIE entity types in the component with their inheritance relationships.

**Format:**

```
ComponentName BIE Object Types:
├── EntityTypeA (leaf)
├── EntityTypeB (leaf)
├── EntityTypeC (composite — contains EntityTypeA)
└── EntityTypeD (composite — contains EntityTypeB, EntityTypeC)
```

For each type, note:
- Whether it is a leaf or composite
- What it contains (if composite)
- Its real-world meaning

## 2. BIE Component Relation Types

Report BIE relation types in two tables. The first provides an overview of all available BIE relation types and whether the component uses them. The second provides detail only for the BIE relation types that are actually used.

Include BIE core relation types plus any component-specific extensions. Only define component-specific BIE relation types if the 7 core BIE relation types are insufficient.

### 2a. BIE Relation Types Usage

List every BIE relation type, its source, and how many times it is used in the component (0 if unused).

**Format:**

| Relation Type | Source | Usage Count |
|---------------|--------|-------------|
| BIE_TYPES_INSTANCES | Core | 1 |
| BIE_WHOLES_PARTS | Core | 3 |
| BIE_SUB_SUPER_SETS | Core | 0 |
| BIE_SAME_AS | Core | 0 |
| BIE_SUMMED | Core | 0 |
| BIE_SUMMING | Core | 0 |
| BIE_COUPLES | Core | 0 |
| GOVERNED_BY | Component | 1 |

### 2b. BIE Relation Types Usage Details

For each *used* relation type, list the participating object types. Only relation types with Usage Count > 0 appear here.

**Format:**

| Relation Type | Source | Usage in Component | place_1 (object type) | place_2 (object type) |
|---------------|--------|-----------------|------------------------|-----------------------|
| BIE_TYPES_INSTANCES | Core | Every workbook classified by type | Workbook | WorkbookType |
| BIE_WHOLES_PARTS | Core | Workbook contains worksheets | Workbook | Worksheet |
| BIE_WHOLES_PARTS | Core | Worksheet contains cells | Worksheet | Cell |
| BIE_WHOLES_PARTS | Core | Cell contains its source value | Cell | CellSourceValue |
| GOVERNED_BY | Component | Document governed by authority | Document | Authority |

## 3. BIE Object Type Identity Dependence Relation Types

For each BIE object type, specify which BIE relation types to other BIE object types its identity depends on. This captures the identity composition dependencies — i.e., what other object types must exist before this type's BIE identity can be computed.

This is the ontology-level view of identity composition. Implementation details (hash modes, specific BieIdCreationFacade calls) are deferred to the data engineer.

**Format:**

| Object Type | Depends On (object type) | Via Relation Type | Dependence Rationale |
|-------------|--------------------------|-------------------|----------------------|
| ColumnType | — | — | Leaf — identity from column name alone |
| RowType | — | — | Leaf — identity from row number alone |
| CoordinateType | RowType | BIE_WHOLES_PARTS | Row position is part of coordinate identity |
| CoordinateType | ColumnType | BIE_WHOLES_PARTS | Column position is part of coordinate identity |
| Workbook | (external file) | — | Identity from external file reference |
| Worksheet | Workbook | BIE_WHOLES_PARTS | Worksheet identity depends on owning workbook |
| Cell | Worksheet | BIE_WHOLES_PARTS | Cell identity depends on owning worksheet |
| Cell | CoordinateType | BIE_COUPLES | Cell identity depends on its coordinate |

Notes:
- Leaf types have no identity dependencies on other object types
- The "Via Relation Type" column shows which relation type connects this object type to the one it depends on
- This table drives the Construction Order (deliverable 4)

## 4. Construction Order

Specify the leaf-first ordering for constructing component entities, derived from the identity dependencies in deliverable 3.

**Format:**

```
Construction Order (leaf-first):
1. ColumnType (leaf — no dependencies)
2. RowType (leaf — no dependencies)
3. CoordinateType (depends on: RowType, ColumnType)
4. Workbook (depends on: file_bie_id from external)
5. Worksheet (depends on: Workbook)
6. Cell (depends on: Worksheet, CoordinateType)
```

Verify no circular dependencies exist.
