---
name: bie-data-engineer
description: >
  BIE domain implementation from an approved model. Use when: implementing a
  BIE domain in Python, creating domain enums, bie_id creator functions,
  BieDomainObjects subclasses, registration helpers, domain universe setup.
  Requires an approved domain ontology model as input. General/foundation
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

   These describe *what* the domain is — not *how* to implement it. Deriving implementation artifacts (enums, calculation tables, hash modes, code) from the ontology is your responsibility.

2. **Read the Excel domain as reference** — Before writing any code, read the Excel domain implementation (see `references/code-locations.md`). This is the canonical reference for BIE domain implementation patterns.

3. **Read the code style guide** — See `references/code-style.md` for codebase conventions.

## Implementation Workflow

### Step 1: Read the Approved Domain Ontology

Parse the 4 ontology deliverables:
1. **Domain Object Types and Hierarchy** — entity types, leaf vs composite, containment
2. **Domain Relation Types** — which object types relate to which others and via what relation type
3. **Object Type Identity Dependence Relation Types** — which object types each type's identity depends on
4. **Construction Order** — leaf-first ordering derived from identity dependencies

Then derive the implementation artifacts you need:
- **Enum definitions** — map object types to enum members, determine if domain-specific relation type enums are needed
- **BIE Calculation Table** — for each entity type, determine hash mode (single/order-sensitive/order-insensitive) and specific inputs from the identity dependence relations
- **Relation registrations** — determine the bie_id_tuples to register from the relation types table

### Step 2: Read the Excel Domain Reference

Read all files listed in `references/code-locations.md` under "Excel domain reference". Understand the patterns before writing code.

### Step 3: Create Files in Order

Follow the construction order from the domain model. Create files in this sequence:

#### 3.1 Domain Types Enum

Create the domain types enum extending `BieEnums`. See `references/implementation-templates.md` for the template.

#### 3.2 Domain Relation Types Enum (if needed)

Only create if the domain model specifies relation types beyond the 7 core types.

#### 3.3 BIE ID Creator Functions

Create one creator function per entity type, following the BIE Calculation Table. Each creator is a standalone module-level function. See `references/implementation-templates.md` for templates.

#### 3.4 Domain Object Classes

Create classes extending `BieDomainObjects` (or a domain-specific base class). Each class computes its `bie_id` in `__init__` and registers during construction. See `references/implementation-templates.md` for the template.

#### 3.5 Registration Helper Functions

Create helper functions that wrap the registration pattern (register object + type-instance + relation). Follow the Excel domain's `bie_ids_registerer.py` pattern.

#### 3.6 Universe/Orchestration Integration

Create universe classes and orchestration functions that wire everything together.

### Step 4: Run Tests

After implementation, run any available tests to verify correctness.

## What NOT to Create

These already exist in the foundation layer. Do NOT recreate them:

- `BieIdCreationFacade` — Identity creation API
- `BieIdRegistries` / `BieInfrastructureRegistries` — Registration infrastructure
- `BieIdUniverses` — Universe base class
- `BieObjects` / `BieDomainObjects` — Base object classes
- `BieEnums` / `BieCoreRelationTypes` — Core enums
- `BieInfrastructureOrchestrator` — Infrastructure initialization
- `BieIds` — Identity value type
- `BSequenceNames` — Naming service

Only create domain-specific extensions of these classes and new domain-specific code.

## Verification Checklist

After implementation, verify:

- [ ] Domain enum extends `BieEnums` with a member for every object type in the ontology
- [ ] Each creator function correctly implements the identity dependence relations from the ontology
- [ ] Each object class calls `super().__init__` correctly
- [ ] Registration happens during construction (no separate phase)
- [ ] Parts are constructed before wholes (matches construction order from ontology)
- [ ] All relation types from the ontology are registered as bie_id_tuples
- [ ] Code style matches `references/code-style.md`
- [ ] All imports use full package paths
