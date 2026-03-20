# Implementation Templates

All templates are derived from the File System Snapshot domain implementation. Follow these patterns exactly.

## Domain Types Enum

```python
from enum import auto
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_domain_types import \
    BieDomainTypes


class BieDomainNameTypes(
        BieDomainTypes):
    NOT_SET = \
        auto()

    BIE_OBJECT_TYPE_A = \
        auto()

    BIE_OBJECT_TYPE_B = \
        auto()
```

Notes:
- Extends `BieDomainTypes` (not `BieEnums` directly)
- Class inheritance on separate indented line
- Each member on its own line with `= \` continuation and `auto()` indented below
- Always include `NOT_SET` as first member
- Member names: `BIE_` prefix + descriptive name (e.g., `BIE_WORKBOOKS`, `BIE_RELATIVE_PATHS`)

## Identity Vector

For each object type, define a NamedTuple of typed places and a `CommonIdentityVector` subclass. Group related identity vectors in a single `_identity_vectors.py` file per domain.

There are two styles depending on whether the vector class serves one object type or multiple:

### Style A: Type-hardcoded (one vector class, one object type)

Use when the identity vector class is specific to exactly one object type. Hardcode `bie_domain_type` inside `__init__`.

```python
from typing import NamedTuple

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.common_knowledge.types.bie_vector_structure_types import \
    BieVectorStructureTypes
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.identity_vectors.common_identity_vector import \
    CommonIdentityVector
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import \
    BieIds
from your_domain.common_knowledge.your_domain_types import BieDomainNameTypes


class ObjectTypeAIdentityVectorPlaces(
        NamedTuple):
    object_a_name: str


class ObjectTypeAIdentityVector(
        CommonIdentityVector):
    def __init__(
            self,
            *,
            bie_hr_name: str,
            places: ObjectTypeAIdentityVectorPlaces) \
            -> None:
        super().__init__(
            bie_domain_type=BieDomainNameTypes.BIE_OBJECT_TYPE_A,
            bie_hr_name=bie_hr_name,
            places=places,
            bie_vector_structure_type=BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_SENSITIVE)


class ObjectTypeBIdentityVectorPlaces(
        NamedTuple):
    object_a_bie_id: BieIds
    object_b_value: str


class ObjectTypeBIdentityVector(
        CommonIdentityVector):
    def __init__(
            self,
            *,
            bie_hr_name: str,
            places: ObjectTypeBIdentityVectorPlaces) \
            -> None:
        super().__init__(
            bie_domain_type=BieDomainNameTypes.BIE_OBJECT_TYPE_B,
            bie_hr_name=bie_hr_name,
            places=places,
            bie_vector_structure_type=BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_SENSITIVE)
```

### Style B: Type-parameterized (one vector class, multiple object types)

Use when the same vector structure is shared by multiple object types (e.g., file snapshots vs folder snapshots). The `bie_type` is passed in from the factory.

```python
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_types import \
    BieTypes


class ObjectTypeSharedIdentityVector(
        CommonIdentityVector):
    def __init__(
            self,
            *,
            bie_type: BieTypes,
            bie_hr_name: str,
            places: ObjectTypeSharedIdentityVectorPlaces) \
            -> None:
        super().__init__(
            bie_domain_type=bie_type,
            bie_hr_name=bie_hr_name,
            places=places,
            bie_vector_structure_type=BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_SENSITIVE)
```

Notes:
- Identity vector classes subclass `CommonIdentityVector` — do NOT subclass `BieIdentityVectorBase` directly
- Constructor uses keyword-only args (`*`)
- `bie_hr_name` — a human-readable name for the identity; typically the primary descriptive attribute of the object
- `places` — a NamedTuple instance containing the raw identity inputs; `CommonIdentityVector` validates that places is a NamedTuple with no None values
- `bie_vector_structure_type` — determines the hashing strategy (single, order-sensitive, order-insensitive)
- The NamedTuple places contain ONLY the raw identity inputs — do NOT manually include `type.item_bie_identity`
- The facade's two-step process: (1) hash input_objects (from places) to get base bie_id, (2) `order_sensitive(bie_domain_type.item_bie_identity, base_bie_id)`
- No custom `_validate_places()` function is needed — `CommonIdentityVector` validates internally

## BIE ID Creator Function (Three-Tier Pattern)

Each creator module provides three functions: `create`, `calculate`, and `issue`.

```python
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import \
    BieIdCreationFacade
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import \
    BieIds
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.registerers.bie_id_issue_requests import \
    BieIdIssueScopes, EntityBieIdRequest
from bclearer_orchestration_services.identification_services.naming_service.b_sequence_names import \
    BSequenceNames
from your_domain.common_knowledge.your_domain_types import BieDomainNameTypes
from your_domain.bie.bie_id_creators.your_domain_identity_vectors import \
    ObjectTypeBIdentityVector, ObjectTypeBIdentityVectorPlaces


def create_object_type_b_bie_id(
        object_a_bie_id: BieIds,
        object_b_value: str) \
        -> BieIds:
    return \
        calculate_object_type_b_bie_id(
            object_a_bie_id=object_a_bie_id,
            object_b_value=object_b_value)


def calculate_object_type_b_bie_id(
        object_a_bie_id: BieIds,
        object_b_value: str) \
        -> BieIds:
    identity_vector = \
        __get_identity_vector(
            object_a_bie_id=object_a_bie_id,
            object_b_value=object_b_value)

    return \
        BieIdCreationFacade.create_bie_id_from_identity_vector(
            vector=identity_vector)


def issue_object_type_b_bie_id(
        object_a_bie_id: BieIds,
        object_b_value: str,
        bie_infrastructure_registry,
        bie_id_type_id: BieIds = None,
        b_sequence_name: BSequenceNames = None) \
        -> BieIds:
    input_objects = \
        __get_input_objects(
            object_a_bie_id=object_a_bie_id,
            object_b_value=object_b_value)

    if bie_id_type_id is None:
        bie_id_type_id = \
            BieDomainNameTypes.BIE_OBJECT_TYPE_B.item_bie_identity

    if b_sequence_name is None:
        b_sequence_name = \
            BSequenceNames(
                initial_b_sequence_name_list=['object_type_b_bie_id'])

    issue_request = \
        EntityBieIdRequest(
            input_objects=tuple(input_objects),
            bie_id_type_id=bie_id_type_id,
            b_sequence_name=b_sequence_name,
            issue_scope=BieIdIssueScopes.INFRASTRUCTURE)

    issue_result = \
        bie_infrastructure_registry.create_and_register_bie_id(
            request=issue_request)

    return \
        issue_result.bie_id


def __get_input_objects(
        object_a_bie_id: BieIds,
        object_b_value: str) \
        -> list:
    identity_vector = \
        __get_identity_vector(
            object_a_bie_id=object_a_bie_id,
            object_b_value=object_b_value)

    return \
        identity_vector.input_objects()


def __get_identity_vector(
        object_a_bie_id: BieIds,
        object_b_value: str) \
        -> ObjectTypeBIdentityVector:
    return \
        ObjectTypeBIdentityVector(
            bie_type=BieDomainNameTypes.BIE_OBJECT_TYPE_B,
            bie_hr_name=object_b_value,
            places=ObjectTypeBIdentityVectorPlaces(
                object_a_bie_id=object_a_bie_id,
                object_b_value=object_b_value))
```

Notes:
- `create` — pure computation, no side effects; delegates to `calculate`
- `calculate` — constructs identity vector and calls `BieIdCreationFacade.create_bie_id_from_identity_vector()`
- `issue` — creates `EntityBieIdRequest` and registers via `create_and_register_bie_id()`; defaults type and name if not provided
- Private `__get_identity_vector` creates a `CommonIdentityVector` subclass instance with the domain type, human-readable name, and typed places
- `__get_input_objects` delegates to the identity vector's `input_objects()` method

## Domain Object Class

Domain objects are passive data holders. They receive a pre-computed `BieBaseIdentities` from the factory and pass it to `super().__init__`. There is no `_create_vector()` method.

```python
from bclearer_core.bie.domain.bie_domain_objects import \
    BieDomainObjects
from bclearer_core.bie.top.bie_base_identities import \
    BieBaseIdentities
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import \
    BieIds


class ObjectTypeBObjects(
        BieDomainObjects):
    def __init__(
            self,
            object_a_bie_id: BieIds,
            object_b_value: str,
            bie_base_identity: BieBaseIdentities) \
            -> None:
        self.object_a_bie_id = \
            object_a_bie_id

        self.object_b_value = \
            object_b_value

        super().__init__(
            bie_base_identity=bie_base_identity)
```

Notes:
- Instance attributes are set BEFORE calling `super().__init__`
- `bie_base_identity` is received from the factory — the object does NOT compute it
- `super().__init__(bie_base_identity=bie_base_identity)` — `BieObjects` extracts `bie_hr_name`, `bie_type`, and `bie_id` from it
- Do NOT pass `bie_id`, `base_hr_name`, or `bie_domain_type` separately
- Do NOT implement `_create_vector()` — that method no longer exists in `BieObjects`

## Factory Function

For each domain object type, create a `create_*` factory function in a `factories/` sub-package. The factory owns all identity construction and registration logic. Pattern: places → vector → BieBaseIdentities → object → register.

```python
from bclearer_core.bie.top.bie_base_identities import \
    BieBaseIdentities, create_bie_base_identity_from_bie_identity_vector
from bclearer_core.infrastructure.session.bie_id_registerers.bie_id_registerer import \
    BieIdRegisterer
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_core_relation_types import \
    BieCoreRelationTypes
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import \
    BieIds
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.registerers.bie_id_issue_requests import \
    RelationBieIdRequest
from bclearer_orchestration_services.identification_services.naming_service.b_sequence_names import \
    BSequenceNames
from your_domain.common_knowledge.your_domain_types import BieDomainNameTypes
from your_domain.bie.bie_id_creators.your_domain_identity_vectors import \
    ObjectTypeBIdentityVector, ObjectTypeBIdentityVectorPlaces
from your_domain.objects.object_type_b_objects import ObjectTypeBObjects


def create_object_type_b_objects(
        *,
        object_a_bie_id: BieIds,
        object_b_value: str,
        bie_id_registerer: BieIdRegisterer) \
        -> ObjectTypeBObjects:
    bie_base_identity = \
        _create_object_type_b_bie_base_identity(
            object_a_bie_id=object_a_bie_id,
            object_b_value=object_b_value)

    object_type_b = \
        ObjectTypeBObjects(
            object_a_bie_id=object_a_bie_id,
            object_b_value=object_b_value,
            bie_base_identity=bie_base_identity)

    bie_id_registerer.register_bie_id(
        bie_base_identity=bie_base_identity)

    bie_id_registerer.issue_and_register_bie_id(
        request=RelationBieIdRequest(
            bie_place_1_id=object_type_b.bie_id,
            bie_place_2_id=object_a_bie_id,
            bie_relation_type_id=BieCoreRelationTypes.BIE_WHOLES_PARTS.item_bie_identity,
            b_sequence_name=BSequenceNames(
                initial_b_sequence_name_list=['object_type_b_whole_part'])))

    return \
        object_type_b


def _create_object_type_b_bie_base_identity(
        *,
        object_a_bie_id: BieIds,
        object_b_value: str) \
        -> BieBaseIdentities:
    places = \
        ObjectTypeBIdentityVectorPlaces(
            object_a_bie_id=object_a_bie_id,
            object_b_value=object_b_value)

    return \
        create_bie_base_identity_from_bie_identity_vector(
            identity_vector=ObjectTypeBIdentityVector(
                bie_hr_name=object_b_value,
                places=places))
```

Notes:
- Factory accepts `bie_id_registerer: BieIdRegisterer` — use `BieIdRegisterer` (wraps real registry) in production, `NoOpBieIdRegisterer` in unit tests
- `register_bie_id(bie_base_identity=...)` — registers the object and its type-instance relation in one call
- `issue_and_register_bie_id(request=RelationBieIdRequest(...))` — registers a relation between two objects
- The private `_create_*_bie_base_identity` helper isolates identity construction — testable independently
- For type-parameterized vectors (Style B), pass `bie_type=BieDomainNameTypes.BIE_OBJECT_TYPE_B` to the vector constructor

## Registration

Registration is done inside factory functions via `BieIdRegisterer` (see Factory Function template above).

The canonical methods are:
- `bie_id_registerer.register_bie_id(bie_base_identity=...)` — registers an object and its type-instance relation
- `bie_id_registerer.issue_and_register_bie_id(request=RelationBieIdRequest(...))` — registers a relation between two objects

`RelationBieIdRequest` fields:
- `bie_place_1_id` — part/child object's `bie_id`
- `bie_place_2_id` — whole/parent object's `bie_id`
- `bie_relation_type_id` — e.g., `BieCoreRelationTypes.BIE_WHOLES_PARTS.item_bie_identity`
- `b_sequence_name` — a `BSequenceNames` with a descriptive label

**Deprecated patterns — do NOT use:**
- `register_bie_object_and_type_instance()` / `register_bie_relation()` helper functions
- Direct `bie_infrastructure_registry.create_and_register_bie_id()` calls inside domain objects
- `EntityBieIdRequest` in registration code (use `register_bie_id` instead for entity registration)
