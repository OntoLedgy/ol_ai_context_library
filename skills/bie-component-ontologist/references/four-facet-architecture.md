# Four-Facet Architecture

The BIE framework is organized along two axes, producing four facets:

|                    | Model (Design)                          | Implementation (Code)                     |
|--------------------|-----------------------------------------|-------------------------------------------|
| **Foundation**     | Core object model, type system, enums   | BieIds, BieEnums, BieIdCreationFacade     |
| **Domain**         | Domain object types, relation types     | Domain enums, creators, object classes    |

- **Foundation Model** — The abstract type system: BieTypes, BieRelationTypes, BieCoreRelationTypes, BieEnums self-identification
- **Foundation Implementation** — The code infrastructure: BieIdCreationFacade, BieIdRegistries, BieIdUniverses, BieObjects, hashing pipeline
- **Domain Model** — The ontology for a specific domain: object types, relation types, calculation table, construction order
- **Domain Implementation** — The Python code for a specific domain: domain enums, bie_id creators, BieDomainObjects subclasses

The ontologist skill can review or design ontologies for **either** foundation or domain components. The four-facet names above are formal architectural terms.

## Two Fundamental Kinds

A BIE ontology has two fundamental kinds:

1. **Objects** — Entities within a component. Each object has a `bie_id` (BIE identifier). Stored in the objects register.
2. **Relations** — Links between things. Each relation is a `bie_id_tuple` — an ordered tuple of bie_ids representing participants and relation type. Stored in the relations register.

## Core Relation Types (BieCoreRelationTypes)

| Relation | Semantics |
|----------|-----------|
| `BIE_TYPES_INSTANCES` | Type-to-instance classification |
| `BIE_WHOLES_PARTS` | Composition (whole contains part) |
| `BIE_SUB_SUPER_SETS` | Subset-superset classification |
| `BIE_SAME_AS` | Identity equivalence |
| `BIE_SUMMED` | Aggregation target |
| `BIE_SUMMING` | Aggregation source |
| `BIE_COUPLES` | Paired/coupled entities |

Domains may define additional relation types by extending `BieRelationTypes`.

## Identity Composition Principles

1. **Deterministic** — Same inputs always produce the same BIE ID via BLAKE2B hashing (order-sensitive) or integer summation (order-insensitive)
2. **Type-first convention** — When composing identity, the type's `item_bie_identity` is typically the first input
3. **Parts before wholes** — Leaf entities must be constructed before their containing composites
4. **Domain typing** — When a `bie_domain_type` is provided, the final identity = `order_sensitive([type.item_bie_identity, vector_bie_id])`

## Object Construction Pattern

Each component object follows this pattern during `__init__`:

```
1. Compute bie_id — call BieIdCreationFacade with type + inputs
2. Init super — super().__init__(bie_id=, base_hr_name=, bie_type=)
3. Register Level 1 — register object + type-instance relation in infrastructure registry
4. Create bie_id_tuples — register all relations (wholes-parts, etc.) in infrastructure registry
```

Construction IS registration — there is no separate registration phase.

## BieEnum Self-Identification

Every BieEnum class and member automatically receives a BIE identity:

- `enum_bie_identity` (class property) — BIE ID for the enum class itself, derived from its snake_case name
- `item_bie_identity` (instance property) — BIE ID for each member, computed as `order_sensitive([enum_bie_identity, item_name])`

This means every type classification in the system is itself BIE-identified and can participate in identity composition.
