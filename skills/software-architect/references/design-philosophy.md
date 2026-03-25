# Design Philosophy

This document describes the two ontological frameworks used in solution design and their relationship to the preferred architectural style.

**Important:** BORO and BIE are two distinct and independent ontologies with different scopes. They share structural similarities but are not tied together in a hierarchy — do not conflate them.

---

## BORO — Business Objects Reference Ontology

BORO is an **ontology of the world** — it describes the structure of real-world things that exist. BORO is a **4D ontology**: everything that exists is part of the 4D universe and has both spatial and temporal extent. There is no distinction between "objects" and "processes" as separate categories — this is a BFO construct that does not apply to BORO. Its upper ontology has three fundamental categories:

| Category | Description |
|----------|-------------|
| **Elements** | Spatio-temporally extended individuals — everything that exists (objects, stages, processes) is an element. All elements have both spatial and temporal extent. |
| **Types** | Sets — collections of elements grouped by classification. Types are not separate entities; they are how we group and reason about elements. |
| **Tuples** | Relations with defined places — n-ary relations where each place has a defined role. |

These three categories break down further:

| Concept | Category | Description |
|---------|----------|-------------|
| **4D individual** | Element | Everything that exists has spatial and temporal extent. A person, an organisation, a contract are all 4D individuals — they have temporal parts just as they have spatial parts. |
| **Stage** | Element (temporal part) | A bounded temporal segment of an individual — what an individual is during a particular period. Person-at-age-30 is a stage (temporal part) of the whole person. |
| **Process** | Element (stage) | A stage in which multiple individuals' stages participate. Processes are not a separate ontological category — they are stages where participation by other stages is what is significant. |
| **Event** | Element (boundary) | A temporal boundary between stages — the limit where one stage ends and another begins. |
| **Whole / Part** | Tuple | A composition relation — a whole is constituted by its spatial or temporal parts. |
| **Name** | Tuple | A linguistic assignment — names are not identity; entities can have multiple names. |
| **Type instance** | Tuple | The relation between a type (set) and its members. |

> **Note on terminology:** "Endurant" and "perdurant" are BFO (Basic Formal Ontology) terms. They do not appear in BORO. In BFO, endurants are 3D objects that persist and perdurants are processes that unfold — a distinction BORO rejects. In BORO, both are 4D individuals; what BFO calls a perdurant is simply a stage in BORO, with other individuals' stages as participants.

### Why BORO matters for architecture

BORO is the tool for **domain analysis** — understanding what real-world things exist in a domain before choosing how to represent them in code:
- Is this thing an element (does it have spatio-temporal extension) or a type (a set of elements)?
- Is this individual viewed as a whole across its lifetime, or is the significant thing one of its stages?
- If this is a process, which individuals' stages participate in it, and how?
- What is the whole/part (spatial and temporal) structure?
- What uniquely identifies it in the world, independent of any system?

BORO informs the **design phase**. It does not dictate implementation.

### BNOP — BORO Native Objects Python

BNOP is the Python implementation of BORO. It provides classes for registering and relating entities at the upper-ontology level.

| Class | Purpose |
|-------|---------|
| `BnopObjects` | Base class for all BORO individuals; carries UUID and registry membership |
| `BnopTypes` | Type classifications for individuals |
| `BnopTuples` | Relationship representations (n-ary, ordered) |
| `BnopNames` | Naming assignments; decoupled from identity |

BNOP maintains global registries:
- `BnopObjects.registry_keyed_on_uuid` — all objects by UUID
- `registry_keyed_on_ckid_type` — objects by content-keyed ID and type

**Location:** `/home/khanm/bclearer/ol_bclearer_pdk/libraries/ontology/bnop/`

---

## BIE — Data Identity Ontology

BIE is an **ontology of the data** — it describes the structure of data objects and how they are identified. BIE is independent of BORO: it does not require BORO concepts and is not a specialisation or extension of BORO.

BIE's upper ontology is intentionally simple and general:

| Category | Description |
|----------|-------------|
| **Objects** | Any data thing that can be given a stable identity. More general than BORO Elements — not required to have spatio-temporal extension. |
| **Relations** | Connections between objects. More general than BORO Tuples — no required place semantics at the upper level. |

**BIE is more formal and general than BORO in this regard.** BORO's upper categories (Elements, Types, Tuples) are richer and world-specific. BIE's upper categories (Objects, Relations) are minimal and data-specific.

### What BIE provides

BIE provides a framework for giving data objects **deterministic, implementation-independent identity**. A BIE ID is computed from the object's intrinsic data properties — the same inputs always produce the same ID, regardless of when, where, or how the object is created.

### Four-Facet Architecture

|  | Model (Design) | Implementation (Code) |
|---|---|---|
| **Foundation** | Core object model, type system | `BieIds`, `BieEnums`, `BieIdCreationFacade` |
| **Domain** | Domain object types, relation types | Domain enums, creators, object classes |

### Identity Composition

Identity is computed in two steps:

1. **Hash raw inputs (places)** — the intrinsic properties that uniquely identify this object type are hashed via BLAKE2B (order-sensitive) or integer summation (order-insensitive)
2. **Compose with type** — the facade automatically composes the base hash with `type.item_bie_identity` when `bie_domain_type` is non-None

This means type is part of identity — two objects with the same raw data but different types have different BIE IDs.

### Key Identity Principles

| Principle | Meaning |
|-----------|---------|
| **Deterministic** | Same inputs → same ID, always |
| **Implementation-independent** | ID is derived from data properties, not storage location |
| **Decoupled construction** | Factories own identity construction; domain objects receive pre-computed identity |
| **Parts before wholes** | Leaf data objects (no identity dependencies) are constructed first |
| **Two fundamental kinds** | BIE Objects (with `bie_id`) and BIE Relations (`bie_id_tuple` linking objects) |

### BIE Hierarchy (data layer only)

```
BIE Foundation (Objects + Relations — upper data ontology)
    ↑ instantiated by
BIE Domain Ontology (designed by bie-component-ontologist)
    ↑ implemented by
Domain Code (written by bie-data-engineer)
```

---

## Cross-Cutting Concern — Structural Similarity

BORO and BIE are architecturally independent, but they share structural patterns. This is not accidental — BIE's design was informed by BORO's ontological thinking. The similarities are:

| BORO concept | BIE structural parallel | Note |
|-------------|------------------------|------|
| Element (4D spatio-temporal individual) | BIE Object | Not equivalent — BIE Objects need not be spatio-temporal; they are data things, not world things |
| Stage (temporal part of an element) | BIE Object (if the stage is the unit of data) | In data systems, the stage rather than the whole individual is often what is recorded |
| Tuple (relation with defined places) | BIE Relation (`bie_id_tuple`) | BIE relations are simpler; places are not semantically typed at the BIE upper level |
| Type (set) | BIE type enum (`BieEnums`) | BIE types carry their own identity via enum self-identification |
| Whole/Part | BIE `BIE_WHOLES_PARTS` relation | Structural parallel, but BORO whole/part applies to 4D individuals including stages |

**Use BORO** when you need to analyse what things exist in a domain and how they relate in the real world — during domain analysis and design.

**Use BIE** when you need to assign stable, deterministic identities to data objects in code — during data design and implementation.

When building a system that models real-world entities, you may use BORO to understand the domain structure and then use BIE to represent data about those entities — but this is a design choice, not a requirement. BIE does not depend on BORO.

---

## Preferred Architectural Style — Clean Architecture with Ontological Grounding

The preferred style is **Clean Architecture** (also known as Hexagonal Architecture / Ports and Adapters), adapted to make both BORO domain grounding and BIE data identity explicit.

### Layers (inner → outer)

```
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                      │
│      Adapters, databases, file I/O, APIs, UI                │
├─────────────────────────────────────────────────────────────┤
│                   Application Layer                         │
│      Orchestrators, pipeline stages, use cases              │
├─────────────────────────────────────────────────────────────┤
│                   Domain Layer                              │
│      Domain objects, factories, registries, domain services │
├──────────────────────────┬──────────────────────────────────┤
│  BORO Foundation         │  BIE Foundation                  │
│  (world ontology)        │  (data identity)                 │
│  BNOP classes,           │  BieIds, BieEnums,               │
│  BORO registries         │  BieIdCreationFacade             │
└──────────────────────────┴──────────────────────────────────┘
```

The foundation layer has two independent components that both underpin the Domain layer:
- **BORO Foundation** — used when domain objects need world-ontology grounding (via BNOP)
- **BIE Foundation** — used when domain objects need deterministic data identity

Not every solution uses both. A solution may use BIE without BNOP, or BNOP without BIE.

**Dependency rule:** Source code dependencies point inward only. Nothing in an inner layer knows anything about an outer layer.

### Layer Responsibilities

| Layer | Contains | Must NOT contain |
|-------|----------|-----------------|
| **BORO Foundation** | BNOP base classes, BORO registries, universal type system | Business logic, I/O, framework code |
| **BIE Foundation** | BIE identity framework, identity vectors, BIE registries | Business logic, I/O, domain-specific knowledge |
| **Domain** | Domain objects, factories, domain services, domain enums | Direct I/O, database calls, framework dependencies |
| **Application** | Orchestrators, pipeline stages, use-case coordinators | Business rules, I/O format knowledge |
| **Infrastructure** | Interop adapters (file, DB, API), UI components, external clients | Domain logic, identity computation |

### Ports and Adapters

- **Ports** are interfaces (abstract base classes or protocols) defined in the Domain or Application layer
- **Adapters** are concrete implementations of those ports living in the Infrastructure layer
- Domain logic calls ports; adapters implement them

Swapping a data source (e.g. CSV → Parquet → database) requires only replacing the adapter — domain logic is unchanged.

### UI Components

UI elements are Infrastructure layer components. The approved UI library is:
- **Python / general:** [`ol_ui_library`](https://github.com/OntoLedgy/ol_ui_library) — note this library itself requires a clean-coding refactor; treat it as the canonical reference but expect to contribute improvements
- **Other platforms:** Platform-equivalent UI libraries are to be constructed following the same principles (see `technology-stack.md`)

---

## Ontological Methods in Practice

When designing a solution, work through these two concerns separately:

### 1. BORO domain analysis (what exists in the world?)

1. Enumerate candidate things in the domain (nouns → candidate Elements or Types; verbs → candidate stages or processes)
2. Classify each against BORO categories: Element, Type, Tuple
3. For each Element: what are its significant stages? What events (temporal boundaries) matter?
4. For each process: which individuals have stages that participate in it?
5. Map Tuple relationships: whole/part (spatial and temporal), type-instance, equivalence
6. Identify what uniquely identifies each individual in the real world

### 2. BIE data design (how will data about these things be identified?)

1. For each entity that needs a data representation, determine its intrinsic data properties
2. Decide which properties form the identity inputs (what makes this data object unique as data)
3. Determine construction order — which data objects depend on others for their identity (leaf → composite)
4. Define the BIE domain ontology (delegate to `bie-component-ontologist`)

Only after both concerns are addressed should you choose technology or write code.
