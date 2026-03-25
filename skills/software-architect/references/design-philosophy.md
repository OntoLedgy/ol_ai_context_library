# Design Philosophy

This document summarises the ontological foundations that underpin all architectural decisions.

---

## BORO — Basic Object Reference Ontology

BORO is a 4-dimensional upper ontology. All things that exist are **BORO individuals** that have spatial and temporal extent. The fundamental principle: an entity is identified by *what it is*, not by how or where it is stored.

### Core Distinctions

| Concept | Description |
|---------|-------------|
| **Individual** | Any distinct thing (object, event, state, boundary) |
| **Type** | A classification — not a separate entity, but a way of grouping individuals |
| **Whole/Part** | Composition — a whole is made up of parts; parts are temporal or spatial sub-extents |
| **Name** | A linguistic assignment — entities can have multiple names; names are not identity |
| **State** | A temporal segment of an individual's existence |
| **Event** | A change — a boundary between states |

The BORO upper ontology distinguishes:
- **4D individuals** — objects with temporal parts (person over time, account over time)
- **Endurants vs. perdurants** — objects that persist through time vs. processes/events that unfold over time

### Why It Matters for Architecture

Every domain entity you design should be classifiable:
- Is this a persistent individual (object) or a process/event?
- Does it have temporal extent — is it meaningful to distinguish its state at different times?
- What uniquely identifies it, independent of storage?

---

## BNOP — BORO Native Objects Python

BNOP is the Python implementation of the BORO upper ontology. It provides the computational foundation for registering and relating entities.

### Key Classes

| Class | Purpose |
|-------|---------|
| `BnopObjects` | Base class for all BORO individuals; carries UUID and registry membership |
| `BnopTypes` | Type classifications for individuals |
| `BnopTuples` | Relationship representations (n-ary, ordered) |
| `BnopNames` | Naming assignments; decoupled from identity |

### Registries

BNOP maintains global registries:
- `BnopObjects.registry_keyed_on_uuid` — all objects by UUID
- `registry_keyed_on_ckid_type` — objects by content-keyed ID and type

This registry-first design means objects are always locatable without passing references through call stacks.

### Location

```
/home/khanm/bclearer/ol_bclearer_pdk/libraries/ontology/bnop/
```

---

## BIE — BORO Identity Ecosystem

BIE sits above BNOP. It provides **deterministic, implementation-independent identity** for data objects. A BIE ID is computed from the object's intrinsic properties — the same inputs always produce the same ID, regardless of when or where the object is created.

### Four-Facet Architecture

|  | Model (Design) | Implementation (Code) |
|---|---|---|
| **Foundation** | Core object model, type system | `BieIds`, `BieEnums`, `BieIdCreationFacade` |
| **Domain** | Domain object types, relation types | Domain enums, creators, object classes |

### Identity Composition

Identity is computed in two steps:

1. **Hash raw inputs (places)** — the intrinsic properties that uniquely identify this object type are hashed via BLAKE2B (order-sensitive) or integer summation (order-insensitive)
2. **Compose with type** — the facade automatically composes the base hash with `type.item_bie_identity` when `bie_domain_type` is non-None

This two-step process means type is part of identity — two objects with the same raw properties but different types have different BIE IDs.

### Key Identity Principles

| Principle | Meaning |
|-----------|---------|
| **Deterministic** | Same inputs → same ID, always |
| **Implementation-independent** | ID is derived from properties, not storage location |
| **Decoupled construction** | Factories own identity construction; domain objects receive pre-computed identity |
| **Parts before wholes** | Leaf entities (no dependencies) are constructed first |
| **Two fundamental kinds** | BIE Objects (entities with `bie_id`) and BIE Relations (`bie_id_tuple` linking objects) |

### Ontology Layer Hierarchy

```
Upper Ontology (BORO/BNOP)
    ↑ classifies
Data Identity Ontology (BIE)
    ↑ instantiates
Domain Ontology (BIE component model — designed by bie-component-ontologist)
    ↑ populates
Domain Implementation (code — written by bie-data-engineer)
```

Note: the **domain ontology** (what types of domain objects exist and how they are related) is distinct from both the upper ontology (fundamental categories of existence) and the domain implementation (Python code). The `bie-component-ontologist` skill designs the domain ontology; this architect skill designs at the level above — choosing which components are needed and how they interconnect.

---

## Ontological Methods in Practice

When designing a solution, work through these questions in order:

1. **What exists?** — enumerate the domain entities (nouns) and events/processes (verbs)
2. **What are the types?** — group entities into classifications; identify type hierarchies
3. **What is identity?** — for each entity, what properties uniquely identify it? Are those properties intrinsic or relational?
4. **What are the relationships?** — whole/part, classification, equivalence, composition
5. **What is the construction order?** — which entities depend on others for their identity?
6. **What are the boundaries?** — where does this component end and another begin?

Only after these questions are answered should you choose technology or write code.
