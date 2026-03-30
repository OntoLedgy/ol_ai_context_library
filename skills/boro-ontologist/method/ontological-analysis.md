# Method: Ontological Analysis

## Overview

When encountering a concept in a domain model, apply these questions to
determine its ontological nature and correct BORO representation.

## The Interrogation Protocol

### Question 1: Is it an individual or a class?

- **Can you point to specific instances with 4D extent?** → Individual object
  (or class of individuals if you can point to multiple).
- **Is it a collection defined by its members?** → Class.
- **Is it a class whose members are themselves classes?** → Powerset.

### Question 2: What is its identity criterion?

- **Can you specify its spatio-temporal extent?** If yes, identity is
  extensional (4D extent). If no, further analysis needed.
- **Apply the chairman test:** If two concepts seem to be "the same thing"
  at one time and "different things" at another, they are distinct objects
  that share temporal parts.
- **Apply the car-minus test:** If removing a part seems to make two objects
  "become the same," they are distinct 4D objects that overlap after the removal.

### Question 3: Is it a type, role, or state?

- **Can an individual LEAVE this category during its lifetime?**
  - No → Genuine type (class). Model as super–sub-class.
  - Yes → Role or state. Model as temporal part (4D sub-extent).
- **Does the category exist independently of any individual holding it?**
  - Yes → Role object (like Chairman of Acme).
  - No → State (temporal part of the specific individual).

### Question 4: Is it a relationship?

- **Does it connect two or more objects?** → Tuple.
- **Is it currently modelled as an attribute?** Ask: does this attribute
  really describe the object itself, or does it describe a connection to
  another object? If the latter → reify as tuple.
- **Does the relationship hold for a limited time?** → The tuple connects
  temporal parts (states), not whole objects.

### Question 5: Is it a sign or a referent?

- **Is this a name, code, identifier, label?** → Sign object.
- **Does this concept refer to a thing in the world?** → Referent.
- **Are there multiple names for the same thing?** → Multiple sign objects
  with same referent. Make the denotation explicit.

## Thought Experiment Templates

When analysis is ambiguous, construct scenarios:

1. **The persistence test:** Imagine the object undergoes radical change.
   Is it still "the same thing"? Why? (Tests identity criteria.)
2. **The overlap test:** Imagine two concepts that seem identical now. Can
   you construct a scenario where they diverge? (Tests whether they are
   one object or two overlapping objects.)
3. **The removal test:** Imagine removing a part. Does the whole still
   exist? Does the part? (Tests whole–part relationships.)
4. **The substitution test:** Can different individuals fill this role at
   different times? (Tests type vs role distinction.)
