# Pattern: Whole–Part

## When to Apply

Use when the domain involves composition, assembly, containment, components,
or any concept where one object is "made up of" others. Also applies to
temporal decomposition (lifecycle phases) and mixed spatio-temporal decomposition.

## Ontological Principle

A part is a sub-region of a whole's **4D spatio-temporal extent**. Because space
and time are on a par, whole–part covers spatial parts (engine in a car),
temporal parts (Tuesday-morning of a week), and spatio-temporal parts
(the engine-on-Tuesday-morning).

(Depends on: `foundations/four-dimensionalism.md`)

## The Problem

In 3D models, whole–part only covers spatial composition. Temporal
decomposition (states, phases) is handled separately by attributes or status
fields. This creates an artificial split — components that change (like
replacing a tyre) cannot be modelled consistently.

## The BORO Resolution

Whole–part is a **single unified pattern** for all spatio-temporal decomposition:

1. **Spatial part**: The engine is a spatial part of the car (shares the full
   time extent but a sub-region of space).
2. **Temporal part**: The car-last-Tuesday is a temporal part of the car
   (shares the full spatial extent but a sub-region of time). These are states.
3. **Spatio-temporal part**: The engine-last-Tuesday is a spatio-temporal part
   (sub-region in both space and time).

**Components as fusions of states:** When a car's tyre is replaced, the "tyre
component" of the car is a fusion of the old-tyre-while-fitted state and the
new-tyre-while-fitted state. This component is a single 4D object (possibly
discontinuous in material composition) that is always a part of the car.

```
  SPACE
    |   ┌──────────────────────────────────┐
    |   │          CAR (4D whole)           │
    |   │                                  │
    |   │  TYRE #21's    │  TYRE #22's     │
    |   │  component     │  component      │
    |   │  state         │  state          │
    |   │ ◄─── TYRE COMPONENT (fusion) ───►│
    |   └──────────────────────────────────┘
    └──────────────────────────────────────────► TIME
         TYRE #21 ═══════╡
                          ╞══════ TYRE #22
```

**Part identity:** A part's identity is determined by its 4D extent, not by
what it is "called" or what role it plays. Car-minus (a car without its back
seats) is a legitimate 4D object that overlaps with the car.

## Minimal Example

**Before:** `CAR has-component ENGINE, has-component WHEEL[4]`

**After:** Engine and each wheel are spatial parts (4D sub-extents) of the car.
When a wheel is replaced, the wheel-component is a fusion of the old-wheel-state
and new-wheel-state. All modelled via whole–part tuples:
`<engine, car>`, `<wheel-component, car>`

## Common Mistakes

- Treating spatial parts and temporal parts as fundamentally different things.
- Not recognising components as fusions when parts are replaced over time.
- Assuming parts must be continuous in time.
- Confusing whole–part (mereological) with super–sub-class (logical).

## Depends On

- `foundations/four-dimensionalism.md`
- `patterns/state-modelling.md`
