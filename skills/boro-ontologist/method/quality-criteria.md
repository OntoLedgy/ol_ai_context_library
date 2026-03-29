# Method: Quality Criteria

## Overview

Use this checklist to validate a BORO model's ontological soundness.

## Structural Checks

- [ ] **Every sign refers to exactly one object** (strong reference principle).
      No ambiguous names. No unnamed objects that should be named.
- [ ] **Every relationship is a tuple object**, not an implicit link or FK.
- [ ] **No mutable attributes.** Every "changing property" is modelled as
      distinct temporal parts (states), not as a field that changes value.
- [ ] **Classes are extensionally defined.** Membership is determined by
      what IS in the class, not by a property description.
- [ ] **Levels are not mixed.** Individuals, classes, and powersets are at
      distinct levels. No individual is treated as a class or vice versa.

## Identity Checks

- [ ] **Every individual has a specifiable 4D extent.** If you cannot
      describe the spatio-temporal boundary of an instance, it may not be
      a legitimate individual.
- [ ] **No identity change over time.** If a concept seems to "become"
      another concept, check for the chairman pattern (distinct objects
      sharing temporal parts).
- [ ] **No duplicate objects.** If two concepts have the same 4D extent,
      they are one object — merge them.

## Pattern Checks

- [ ] **Roles are not subtypes.** Any class whose members can "leave" is
      a role or state pattern, not a genuine type hierarchy.
- [ ] **States are temporal parts.** Lifecycle stages, statuses, and
      conditions are modelled as 4D sub-extents, not attribute values.
- [ ] **Events are first-class objects.** Happenings have their own
      identity and extent, connected to participants via tuples.
- [ ] **Whole–part is spatio-temporal.** Components that change over time
      are modelled as fusions of component-states.

## Sign Checks

- [ ] **Signs and referents are separated.** Names, codes, and identifiers
      are sign objects linked to referents by denotation tuples.
- [ ] **No homonymy.** One sign does not secretly refer to two different objects.
- [ ] **No ungrounded synonymy.** If two signs refer to the same object,
      this is made explicit.

## Generalisation Checks

- [ ] **Patterns are re-usable.** Specific patterns have been generalised
      where possible (e.g., a "country name" pattern generalised to a
      "named entity" pattern).
- [ ] **No unnecessary specificity.** If two patterns share structure,
      they should be unified into one general pattern.
