# Foundation: Signs, Naming, and Reference

## Principle

Names, identifiers, labels, and codes are **themselves objects** (signs) that
**denote** other objects. The sign is not the thing it refers to. A model must
keep signs and their referents explicitly separate.

## Frege's Framework

BORO adopts Frege's analysis of meaning with three components:

- **Sign (Zeichen)**: The name, symbol, or identifier itself — a physical mark
  or sound. "Venus", "Morning Star", "Evening Star" are three different signs.
- **Sense (Sinn)**: The descriptive content or mode of presentation associated
  with a sign. "Morning Star" presents Venus as the bright object visible at
  dawn. "Evening Star" presents it as visible at dusk.
- **Reference (Bedeutung)**: The actual object in the world that the sign
  denotes. Both "Morning Star" and "Evening Star" refer to the same object: Venus.

## Key Rules

**Signs are objects in the ontology.** The string "UK" is a physical object (a
pattern of marks) that denotes the country. The model must include both the sign
object and the country object, linked by a denotation tuple.

**The strong reference principle.** Each sign refers to exactly one object; each
object is referred to by exactly one sign. When this principle is violated (one
name for two things, or two names for one thing), the model must be re-engineered
to restore it.

**Sense supports reference.** Sense helps fix which object a sign denotes, but
sense is not reference. Two signs can have different senses but the same reference
("Morning Star" ≠ "Evening Star" as signs, but both refer to Venus).

**Signs for classes.** A class sign (type name) denotes the class object, not any
individual member. "Person" denotes the class of all persons, not any particular
person.

**Signs for tuples.** Relationship names (e.g., "works-for") denote tuple classes.
Individual tuple instances typically do not have their own signs.

## Modelling Signs

In a BORO model, the sign layer is explicit:

```
SIGN OBJECT ──denotes──► REFERENT OBJECT
"UK"         ──denotes──► United Kingdom (4D country object)
"ISO 3166 GB" ──denotes──► United Kingdom (same referent, different sign)
```

When two signs denote the same object, this must be made explicit as a
same-reference relationship, not left implicit.

## Anti-Patterns

- Treating the name as the object (confusing the sign with its referent).
- Assuming two different names must refer to two different objects.
- Leaving denotation relationships implicit in the model.
- Modelling identifiers (codes, keys) without treating them as sign objects
  with explicit denotation tuples.
