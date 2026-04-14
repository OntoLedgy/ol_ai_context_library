# Four-Facet Architecture

## BIE is not BORO

Before anything else, keep these two ontologies distinct:

- **BORO ontology** — models real-world business objects. It is extensional, 4D,
  and lives in the **master BORO ontology object store** that the organisation
  curates as its authoritative semantic reference.
- **BIE ontology** — identifies **data-structure artefacts**: the files, rows,
  records, cells, nodes, and in-memory objects that carry information *about*
  the real world. A `bie_id` identifies the data-structure, not the real-world
  referent it describes.

The two are **correlated but not identical**. The same data structure usually
describes the same real-world thing, and BIE identity composition is
BORO-aligned (extensional, deterministic, parts-before-wholes), but a BIE
identity is not a BORO identity. The bridge between them is the pipeline's
**Assimilate** stage (`4a_assimilate`), which injects the evolved BIE fragment
into the master BORO ontology object store and reconciles any non-compliance
against the master compliance model.

Whenever this document (or any downstream skill) says "the BIE ontology",
it means the identity ecosystem for data-structure artefacts — never the
master BORO ontology.

---

## Four Facets

The BIE framework is organized along two axes, producing four facets:

|                    | Model (Design)                          | Implementation (Code)                     |
|--------------------|-----------------------------------------|-------------------------------------------|
| **Foundation**     | Core object model, type system, enums   | BieIds, BieEnums, BieIdCreationFacade     |
| **Domain**         | Domain object types, relation types     | Domain enums, creators, object classes    |

- **Foundation Model** — The abstract type system: BieTypes, BieRelationTypes, BieCoreRelationTypes, BieEnums self-identification
- **Foundation Implementation** — The code infrastructure: BieIdCreationFacade, CommonIdentityVector, BieIdRegistries, BieIdUniverses, BieObjects, hashing pipeline
- **Domain Model** — The ontology for a specific domain: object types, relation types, calculation table, construction order
- **Domain Implementation** — The Python code for a specific domain: domain enums, bie_id creators, BieDomainObjects subclasses

The ontologist skill can review or design ontologies for **either** foundation or domain components. The four-facet names above are formal architectural terms.

## Two Fundamental Kinds

A BIE ontology has two fundamental kinds:

1. **BIE Objects** — Entities within a component. Each object has a `bie_id` (BIE identifier). Stored in the objects register.
2. **BIE Relations** — Links between things. Each relation is a `bie_id_tuple` — an ordered tuple of bie_ids representing participants and relation type. Stored in the relations register.

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
2. **Two-step domain typing** — Identity composition is a two-step process:
   - Step 1: Hash the raw identity inputs (places) to produce a base bie_id
   - Step 2: Compose `order_sensitive(type.item_bie_identity, base_bie_id)` to produce the final typed identity
   - This is triggered automatically by the facade when the identity vector's `bie_domain_type` is non-None
3. **Parts before wholes** — Leaf entities must be constructed before their containing composites

## Object Construction Pattern

Each component object follows this pattern during `__init__`:

```
1. Set instance attributes needed for identity
2. Create identity vector — _create_vector() builds a CommonIdentityVector subclass instance
3. Init super — super().__init__(identity_vector=vector)
   (BieObjects extracts bie_hr_name, bie_type, and computes bie_id from the vector)
4. Register Level 1 — register object + type-instance relation in infrastructure registry
5. Create bie_id_tuples — register all relations (wholes-parts, etc.) in infrastructure registry
```

Construction IS registration — there is no separate registration phase.

## BieEnum Self-Identification

Every BieEnum class and member automatically receives a BIE identity:

- `enum_bie_identity` (class property) — BIE ID for the enum class itself, derived from its snake_case name
- `item_bie_identity` (instance property) — BIE ID for each member, computed as `order_sensitive([enum_bie_identity, item_name])`

This means every type classification in the system is itself BIE-identified and can participate in identity composition.
