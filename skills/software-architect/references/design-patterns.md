# Design Patterns Reference

Recurring structural patterns used in solutions. Organised into two sections:

1. **General Design Patterns** — the canonical GoF (Gang of Four) and related patterns from [refactoring.guru/design-patterns](https://refactoring.guru/design-patterns). Apply these across any platform and domain.
2. **BORO/BIE-Specific Patterns** — patterns specific to the ontological architecture of bclearer solutions. These extend and apply the general patterns within the BORO/BIE context.

---

## Part 1 — General Design Patterns

Reference: [refactoring.guru/design-patterns](https://refactoring.guru/design-patterns)

### Creational Patterns

These patterns deal with object creation mechanisms, aiming to create objects in a manner suitable to the situation.

| Pattern | Intent | Use When |
|---------|--------|----------|
| **Abstract Factory** | Produce families of related objects without specifying their concrete classes | You need to create sets of related objects (e.g. cross-platform UI components) and want families to be interchangeable |
| **Builder** | Construct complex objects step by step, separating construction from representation | Object construction requires many steps or optional parts; you want the same process to produce different representations |
| **Factory Method** | Define an interface for creating an object, but let subclasses decide which class to instantiate | A class cannot anticipate the class of objects it needs to create; subclasses should specify |
| **Prototype** | Copy existing objects without depending on their concrete classes | Object creation is expensive; you need copies of objects that vary only in state |
| **Singleton** | Ensure a class has only one instance and provide a global access point | Exactly one object is needed to coordinate actions (registries, configuration); use sparingly — prefer dependency injection |

---

### Structural Patterns

These patterns explain how to assemble objects and classes into larger structures while keeping these structures flexible and efficient.

| Pattern | Intent | Use When |
|---------|--------|----------|
| **Adapter** | Convert the interface of a class into another interface clients expect | You want to use an existing class but its interface doesn't match what you need; wrapping I/O sources (files, DBs, APIs) |
| **Bridge** | Separate an abstraction from its implementation so the two can vary independently | You want to extend a class in several orthogonal dimensions; avoid a proliferation of subclasses |
| **Composite** | Compose objects into tree structures and let clients treat individual objects and compositions uniformly | You need to represent whole/part hierarchies; clients should treat leaves and composites the same way |
| **Decorator** | Attach additional responsibilities to an object dynamically | You want to add behaviour to individual objects at runtime without affecting others; prefer over subclassing for extensibility |
| **Facade** | Provide a simplified interface to a complex subsystem | You want to hide complexity behind a simple interface; provide an entry point to a layered architecture |
| **Flyweight** | Share common state between many fine-grained objects to save memory | You need a large number of similar objects and memory cost is prohibitive; shared state must be truly immutable |
| **Proxy** | Provide a surrogate or placeholder for another object to control access to it | Lazy initialisation, access control, logging, caching, remote access — when you need a wrapper around the real object |

---

### Behavioral Patterns

These patterns deal with communication and responsibilities between objects.

| Pattern | Intent | Use When |
|---------|--------|----------|
| **Chain of Responsibility** | Pass a request along a chain of handlers; each handler decides to process or pass on | More than one object may handle a request; you want to decouple sender from receiver |
| **Command** | Encapsulate a request as an object, allowing parameterisation, queuing, and undo | You need to parameterise operations, support undo/redo, queue or log requests |
| **Iterator** | Provide a way to sequentially access elements of a collection without exposing its representation | You need a uniform way to traverse different collection types |
| **Mediator** | Define an object that encapsulates how a set of objects interact | Many objects communicate in complex ways, creating tight coupling; centralise coordination |
| **Memento** | Capture and externalise an object's internal state so it can be restored later | You need undo/redo or snapshots of object state without violating encapsulation |
| **Observer** | Define a one-to-many dependency so that when one object changes state, its dependents are notified | A change in one object requires changing others, and you don't know how many or which objects need to change |
| **State** | Allow an object to alter its behaviour when its internal state changes | Object behaviour depends on its state, and it must change at runtime; avoids large conditionals |
| **Strategy** | Define a family of algorithms, encapsulate each one, and make them interchangeable | You need different variants of an algorithm; you want to switch algorithms at runtime |
| **Template Method** | Define the skeleton of an algorithm in a base class, deferring some steps to subclasses | Several classes share the same algorithm structure but differ in certain steps |
| **Visitor** | Represent an operation to be performed on elements of an object structure without changing the classes | You need to add operations to a stable object hierarchy without modifying it; separates algorithm from data structure |

---

## Part 2 — BORO/BIE-Specific Patterns

These patterns are the "how" that implements the BORO/BIE "what" defined in `design-philosophy.md`. They build on the general patterns above.

---

### Factory Pattern (BIE variant of Factory Method)

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

**General pattern basis:** Factory Method / Abstract Factory

---

### Registry Pattern

**Use for:** Locating objects without passing references.

All domain objects register themselves (via factory) into one or more registries keyed by their identity. Consumers look up objects by ID rather than holding direct references.

- BIE: `BieIds` → `BieIdRegistries` → `BieIdUniverses`
- BNOP: `BnopObjects.registry_keyed_on_uuid`

**Why:** Decouples producers from consumers. Enables late binding and cross-component lookup.

**General pattern basis:** Flyweight (shared object pool) + Observer (implicit notification via registry)

---

### Adapter Pattern (BIE variant)

**Use for:** All I/O boundaries (files, databases, APIs).

External data sources are wrapped in adapters that translate between the external format and internal domain representations. Domain logic never imports interop services directly — it depends on an adapter interface (port).

```
External Source → Adapter → Domain Objects → Pipeline / Service
```

**Why:** Changing the data source (e.g. CSV → Parquet) requires only changing the adapter, not the domain logic.

**General pattern basis:** Adapter (Structural)

---

### Identity-Before-Construction

**Use for:** Any entity that needs a stable, referenceable identifier.

Identity (BIE ID or BNOP UUID) is computed before the object is constructed. The object receives its identity as a constructor parameter — it does not generate its own identity.

```python
bie_base_identity = _create_entity_bie_base_identity(places)
entity = EntityObjects(
    property_a=...,
    bie_base_identity=bie_base_identity)
```

**Why:** Makes identity deterministic. Enables pre-registration and cross-component referencing before full construction.

**General pattern basis:** Builder (separates construction phases)

---

### Leaf-Before-Whole Construction Order

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

**General pattern basis:** Composite (tree structure) + Template Method (fixed construction sequence)

---

### Universe Pattern

**Use for:** Grouping all objects belonging to a single processing context.

A Universe is a container that holds all registries and objects created in one logical context (e.g. one pipeline run, one snapshot). It is created at the top of the call stack and passed down.

```python
universe = SomeDomainUniverse()
# ... populate via factories
# ... pass to consumers
```

**Why:** Avoids global mutable state. Makes the scope of a computation explicit and cleanly disposable.

**General pattern basis:** Facade (single entry point to a subsystem) + Memento (encapsulated state snapshot)

---

### Three-Tier Creator Pattern (BIE-specific)

**Use for:** BIE ID creation functions.

Every BIE entity has three creation functions:

| Tier | Function | Purpose |
|------|----------|---------|
| Public | `create_entity_bie_id(...)` | Simple entry point for external callers |
| Internal | `calculate_entity_bie_id(...)` | Constructs the identity vector and calls the facade |
| Registration | `issue_entity_bie_id(...)` | Creates an `EntityBieIdRequest` and calls `create_and_register_bie_id()` |

**Why:** Separates the concern of computing an ID from the concern of registering it. Callers that only need the ID call `create_`; callers that need the full registration lifecycle call `issue_`.

**General pattern basis:** Command (encapsulates a request) + Chain of Responsibility (tiered processing)

---

### Orchestrator Pattern

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

**General pattern basis:** Mediator (central coordinator) + Template Method (fixed sequence, swappable steps)

---

### Dependency Inversion

**Use for:** All inter-component dependencies.

High-level components (orchestrators, domain services) depend on abstractions (protocols, base classes), not on concrete implementations (specific interop adapters, specific databases).

```python
# Correct — depends on abstraction
def process(reader: DataReader, writer: DataWriter) -> None: ...

# Avoid — depends on concrete implementation
def process(excel_reader: ExcelReader, postgres_writer: PostgresWriter) -> None: ...
```

**Why:** Makes components testable in isolation. Enables swapping implementations without changing callers.

**General pattern basis:** Strategy (swappable implementations behind an interface)

---

## Pattern Selection Guide

### General patterns — when to apply

| Situation | Pattern |
|-----------|---------|
| Creating families of related objects | Abstract Factory |
| Complex multi-step object construction | Builder |
| Subclasses decide which object to create | Factory Method |
| Wrapping incompatible interfaces | Adapter |
| Adding behaviour without subclassing | Decorator |
| Simplifying access to a complex subsystem | Facade |
| Tree / whole-part hierarchy | Composite |
| One-to-many change notification | Observer |
| Interchangeable algorithms | Strategy |
| Fixed algorithm, variable steps | Template Method |
| Encapsulating a request | Command |
| Object behaviour varies by state | State |

### BORO/BIE patterns — when to apply

| Situation | Pattern |
|-----------|---------|
| Creating a domain object | Factory Pattern (BIE variant) |
| Finding an object by ID | Registry Pattern |
| Reading from a file or database | Adapter Pattern (BIE variant) |
| Assigning an identifier before construction | Identity-Before-Construction |
| Constructing a hierarchy of entities | Leaf-Before-Whole |
| Scoping a pipeline run | Universe Pattern |
| Creating BIE IDs | Three-Tier Creator |
| Sequencing pipeline steps | Orchestrator Pattern |
| Connecting to external services | Dependency Inversion |
