# Design Patterns Reference

Recurring structural patterns used in bclearer solutions. These are the "how" that implements the "what" defined in `design-philosophy.md`.

---

## Factory Pattern

**Use for:** All domain object construction.

Objects are never constructed directly at call sites. A factory function owns:
1. Assembling the identity inputs (places)
2. Computing the identity (vector → BIE ID or BNOP ID)
3. Constructing the object (passing pre-computed identity)
4. Registering the object and its relations

```
places → identity vector → bie_base_identity → domain object → register
```

**Why:** Keeps domain objects passive (no identity logic inside them). Makes construction testable and composable.

---

## Registry Pattern

**Use for:** Locating objects without passing references.

All domain objects register themselves (via factory) into one or more registries keyed by their identity. Consumers look up objects by ID rather than holding direct references.

- BIE: `BieIds` → `BieIdRegistries` → `BieIdUniverses`
- BNOP: `BnopObjects.registry_keyed_on_uuid`

**Why:** Decouples producers from consumers. Enables late binding and cross-component lookup.

---

## Adapter Pattern

**Use for:** All I/O boundaries (files, databases, APIs).

External data sources are wrapped in adapters that translate between the external format and internal domain representations. Domain logic never imports interop services directly — it depends on an adapter interface.

```
External Source → Adapter → Domain Objects → Pipeline / Service
```

**Why:** Changing the data source (e.g. CSV → Parquet) requires only changing the adapter, not the domain logic.

---

## Identity-Before-Construction

**Use for:** Any entity that needs a stable, referenceable identifier.

Identity (BIE ID or BNOP UUID) is computed before the object is constructed. The object receives its identity as a constructor parameter — it does not generate its own identity.

```python
bie_base_identity = _create_entity_bie_base_identity(places)
entity = EntityObjects(
    property_a=...,
    bie_base_identity=bie_base_identity)
```

**Why:** Makes identity deterministic. Enables pre-registration and cross-component referencing before full construction.

---

## Leaf-Before-Whole Construction Order

**Use for:** Any domain with hierarchical or compositionally-dependent entities.

Entities whose identity depends on other entities must be constructed after those dependencies. The construction order is derived from the identity dependence graph (designed by `bie-component-ontologist`).

```
Leaf entities (no identity dependencies)
    ↓
Intermediate composites (depend on leaf BIE IDs)
    ↓
Top-level composites (depend on intermediate BIE IDs)
```

**Why:** Prevents null-reference errors and circular dependencies. Makes construction order explicit and reviewable.

---

## Universe Pattern

**Use for:** Grouping all objects belonging to a single processing context.

A Universe is a container that holds all registries and objects created in one logical context (e.g. one pipeline run, one snapshot). It is created at the top of the call stack and passed down.

```python
universe = SomeDomainUniverse()
# ... populate via factories
# ... pass to consumers
```

**Why:** Avoids global mutable state. Makes the scope of a computation explicit and cleanly disposable.

---

## Three-Tier Creator Pattern (BIE-specific)

**Use for:** BIE ID creation functions.

Every BIE entity has three creation functions:

| Tier | Function | Purpose |
|------|----------|---------|
| Public | `create_entity_bie_id(...)` | Simple entry point for external callers |
| Internal | `calculate_entity_bie_id(...)` | Constructs the identity vector and calls the facade |
| Registration | `issue_entity_bie_id(...)` | Creates an `EntityBieIdRequest` and calls `create_and_register_bie_id()` |

**Why:** Separates the concern of computing an ID from the concern of registering it. Callers that only need the ID call `create_`; callers that need the full registration lifecycle call `issue_`.

---

## Orchestrator Pattern

**Use for:** Multi-step pipeline stages.

An orchestrator is a component whose sole responsibility is to sequence calls to services and adapters. It holds no business logic — it only coordinates.

```
Orchestrator
├── calls Adapter A (reads input)
├── calls Service B (transforms)
├── calls Factory C (constructs domain objects)
└── calls Adapter D (writes output)
```

**Why:** Keeps individual services focused. Makes the pipeline sequence readable as a single high-level narrative.

---

## Dependency Inversion

**Use for:** All inter-component dependencies.

High-level components (orchestrators, domain services) depend on abstractions (protocols, base classes), not on concrete implementations (specific interop adapters, specific databases).

```python
# Correct — depends on abstraction
def process(reader: DataReader, writer: DataWriter) -> None: ...

# Avoid — depends on concrete implementation
def process(excel_reader: ExcelReader, postgres_writer: PostgresWriter) -> None: ...
```

**Why:** Makes components testable in isolation. Enables swapping implementations without changing callers.

---

## Pattern Selection Guide

| Situation | Pattern |
|-----------|---------|
| Creating a domain object | Factory Pattern |
| Finding an object by ID | Registry Pattern |
| Reading from a file or database | Adapter Pattern |
| Assigning an identifier before construction | Identity-Before-Construction |
| Constructing a hierarchy of entities | Leaf-Before-Whole |
| Scoping a pipeline run | Universe Pattern |
| Creating BIE IDs | Three-Tier Creator |
| Sequencing pipeline steps | Orchestrator Pattern |
| Connecting to external services | Dependency Inversion |
