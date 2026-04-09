# BIE Component Review Checklist

Apply each check to the target component. Mark as PASS or GAP.

## Enum Checks

- [ ] Component type enum exists and extends `BieEnums` or the appropriate subtype such as `BieDomainTypes`
- [ ] Each component entity type has a corresponding enum member
- [ ] BIE Domain relation type enum exists (if component needs relations beyond core)
- [ ] Enum members use `auto()` values

## Object Class Checks

- [ ] Each component object class subtypes `BieObjects` (or appropriate base like `BieDomainObjects`)
- [ ] Each receives a pre-computed `BieBaseIdentities` from a factory/helper and calls `super().__init__(bie_base_identity=...)`
- [ ] No component object computes its own identity via `_create_vector()`, direct hash calls, or registration side effects inside `__init__`
- [ ] Identity vectors subclass `CommonIdentityVector` (not `BieIdentityVectorBase` directly)
- [ ] Identity vector `bie_domain_type` is set to the object's domain type enum member (not `None`)
- [ ] Identity vector `bie_hr_name` is set to a human-readable name for the identity
- [ ] NamedTuple places contain only the raw identity inputs (does NOT manually include `type.item_bie_identity`)
- [ ] No mutable state participates in identity computation

## Registration Checks

- [ ] Registration is owned by factories/helpers, not object constructors
- [ ] "Register" means rows are written into the parallel BIE universe / infrastructure registry tables, not just local dictionaries or cached `BieIds`
- [ ] Every local object `bie_id` created by creator/factory code is materialised as an object and registered through the canonical object-registration path
- [ ] Every locally issued relation is written through the canonical relation-registration path
- [ ] Every local relation target is already registered in the object/type-instance tables
- [ ] Bare `BieIds` are used only for explicit external dependencies that are already registered elsewhere
- [ ] Every composite identity dependency from creator/factory code is mirrored by at least one registered relation unless it is explicitly external
- [ ] Relations use correct `BieCoreRelationTypes` or domain relation types
- [ ] For every registration GAP, the review traces the concrete code path with file/line evidence for the `BieId` creation site, relation-registration site, and endpoint object-registration sites
- [ ] Passing tests are treated only as supporting evidence; they do NOT replace inspection of the production registration path

## Construction Order Checks

- [ ] Parts are computed before wholes (leaf-first ordering)
- [ ] No circular dependencies in identity composition
- [ ] Creator functions are stateless (pure input -> BieIds output)

## Model Completeness Checks

- [ ] BIE Calculation Table exists or can be inferred from code
- [ ] Every entity type has a documented identity composition rule
- [ ] Every relation in the component has a corresponding bie_id_tuple registration
- [ ] Every local object type has an explicit object-registration path into the parallel BIE universe
- [ ] Construction order is documented or inferable from the code
- [ ] The review distinguishes implementation gaps from missing-test-only gaps

## Output Format

| # | Principle | Expected | Actual | Status |
|---|-----------|----------|--------|--------|
| 1 | BIE type enum | BieEnums subclass with members | ... | PASS/GAP |
| 2 | ... | ... | ... | ... |

For each GAP, add a short evidence block with:
- `Gap type`: implementation gap, testing gap, or both
- `Creator/identity site`: file and line
- `Relation site`: file and line, or `not applicable`
- `Object registration sites`: file and line for each endpoint, or `missing`
- `Why this is a gap`: one sentence tied to the checklist item
