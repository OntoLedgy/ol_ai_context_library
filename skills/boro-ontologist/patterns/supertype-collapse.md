# Pattern: Supertype Collapse

## When to Apply

Use when a model has a taxonomy (IS-A hierarchy) that conflates different
ontological distinctions — mixing roles with types, states with classes, or
creating subtypes based on mutable properties. Symptom: "subtype explosion"
where every combination of attributes spawns a new subtype.

## Ontological Principle

In BORO, a class is defined **extensionally** by its members. Super–sub-class
is strict set containment: every member of the sub-class is also a member of
the super-class. Classification must respect the distinction between types
(permanent membership) and states/roles (temporal membership).

(Depends on: `foundations/types-tuples-powersets.md`)

## The Problem

Entity models often build deep IS-A hierarchies that conflate:
- **Type distinctions** (Dog vs Cat — permanent, based on essential identity)
- **Role distinctions** (Employee vs Customer — temporal, based on function)
- **State distinctions** (Active vs Retired — temporal, based on lifecycle)
- **Classification dimensions** (Red vs Large — overlapping, not exclusive)

This produces tangled hierarchies where instances awkwardly migrate between
subtypes, or where multi-dimensional classification creates combinatorial
subtype explosion.

## The BORO Resolution

**Flatten the false hierarchy** by separating genuine type distinctions from
roles and states:

1. **Genuine types**: Permanent membership. An individual is a member for
   its entire existence. Model as super–sub-class. Dog IS-A Animal.
2. **Roles**: Temporal parts of individuals. Model as separate 4D objects
   using the role-vs-type pattern. Do NOT model as subtypes.
3. **States**: Temporal parts along a lifecycle. Model using state-modelling
   pattern. Do NOT model as subtypes.
4. **Classification dimensions**: Independent, potentially overlapping
   classifications. Model as separate class hierarchies, not a single tree.

**Test each subtype:**
- Can an individual LEAVE this subtype during its lifetime? → It is a state
  or role, not a genuine subtype. Re-engineer as temporal part.
- Can an individual be in MULTIPLE subtypes simultaneously? → These are
  overlapping classifications, not exclusive subtypes. Re-engineer as
  independent class hierarchies.

## Minimal Example

**Before (false hierarchy):**
```
PERSON
  ├── EMPLOYEE
  │     ├── ACTIVE_EMPLOYEE
  │     └── RETIRED_EMPLOYEE
  ├── CUSTOMER
  └── CONTRACTOR
```

**After (BORO):**
```
Classes:         Persons (genuine type)
Roles (4D objs): Employee-of-X, Customer-of-X, Contractor-of-X
States:          Active-employment-state, Retired-state
                 (temporal parts of employment role objects)
```

## Common Mistakes

- Keeping role-based subtypes because "the database needs them."
- Treating every adjective as a sub-class (not every property warrants a type).
- Building single-inheritance trees when the domain is multi-dimensional.
- Not applying the "can it leave?" test to proposed subtypes.

## Depends On

- `foundations/types-tuples-powersets.md`
- `patterns/role-vs-type.md`
- `patterns/state-modelling.md`
