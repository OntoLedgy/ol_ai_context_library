# Pattern: Stuff Objects

## When to Apply

Use when the domain involves materials, substances, amounts, mixtures, or
continuous matter — oil, water, gold, crude, chemicals, fuel. Any concept
that refers to "stuff" rather than discrete countable things.

## Ontological Principle

Stuffs are **physical bodies** — 4D spatio-temporal extents, just like any
other individual object. "Gold" is not an abstract substance; every portion of
gold is a 4D object. The class "gold" collects all gold objects (every piece,
nugget, bar, and atom of gold that has ever existed or will exist).

(Depends on: `foundations/four-dimensionalism.md`)

## The Problem

Naive models treat stuff as either: (a) an uncountable abstract concept,
(b) a measured quantity (`amount: 500 barrels`), or (c) a type without
individuals. None properly capture the fact that a specific batch of crude
oil is a real physical object with identity, location, and history.

## The BORO Resolution

Model each portion of stuff as a **4D individual object**. Classify stuff
objects into classes (gold objects, crude oil objects). Use whole–part patterns
for mixing and splitting.

**Key points:**
- A specific 500-barrel batch of crude is a 4D object.
- When two batches are mixed, the result is a new 4D object whose temporal
  parts include the mixing event and whose spatial parts overlap with the
  contributing batches.
- Measurements (mass, volume) are signs/descriptions of the object, not the
  object itself.

## Minimal Example

**Before:** `MATERIAL { type: "crude_oil", volume: 500, unit: "bbl" }`

**After:**
```
Individual:  Batch-#42 (4D crude oil object, specific spatio-temporal extent)
Classes:     Crude-Oil-Objects (all crude oil), Batch-#42's class membership
Tuples:      <Batch-#42, Tank-7> (location whole-part tuple)
Signs:       "500 bbl" is a sign denoting the volume of Batch-#42's extent
```

## Common Mistakes

- Treating stuff as only a class with no individuals.
- Confusing the measurement of stuff with the stuff itself.
- Not modelling mixing/splitting as whole–part patterns on 4D extents.

## Depends On

- `foundations/four-dimensionalism.md`
- `patterns/whole-part.md`
