# Pattern: Role vs Type

## When to Apply

Use when the domain has positions, roles, functions, or capacities that different
individuals can hold at different times — chairman, CEO, project lead, account
manager, vehicle driver, team captain. Any time a concept's reference seems to
"change identity" over time.

## Ontological Principle

A role is **not a type** (class) that an individual "joins" and "leaves." A role is a
**4D object in its own right**, composed of temporal parts of the individuals who
hold it. The role and the role-holder are distinct objects that share temporal parts.

(Depends on: `foundations/four-dimensionalism.md`)

## The Problem

In naive models, "Chairman" is treated as either an attribute of a person
(`person.role = "chairman"`) or a subtype (`Chairman IS-A Person`). Both
approaches break when the chairman changes:

- As attribute: the reference of "Chairman of Acme" flips from Jones to Smith,
  violating the strong reference principle.
- As subtype: Jones was a Chairman, now he is not — does he leave the class?
  Then class membership changes over time, violating timelessness.

## The BORO Resolution

Model the role as a **separate 4D object** whose extent is the fusion of all the
temporal parts during which individuals hold that role.

```
  SPACE
    |   ┌──────────────────────────────────────────┐
    |   │              MR JONES (4D)                │
    |   └──────────────────────────────────────────┘
    |         ┌──────┐                    ┌──────┐
    |         │Jones'│                    │Smith'│
    |         │chair │                    │chair │
    |   ┌─────┤man-  ├──── gap ──────────┤man-  ├─────┐
    |   │     │ship  │                    │ship  │     │
    |   │     └──────┘  CHAIRMAN OF ACME  └──────┘     │
    |   └──────────────────────────────────────────────┘
    |                 ┌───────────────────────────────────┐
    |                 │          MR SMITH (4D)             │
    |                 └───────────────────────────────────┘
    └──────────────────────────────────────────────────────► TIME
```

**Objects:**
- Mr Jones (4D person)
- Mr Smith (4D person)
- Chairman of Acme (4D role object — fusion of chairmanship temporal parts)
- Jones' chairmanship (temporal part shared by Jones AND Chairman of Acme)
- Smith' chairmanship (temporal part shared by Smith AND Chairman of Acme)

**Key insight:** The Chairman of Acme is NEVER the same object as Mr Jones or
Mr Smith. They merely share temporal parts (overlap). The role object can even
have temporal gaps (between Jones' resignation and Smith's appointment).

## Minimal Example

**Before (entity model):**
```
PERSON { id, name, role: "chairman"|null }
```

**After (BORO):**
```
Individual objects: Jones, Smith, Chairman-of-Acme
Temporal parts:    Jones-chairmanship (part of Jones AND Chairman-of-Acme)
                   Smith-chairmanship (part of Smith AND Chairman-of-Acme)
Classes:           Persons, Chairmanships, Roles
Tuples:            <Jones-chairmanship, Chairman-of-Acme> (role-holding)
```

## Common Mistakes

- Treating the role as a subtype of person (Chairman IS-A Person).
- Treating the role as an attribute that changes value.
- Assuming the role-holder and the role are the same object during the
  holding period — they are not; they merely overlap.
- Expecting role objects to be temporally continuous — gaps are permitted.
- Applying this pattern where a genuine type distinction exists (dog vs cat
  IS a type distinction, not a role).

## Depends On

- `foundations/four-dimensionalism.md`
- `foundations/identity-and-individuation.md`
