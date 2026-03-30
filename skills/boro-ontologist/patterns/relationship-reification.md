# Pattern: Relationship Reification

## When to Apply

Use whenever a model contains relationships between objects — associations,
links, foreign keys, "belongs-to", "works-for", "located-at." In BORO, ALL
relationships are reified as tuple objects.

## Ontological Principle

Relationships are not primitives. Every relationship is a **tuple** — a constructed
object that connects two or more objects in an ordered sequence. Tuples are
objects with their own identity: two tuples are the same iff they connect the
same objects in the same order.

(Depends on: `foundations/types-tuples-powersets.md`)

## The Problem

In entity/relational models, relationships are either: (a) foreign keys
(asymmetric, hidden in one entity), (b) association tables (no independent
semantics), or (c) attributes (`employee.department = "Sales"`). None of these
treat the relationship as a first-class object that can itself be classified,
related to other objects, or reasoned about.

## The BORO Resolution

Every relationship becomes a **tuple object**, grouped into **tuple classes**.

**Simple tuple:** `<object-A, object-B>` — an ordered pair.
**Tuple class:** The collection of all tuples of the same kind (e.g., all
employment tuples form the "employment" tuple class).

**Key rules:**
1. Tuples connect **temporal parts** (states) when the relationship is
   time-bounded. "John works for Acme 2020–2023" connects John's
   Acme-employment state to Acme, not John-as-a-whole.
2. Tuple order matters: `<John, Acme>` (person works-for company) is
   different from `<Acme, John>` (company employs person) — they are
   different tuple classes even if they pair the same objects.
3. Tuples can participate in other tuples (higher-order relationships).

**Super–sub-class tuples:** The super–sub-class relationship between two classes
is itself modelled as a tuple: `<sub-class, super-class>`.

**Whole–part tuples:** The part-of relationship is a tuple:
`<part-object, whole-object>`.

## Minimal Example

**Before (entity model):**
```
EMPLOYEE { id, name, department_id }  -- FK to DEPARTMENT
```

**After (BORO):**
```
Individual objects:
  John (4D person)
  John-sales-state (temporal part: John while in Sales)
  Sales-dept (4D department)

Tuple:
  <John-sales-state, Sales-dept>  (member of employment-tuple-class)

Classes:
  Persons, Departments, Employment-Tuples
```

## Common Mistakes

- Leaving relationships as implicit foreign keys.
- Connecting whole objects rather than their relevant temporal parts.
- Forgetting that tuple order is significant.
- Not classifying tuples into tuple classes (losing the ability to
  reason about relationship types).

## Depends On

- `foundations/types-tuples-powersets.md`
- `patterns/state-modelling.md` (for time-bounded relationships)
