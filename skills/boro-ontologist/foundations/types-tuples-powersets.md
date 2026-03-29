# Foundation: Types, Tuples, and Powersets

## Principle

BORO has three kinds of constructed object built from individuals:
**classes** (types), **tuples** (relationships), and **powersets** (types of types).
All are extensionally defined.

## Classes (Types)

A class is a **collection of objects that share the same 4D extent membership**.
Classes are extensionally defined: two classes are identical iff they have exactly
the same members.

- **Super–sub-class**: Class A is a super-class of class B iff every member of B
  is also a member of A. Visualise with Venn diagrams (B's circle inside A's).
- **Membership is timeless**: An object either is or is not a member of a class.
  There is no "joining" or "leaving" a class over time. If a person is a member
  of the class "employees of Acme Corp" only during 2020–2023, then the member
  is a temporal part of the person (their Acme-employment state), not the
  whole person.

## Tuples

A tuple is a **constructed object that connects two or more objects in an ordered
relationship**. Tuples replace the substance paradigm's relational attributes.

- A tuple is itself an object with identity — two tuples are the same iff they
  connect the same objects in the same order.
- Tuples are the mechanism for all relationships. "John works for Acme" is
  modelled as a tuple <John-employment-state, Acme>.
- **Tuple classes** group tuples of the same kind (e.g., all employment tuples).

## Powersets (Types of Types)

A powerset is a **class whose members are themselves classes**. This gives a
clean layered hierarchy:

- Level 0: Individual objects (4D extents)
- Level 1: Classes of individuals (e.g., "Persons", "Cars")
- Level 2: Classes of classes / powersets (e.g., "Species" is a class whose
  members are classes like "Homo sapiens", "Canis lupus")

Powersets prevent type confusion — they make explicit the level at which you
are modelling.

## Key Rules for Modelling

1. **Every relationship is a tuple.** Never model relationships as attributes or
   direct links — always reify as a tuple object.
2. **Classes are extensional.** Define classes by their members, not by
   properties or intensions. Two classes with the same members are one class.
3. **Respect levels.** Do not mix individuals and classes at the same level.
   A type of type (powerset) is not the same kind of thing as a type of individual.

## Anti-Patterns

- Treating relationships as attributes on entities (the ER-model habit).
- Defining classes intensionally (by properties) rather than extensionally (by members).
- Conflating an individual with its singleton class.
- Mixing meta-levels: treating "the concept of Dog" (a class) as if it were on
  the same level as "Fido" (an individual).
