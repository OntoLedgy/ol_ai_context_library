# Pattern: Temporal Ordering

## When to Apply

Use when the domain involves sequences of states, lifecycle progressions,
before/after relationships, workflows, or any concept where the order of
things in time matters. Also applies to pre-conditions and post-conditions.

## Ontological Principle

Temporal ordering is modelled as **tuple objects** connecting pairs of states
(temporal parts). The ordering tuples belong to time-ordering tuple classes.
Time ordering is a relationship between objects, not a property of time itself.

(Depends on: `patterns/state-modelling.md`, `foundations/four-dimensionalism.md`)

## The Problem

In entity models, temporal ordering is typically implicit — encoded in
timestamps, sequence numbers, or workflow engine state machines. The
ordering relationships have no independent identity and cannot be queried
or reasoned about as first-class objects.

## The BORO Resolution

Model time ordering explicitly using **time-ordering tuples** that connect
successive states.

### Simple State Change

Two states connected by a time-ordering tuple indicating one follows the other:
```
  <caterpillar-state, pupa-state>  ∈ time-ordering-tuples
```

**Temporally continuous:** The second state begins exactly when the first ends
(no gap). The caterpillar-to-pupa transition is continuous.

**Temporal gap:** There is a gap between the two states. The chairman pattern
has a gap between Jones' resignation and Smith's appointment.

### Sequence of States

A chain of time-ordering tuples: state-A → state-B → state-C. The lepidopter
lifecycle is: caterpillar → pupa → butterfly. Each arrow is a distinct
time-ordering tuple object.

### Alternating States Pattern

States that repeat in a regular pattern. A machine alternates between
running-state and idle-state. Each occurrence is a distinct state object,
but they belong to alternating state classes.

### Pre-condition Patterns

A pre-condition is a stronger form of time ordering: state-B cannot exist
unless state-A has preceded it. Pre-condition tuples belong to a sub-class
of time-ordering tuples.

### Life History

The complete time-ordering pattern for an object — all its states and their
ordering — constitutes its life history. This is a constructed pattern object
combining all the individual time-ordering tuples.

## Minimal Example

**Before:** `ORDER { status: pending→approved→shipped→delivered }`

**After:**
```
States:  Order-pending, Order-approved, Order-shipped, Order-delivered
         (temporal parts of Order #42)

Time-ordering tuples:
  <Order-pending, Order-approved>     ∈ order-progression-tuples
  <Order-approved, Order-shipped>     ∈ order-progression-tuples
  <Order-shipped, Order-delivered>    ∈ order-progression-tuples

Pre-condition tuples:
  <Order-approved, Order-shipped>     ∈ shipping-pre-condition-tuples
  (shipping requires prior approval)
```

## Common Mistakes

- Encoding ordering implicitly in timestamps rather than as explicit tuples.
- Confusing temporal ordering (which state follows which) with temporal
  containment (which state is part of which).
- Assuming all state sequences are strictly linear — they can branch and merge.

## Depends On

- `patterns/state-modelling.md`
- `foundations/four-dimensionalism.md`
- `foundations/types-tuples-powersets.md`
