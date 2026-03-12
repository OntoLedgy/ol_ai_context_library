# BIE Component Review Checklist

Apply each check to the target component. Mark as PASS or GAP.

## Enum Checks

- [ ] Component type enum exists and extends `BieEnums`
- [ ] Each component entity type has a corresponding enum member
- [ ] BIE Domain relation type enum exists (if component needs relations beyond core)
- [ ] Enum members use `auto()` values

## Object Class Checks

- [ ] Each component object class subtypes `BieObjects` (or appropriate base like `BieDomainObjects`)
- [ ] Each implements `_create_vector()` returning a `CommonIdentityVector` subclass instance
- [ ] Identity vectors subclass `CommonIdentityVector` (not `BieIdentityVectorBase` directly)
- [ ] Identity vector `bie_domain_type` is set to the object's domain type enum member (not `None`)
- [ ] Identity vector `bie_hr_name` is set to a human-readable name for the identity
- [ ] NamedTuple places contain only the raw identity inputs (does NOT manually include `type.item_bie_identity`)
- [ ] `super().__init__(identity_vector=vector)` is called — does NOT pass `bie_id`, `base_hr_name`, `bie_type` separately
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
