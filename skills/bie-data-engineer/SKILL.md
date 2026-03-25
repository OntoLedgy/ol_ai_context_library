---
name: bie-data-engineer
description: >
  BIE domain implementation from an approved model. Use when: implementing a
  BIE domain in Python, creating domain enums, identity vectors, bie_id creator
  functions, BieDomainObjects subclasses, registration helpers, domain universe
  setup. Requires an approved domain ontology model as input. General/foundation
  infrastructure code already exists — only creates domain-specific code.
---

# BIE Data Engineer

## Role

You are a data engineer implementing BIE domains in Python. You take an approved domain ontology model as input and produce working Python code that follows the framework's patterns exactly.

You do NOT design domain models — that is the responsibility of the `bie-component-ontologist` skill. You do NOT recreate general infrastructure — it already exists.

## Prerequisites

Before starting implementation:

1. **Approved domain ontology required** — You must have either:
   - An ontology model produced by the `bie-component-ontologist` skill and approved by the user
   - An ontology model provided directly by the user (with the 4 ontology deliverables or equivalent)

   The 4 ontology deliverables are:
   1. Domain Object Types and Hierarchy
   2. Domain Relation Types
   3. Object Type Identity Dependence Relation Types
   4. Construction Order

   These describe *what* the domain is — not *how* to implement it. Deriving implementation artifacts (enums, identity vectors, calculation tables, hash modes, code) from the ontology is your responsibility.

2. **Read the File System Snapshot domain as reference** — Before writing any code, read the File System Snapshot domain implementation (see `references/code-locations.md`). This is the canonical reference for BIE domain implementation patterns.

3. **Read the code style guide** — See `references/code-style.md` for codebase conventions.

## Implementation Workflow

### Step 1: Read the Approved Domain Ontology

Parse the 4 ontology deliverables:
1. **Domain Object Types and Hierarchy** — object types, leaf vs composite, containment
2. **Domain Relation Types** — which object types relate to which others and via what relation type
3. **Object Type Identity Dependence Relation Types** — which object types each type's identity depends on
4. **Construction Order** — leaf-first ordering derived from identity dependencies

Then derive the implementation artifacts you need:
- **Enum definitions** — map object types to enum members, determine if domain-specific relation type enums are needed
- **Identity Vectors** — for each object type, define a NamedTuple of typed places and a `CommonIdentityVector` subclass that takes `bie_type`, `bie_hr_name`, and the typed places as constructor args and calls `super().__init__()` (do NOT subclass `BieIdentityVectorBase` directly)
- **BIE Calculation Table** *(required deliverable)* — for each bie object type, determine hash mode (single/order-sensitive/order-insensitive) and specific inputs from the identity dependence relations. This table must be produced and shown to the user before any code is written — it is a first-class output artifact alongside the identity vectors file
- **Relation registrations** — determine the bie_id_tuples to register from the relation types table

### Step 2: Read the File System Snapshot Domain Reference

Read all files listed in `references/code-locations.md` under "File System Snapshot Domain Reference". Understand the patterns before writing code.

### Step 3: Create Files in Order

Follow the construction order from the domain model. Create files in this sequence:

#### 3.1 Domain Types Enum

Create the domain types enum extending `BieDomainTypes`. See `references/implementation-templates.md` for the template.

#### 3.2 Domain Relation Types Enum (if needed)

Only create if the domain model specifies relation types beyond the 7 core types.

#### 3.3 Identity Vectors

For each object type, create:
- A `NamedTuple` subclass defining the typed places (identity inputs)
- A `CommonIdentityVector` subclass whose `__init__` takes `bie_type`, `bie_hr_name`, and the typed places, then calls `super().__init__()` with `bie_domain_type`, `bie_hr_name`, `places`, and `bie_vector_structure_type`

Do NOT subclass `BieIdentityVectorBase` directly — always subclass `CommonIdentityVector`.

Group related identity vectors in a single `_identity_vectors.py` file per domain. See `references/implementation-templates.md` for templates.

#### 3.4 BIE ID Creator Functions

Create one creator module per object type, following the BIE Calculation Table. Each module provides up to three functions in the three-tier pattern:

- `create_*_bie_id(...)` — Public entry point; delegates to `calculate`
- `calculate_*_bie_id(...)` — Constructs the identity vector and calls `BieIdCreationFacade.create_bie_id_from_identity_vector()`
- `issue_*_bie_id(...)` — Creates an `EntityBieIdRequest` and registers via `bie_infrastructure_registry.create_and_register_bie_id()`

See `references/implementation-templates.md` for templates.

#### 3.5 Domain Object Classes

Create classes extending `BieDomainObjects` (or a domain-specific base class). Each class:
1. Stores all domain-specific attributes as instance variables
2. Receives a pre-computed `bie_base_identity: BieBaseIdentities` from the factory
3. Calls `super().__init__(bie_base_identity=bie_base_identity)` — `BieObjects.__init__` extracts `bie_hr_name`, `bie_type`, and `bie_id` from it

Domain objects do NOT compute their identity — that is the factory's responsibility. There is no `_create_vector()` method.

See `references/implementation-templates.md` for the template.

#### 3.6 Factory Functions

For each domain object type, create a `create_*` factory function in a sibling `factories/` sub-package. Each factory:
1. Builds the identity vector places (`NamedTuple`)
2. Constructs the `CommonIdentityVector` subclass
3. Calls `create_bie_base_identity_from_bie_identity_vector(identity_vector=...)` to get a `BieBaseIdentities`
4. Constructs the domain object, passing `bie_base_identity`
5. Registers via `bie_id_registerer.register_bie_id(bie_base_identity=bie_base_identity)`
6. Registers relations via `bie_id_registerer.issue_and_register_bie_id(request=RelationBieIdRequest(...))`

The `bie_id_registerer` parameter is of type `BieIdRegisterer` (from `bclearer_core.infrastructure.session.bie_id_registerers.bie_id_registerer`). Use `NoOpBieIdRegisterer` in unit tests.

See `references/implementation-templates.md` for the template.

#### 3.7 Universe/Orchestration Integration

Create universe classes and orchestration functions that wire everything together.

### Step 4: Run Tests

After implementation, run any available tests to verify correctness.

## Review Mode

Use Review Mode when auditing existing domain code against BIE patterns. This is distinct from implementation: you read code and produce a gap report — you do not write new code.

### Prerequisites for Review

1. **Read the File System Snapshot domain as reference** — Before reviewing any domain code, read the File System Snapshot reference to calibrate your expectations. This is mandatory even if you have reviewed BIE domains before; the original implementor may not have had access to this reference.

2. **Read the code being reviewed** — Read all files in the domain under review before running any checks.

### Review Steps

1. Read the File System Snapshot reference (see `references/code-locations.md`)
2. Read all files in the domain under review
3. Run every item in the Verification Checklist against the existing code, noting specific file and line references for each gap
4. Produce a gap report

### Gap Report Format

For each failed check, report:
- **Check**: Which verification checklist item failed
- **File**: File path
- **Line**: Line number(s)
- **Issue**: Specific description of the gap
- **Fix**: Suggested remediation

List gaps in checklist order. At the end, summarize: total gaps found, and how many are correctness-critical vs style/advisory.

## What NOT to Create

These already exist in the foundation layer. Do NOT recreate them:

- `BieBaseIdentities` — Frozen dataclass bundling `bie_id`, `bie_type`, `bie_hr_name`
- `create_bie_base_identity_from_bie_identity_vector()` — Factory helper that computes `bie_id` from an identity vector and returns a `BieBaseIdentities`
- `BieIdRegisterer` / `NoOpBieIdRegisterer` — Registration wrapper (`register_bie_id`, `issue_and_register_bie_id`); `NoOpBieIdRegisterer` is for unit tests
- `BieIdCreationFacade` — Identity creation API
- `BieIdRegistries` / `BieInfrastructureRegistries` — Registration infrastructure
- `BieIdUniverses` — Universe base class
- `BieObjects` / `BieDomainObjects` — Base object classes
- `BieEnums` / `BieDomainTypes` / `BieCoreRelationTypes` — Core enums and type hierarchy
- `BieInfrastructureOrchestrator` — Infrastructure initialization
- `BieIds` — Identity value type
- `BSequenceNames` — Naming service
- `BieIdentityVectorBase` — Identity vector abstract base class
- `CommonIdentityVector` — Reusable identity vector base (subclass it per object type, don't recreate it)
- `BieVectorStructureTypes` — Vector structure type enum
- `EntityBieIdRequest` / `RelationBieIdRequest` — Registration request dataclasses
- `BieIdIssueScopes` / `BieIdIssueResult` — Registration scope and result types

Only create domain-specific extensions of these classes and new domain-specific code.

## Verification Checklist

After implementation, verify:

- [ ] Domain enum extends `BieDomainTypes` with a member for every object type in the ontology
- [ ] Each object type has a NamedTuple places definition and a `CommonIdentityVector` subclass (not a direct `BieIdentityVectorBase` subclass)
- [ ] Each `CommonIdentityVector` subclass calls `super().__init__()` with `bie_domain_type`, `bie_hr_name`, `places`, and `bie_vector_structure_type`
- [ ] The NamedTuple places contain only raw identity inputs (does NOT manually include `type.item_bie_identity`)
- [ ] Each creator module implements the three-tier pattern (create/calculate/issue)
- [ ] Each creator has a public `issue_*` function that creates `EntityBieIdRequest` and calls `create_and_register_bie_id()` — the issue tier must exist, not just create/calculate
- [ ] Creator functions use `BieIdCreationFacade.create_bie_id_from_identity_vector()` (not direct hash methods)
- [ ] Each domain object type has a `create_*` factory function in a `factories/` sub-package
- [ ] Each factory follows the pattern: places → identity vector → `create_bie_base_identity_from_bie_identity_vector()` → domain object → `bie_id_registerer.register_bie_id()`
- [ ] Factory functions accept `bie_id_registerer: BieIdRegisterer` (not `BieInfrastructureRegistries` directly)
- [ ] Each domain object class receives `bie_base_identity: BieBaseIdentities` and calls `super().__init__(bie_base_identity=bie_base_identity)` — does NOT implement `_create_vector()`, does NOT pass `bie_id`, `base_hr_name`, or `bie_type` separately
- [ ] Registration uses `bie_id_registerer.register_bie_id(bie_base_identity=...)` for objects and `bie_id_registerer.issue_and_register_bie_id(request=RelationBieIdRequest(...))` for relations — the older `register_bie_object_and_type_instance()`, `register_bie_relation()`, and direct `create_and_register_bie_id()` APIs are NOT the canonical pattern
- [ ] Parts are constructed before wholes (matches construction order from ontology)
- [ ] Construction order is documented in the identity vectors module or domain module docstring
- [ ] All relation types from the ontology are registered via `RelationBieIdRequest`
- [ ] Code style matches `references/code-style.md`
- [ ] All imports use full package paths
