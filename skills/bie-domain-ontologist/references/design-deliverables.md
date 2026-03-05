# Design Deliverables

The domain ontologist produces 4 deliverables. Each must be completed before handoff to the data engineer.

## 1. Domain Object Types and Hierarchy

List all entity types in the domain with their inheritance relationships.

**Format:**

```
DomainName Object Types:
├── EntityTypeA (leaf)
├── EntityTypeB (leaf)
├── EntityTypeC (composite — contains EntityTypeA)
└── EntityTypeD (composite — contains EntityTypeB, EntityTypeC)
```

For each type, note:
- Whether it is a leaf or composite
- What it contains (if composite)
- Its real-world meaning

## 2. Domain Relation Types

For each relation in the domain, list the object types that participate and the relation type that connects them. This makes explicit which object types relate to which other object types and through what relation type.

Include core relation types used by the domain plus any domain-specific extensions. Only define domain-specific relation types if the 7 core types are insufficient.

**Format:**

| Relation Type | Source | Usage in Domain | place_1 (object type) | place_2 (object type) |
|---------------|--------|-----------------|------------------------|-----------------------|
| BIE_TYPES_INSTANCES | Core | Every workbook classified by type | Workbook | WorkbookType |
| BIE_WHOLES_PARTS | Core | Workbook contains worksheets | Workbook | Worksheet |
| BIE_WHOLES_PARTS | Core | Worksheet contains cells | Worksheet | Cell |
| BIE_WHOLES_PARTS | Core | Cell contains its source value | Cell | CellSourceValue |
| GOVERNED_BY | Domain | Document governed by authority | Document | Authority |

## 3. Object Type Identity Dependence Relation Types

For each object type, specify which relation types to other object types its identity depends on. This captures the identity composition dependencies — i.e., what other object types must exist before this type's BIE identity can be computed.

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

Specify the leaf-first ordering for constructing domain entities, derived from the identity dependencies in deliverable 3.

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
