# Method: The Re-Engineering Process (REV-ENG)

## Overview

BORO re-engineering transforms an existing entity-based model (or raw business
vocabulary) into an ontologically grounded object model. The process is
systematic and repeatable.

## The REV-ENG Approach

### Step 1: Familiarise

Examine the existing system's entity formats — the tables, fields, codes,
and relationships. Understand what the system currently captures and how.
Do NOT assume the existing model is ontologically correct.

### Step 2: Re-engineer Entity Type Signs

For each entity type in the existing system, ask: **what object in the business
does this sign refer to?**

Apply the identity test: can you specify the spatio-temporal extent of an
instance? If yes, it is an individual object. If no, it may be a class, a
sign, or a confused conflation.

### Step 3: Re-engineer Attribute Type Signs

For each attribute, ask: **is this a genuine property of the object, or is it
really a relationship (tuple), a sign, a state, or a role?**

Common re-engineering moves:
- Foreign keys → tuple objects
- Status fields → temporal parts (states)
- Role/position attributes → separate 4D role objects
- Names/codes → sign objects with denotation tuples
- Dates → temporal boundaries of states or events

### Step 4: Build the Framework Model

Construct the re-engineered model using BORO's structural elements:
- Individual objects (4D extents)
- Classes (extensionally defined)
- Tuples (reified relationships)
- Signs (with explicit denotation)

### Step 5: Generalise and Compact

Look for re-usable patterns across the model. Generalise specific patterns
into generic ones. Compact by identifying shared structure:

- Are multiple entity types really the same class under different names?
- Do multiple relationships follow the same tuple pattern?
- Can state hierarchies be unified across different object types?

### Step 6: Validate

Apply quality criteria (see `quality-criteria.md`) to check the model is
ontologically sound. Iterate as needed.

## The Context for Re-engineering

Re-engineering occurs within a broader context:

- **The existing system** provides entity formats to analyse.
- **The business domain** provides the ground truth — the actual objects
  and patterns that exist in the world.
- **The BORO framework** provides the target ontological structure.

The re-engineer's job is to bridge from the existing system's representation
to a model that directly reflects the business reality.

## Principles

1. **Start with what exists.** Don't model from scratch — re-engineer from
   the existing system. This grounds the work in real data.
2. **Follow the strong reference principle.** Every sign must refer to exactly
   one object. This discipline exposes ambiguity and conflation.
3. **Prioritise re-usable patterns.** The goal is not just a correct model
   but a model built from general, re-usable patterns.
4. **Use thought experiments.** When unsure about identity, construct
   scenarios that test the concept's boundaries (cf. the wrecked car,
   car-minus, and chairman experiments).
