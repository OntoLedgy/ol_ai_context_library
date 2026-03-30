# Pattern: Hierarchy Patterns

## When to Apply

Use when modelling classification structures, taxonomies, or decompositions
where you need to express how objects or classes relate structurally — whether
they are distinct, overlapping, partitioned, intersected, or fused.

## Ontological Principle

Extension-based connections operate at two levels using analogous patterns:
- **Individual level**: whole–part, distinct, overlapping (based on 4D extent)
- **Class level**: super–sub-class, distinct, overlapping (based on membership)

Any pair of objects (or classes) must fall into exactly one of three structural
patterns: **distinct**, **overlapping**, or **containment** (part-of / sub-class-of).

(Depends on: `foundations/types-tuples-powersets.md`)

## The Three Structural Patterns

**Distinct:** No shared parts (individuals) or members (classes).
My car and me are distinct — no spatio-temporal part of one is a part of the other.
Birds and bees are distinct classes — no individual is a member of both.

**Overlapping:** Some shared parts/members but neither contains the other.
The United Kingdom and the island of Ireland overlap — Northern Ireland is
a part of both. Blondes and Germans overlap — some individuals are in both classes.

**Containment:** One fully contains the other (whole–part or super–sub-class).
My hand is part of my arm. Robins are a sub-class of birds.

## Inheritance Rules

**Distinctness inherits DOWN.** If USA and France are distinct, then Texas and
Bordeaux (their parts) are also distinct. Similarly at class level: if birds and
bees are distinct, so are robins and bumble bees.

**Overlapping inherits UP.** If London and the River Thames overlap, then
South-East England and the Thames-and-tributaries also overlap. Similarly
at class level.

**Neither inherits in the opposite direction.** Two wholes can overlap even
though specific parts are distinct. Two parts can be distinct even though
their wholes overlap.

## Partition Pattern

A partition divides a whole into mutually distinct parts that together cover
the whole completely. The lepidopter's caterpillar, pupa, and butterfly states
form a complete temporal partition.

**Incomplete partition:** When only some parts are modelled, mark the
partition as incomplete/partial.

**Partition inheritance:** Partitions inherit down the hierarchy. Partitioning
the USA into North and South is inherited by sub-regions (e.g., Western USA
becomes North-Western and South-Western).

## Intersection and Fusion

**Intersection:** Where two objects overlap, their common part can be
recognised as a distinct object. Northern Ireland is the intersection of the
island of Ireland and the United Kingdom.

**Fusion:** Multiple overlapping objects can be fused into a single object
covering all their extents. The fusion is logically dependent on its constituents.

## Common Mistakes

- Assuming all hierarchies are trees — overlapping produces lattices.
- Not pushing distinct connections up and overlapping connections down the
  hierarchy for maximum inheritance and compactness.
- Confusing state–sub-state (mereological, whole–part) with state–sub-class
  (logical, super–sub-class).

## Depends On

- `foundations/types-tuples-powersets.md`
- `foundations/four-dimensionalism.md`
- `patterns/whole-part.md`
