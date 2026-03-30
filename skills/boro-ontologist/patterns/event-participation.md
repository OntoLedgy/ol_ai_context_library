# Pattern: Event Participation

## When to Apply

Use when the domain involves happenings, occurrences, processes, transactions,
or any concept where multiple objects come together for a bounded period.
Examples: meetings, sales, accidents, manufacturing steps, inspections.

## Ontological Principle

Events are **individual physical objects** — 4D spatio-temporal extents, just like
physical bodies. They are not attributes, not state changes, not "things that
happen TO objects." Events are first-class objects in the ontology. Participation
in an event is modelled via temporal overlap and tuples.

(Depends on: `foundations/four-dimensionalism.md`)

## The Problem

In entity models, events are often modelled as either: (a) timestamps on entities
(`order.created_at`), (b) junction tables with no independent identity, or
(c) state transitions (`status: pending → approved`). All three fail to capture
the event as a thing in its own right with its own extent, participants, and
structure.

## The BORO Resolution

Model events as **4D objects** with their own spatio-temporal extent. Participants
are connected to events via **tuple objects** that link temporal parts of
participants to the event.

**Events vs States:**
- A **state** is a temporal part of a single physical body (one object's time-slice).
- An **event** is a 4D extent that encompasses temporal parts of MULTIPLE objects
  (the participants). Events are where participants' time-lines intersect.

**Event structure:**
- Events can have temporal parts (sub-events, phases).
- Events can be members of event classes (types of events).
- Events can participate in higher-level events.
- Events can be spatially and temporally bounded.

**Participation tuples:**
Each participant's involvement is modelled as a tuple:
`<participant-state, event, participation-role-class>`

## Minimal Example

**Before (entity model):**
```
MEETING { id, date, location }
ATTENDEE { meeting_id, person_id, role }
```

**After (BORO):**
```
Individual objects:
  Meeting-#42 (4D event extent: boardroom, 2pm-3pm Tuesday)
  Jones (4D person)
  Smith (4D person)
  Jones-at-meeting (temporal part of Jones overlapping Meeting-#42)
  Smith-at-meeting (temporal part of Smith overlapping Meeting-#42)

Tuples:
  <Jones-at-meeting, Meeting-#42>  (participation tuple)
  <Smith-at-meeting, Meeting-#42>  (participation tuple)

Classes:
  Meetings, Persons, Meeting-Participations
```

**Space-time map:**
```
  SPACE
    |   ═══════ JONES ═══════════════════════
    |              ┌──────────┐
    |              │Jones-at- │
    |              │meeting   │
    |         ┌────┼──────────┼────┐
    |         │    │MEETING #42    │
    |         │    │          │    │
    |              │Smith-at- │
    |              │meeting   │
    |              └──────────┘
    |   ═══════ SMITH ═══════════════════════
    └──────────────────────────────────────► TIME
```

## Complex Events

Events can contain sub-events (temporal parts). A "project" event may contain
"phase" sub-events. An "inspection" may contain "test" sub-events. This uses
the standard whole–part pattern applied to event objects.

Events have causal structure: Partridge distinguishes efficient cause (the
agent or trigger), material cause (what is acted upon), and formal cause
(the pattern or plan followed).

## Common Mistakes

- Modelling events as timestamps rather than 4D extents.
- Not giving events independent identity (treating them as mere links).
- Confusing events with states: a state belongs to ONE object; an event spans
  MULTIPLE objects' time-lines.
- Forgetting that participants connect to events via their temporal parts, not
  as whole objects.

## Depends On

- `foundations/four-dimensionalism.md`
- `foundations/types-tuples-powersets.md`
- `patterns/state-modelling.md`
