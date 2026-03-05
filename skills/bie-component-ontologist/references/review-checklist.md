# BIE Component Review Checklist

Apply each check to the target component. Mark as PASS or GAP.

## Enum Checks

- [ ] Component type enum exists and extends `BieEnums`
- [ ] Each component entity type has a corresponding enum member
- [ ] Domain relation type enum exists (if component needs relations beyond core)
- [ ] Enum members use `auto()` values

## Object Class Checks

- [ ] Each component object class subtypes `BieObjects` (or appropriate base like `BieDomainObjects`)
- [ ] Each computes `bie_id` in `__init__` via `BieIdCreationFacade`
- [ ] Type `item_bie_identity` is the first composition input (type-first convention)
- [ ] `super().__init__(bie_id=, base_hr_name=, bie_type=)` is called with correct arguments
- [ ] No mutable state participates in identity computation

## Registration Checks

- [ ] Level 1 registration (object + type-instance) happens during construction
- [ ] All `bie_id_tuples` are created during `__init__` (construction is registration)
- [ ] No post-construction registration phase exists
- [ ] Relations use correct `BieCoreRelationTypes` or domain relation types

## Construction Order Checks

- [ ] Parts are computed before wholes (leaf-first ordering)
- [ ] No circular dependencies in identity composition
- [ ] Creator functions are stateless (pure input -> BieIds output)

## Model Completeness Checks

- [ ] BIE Calculation Table exists or can be inferred from code
- [ ] Every entity type has a documented identity composition rule
- [ ] Every relation in the component has a corresponding bie_id_tuple registration
- [ ] Construction order is documented or inferable from the code

## Output Format

| # | Principle | Expected | Actual | Status |
|---|-----------|----------|--------|--------|
| 1 | BIE type enum | BieEnums subclass with members | ... | PASS/GAP |
| 2 | ... | ... | ... | ... |
