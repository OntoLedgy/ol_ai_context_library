# Pattern: State Modelling

## When to Apply

Use when the domain involves things that "change" attributes over time — lifecycle
stages, statuses, conditions, modes, phases. Any time a naive model uses a mutable
attribute (e.g., `status: active/inactive`), this pattern applies.

## Ontological Principle

States are **temporal parts** of a physical body. They are themselves physical
bodies — 4D extents that are time-slices of the whole object. A state is not a
property or attribute that an object "has"; it is a part of what the object IS.

(Depends on: `foundations/four-dimensionalism.md`)

## The Problem

In entity/relational models, change is captured by mutating attributes:
`employee.status = "active"` becomes `employee.status = "retired"`. This treats
objects as 3D things that change properties, which creates identity confusion:
the "active employee" and the "retired employee" appear to be the same thing
with different properties, but they occupy different spatio-temporal extents.

## The BORO Resolution

Model each state as a **distinct temporal part** (a 4D sub-extent) of the whole
object. The whole object is the fusion of all its states.

**Rules:**
1. A state must span the FULL spatial extent of the object for a period of time
   (otherwise it is a spatial part, not a state).
2. States have their own identity — two states are distinct if they occupy
   different extents.
3. States can belong to classes: the "caterpillar state" of lepidopter #1 is a
   member of the class "caterpillar states."
4. States form hierarchies: states can have sub-states (temporal subdivision)
   and sub-classes (classification of states).

## Minimal Example

**Before (entity model):**
```
EMPLOYEE { id, name, status: "active"|"retired", start_date, end_date }
```

**After (BORO):**
```
  SPACE
    |   ┌─────────────────────────────┐
    |   │     EMPLOYEE #1 (4D)        │
    |   │                             │
    |   │  ACTIVE STATE  │ RETIRED STATE │
    |   │  (temporal pt) │ (temporal pt) │
    |   └─────────────────────────────┘
    └─────────────────────────────────────► TIME

  Objects:  Employee #1 (whole 4D extent)
            Active-state-of-#1 (temporal part, member of class Active-States)
            Retired-state-of-#1 (temporal part, member of class Retired-States)
  Classes:  Employees, Active-States, Retired-States
```

## State Hierarchy Patterns

**State–sub-state (mereological):** A state can be subdivided into finer temporal
parts. Early-caterpillar and late-caterpillar are sub-states of the caterpillar
state. Based on whole–part pattern. Forms tree or lattice hierarchies.

**State–sub-class (logical):** States can be classified. Red-caterpillars and
green-caterpillars are sub-classes of the caterpillar class. Based on super–sub-class
pattern. Individual state identity is unchanged; classification is at type level.

**Overlapping states:** States from different classification dimensions can overlap.
A lepidopter can be simultaneously in an "infected state" and a "caterpillar state,"
producing an "infected caterpillar sub-state" at their intersection. Overlapping
sub-states form lattice (not tree) hierarchies.

## Common Mistakes

- Modelling state as a mutable attribute rather than a temporal part.
- Forgetting that states ARE physical bodies — they have full 4D extent.
- Confusing state–sub-state (mereological, whole–part) with state–sub-class
  (logical, super–sub-class). They look similar but are different patterns.
- Not recognising that an object can be a state of itself (if its state never
  changes, the whole object IS its own state — same 4D extent).

## Depends On

- `foundations/four-dimensionalism.md`
- `foundations/types-tuples-powersets.md` (for state classes)
