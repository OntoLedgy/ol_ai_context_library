# Pattern: Cardinality Patterns

## When to Apply

Use when defining multiplicity constraints on relationships — how many times
objects of a class can participate in a tuple class. The BORO equivalent of
traditional cardinality notation (1:1, 1:N, M:N).

## Ontological Principle

Cardinality is a pattern on **occupied class places** within a tuple class.
It specifies how many times members of a given class can appear in a
particular position of tuples belonging to that tuple class. Both an upper
and a lower bound are specified.

(Depends on: `foundations/types-tuples-powersets.md`)

## The Problem

In ER models, cardinality is an implicit annotation on relationship lines.
It has no independent identity and is not itself an object. The relationship
and its constraints are tangled together.

## The BORO Resolution

Cardinality applies to each **occupied class place** independently. Each
class place in a tuple class gets its own upper and lower bound.

### The Four Cardinality Patterns

**Lower bounds:** Optional (0) or Mandatory (1)
**Upper bounds:** One (1) or Multiple (*)

| Pattern | Lower | Upper | Meaning |
|---|---|---|---|
| Optional-to-one | 0 | 1 | Member may appear 0 or 1 times |
| One-to-one | 1 | 1 | Member must appear exactly once |
| Optional-to-multiple | 0 | * | Member may appear 0 or more times |
| One-to-multiple | 1 | * | Member must appear 1 or more times |

### Verification Process

Always confirm cardinality with **specific instances**:

1. Find a member of the class that does NOT participate → lower bound is 0.
2. Find a member that DOES participate → participation is possible.
3. Find a member that participates MORE than once → upper bound is *.
4. If no member can participate more than once → upper bound is 1.

### Example

Person-born-in-Britain tuple class with two class places:
- **Persons place**: Prince Philip (not born in Britain) → optional.
  Queen Elizabeth (born in Britain, once) → upper bound 1.
  Result: optional-to-one (0..1).
- **Britain place**: Britain appears in every tuple → mandatory.
  Britain appears in multiple tuples → upper bound *.
  Result: one-to-multiple (1..*).

## Common Mistakes

- Applying cardinality to the relationship as a whole rather than to each
  occupied class place independently.
- Not verifying bounds with concrete instances — relying on intuition alone.
- Forgetting that cardinality constrains class places in tuples, not direct
  links between entities.

## Depends On

- `foundations/types-tuples-powersets.md`
- `patterns/relationship-reification.md`
