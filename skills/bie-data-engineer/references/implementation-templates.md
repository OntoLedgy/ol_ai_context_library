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

```python
from typing import NamedTuple

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.common_knowledge.types.bie_vector_structure_types import \
    BieVectorStructureTypes
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.identity_vectors.common_identity_vector import \
    CommonIdentityVector
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_types import \
    BieTypes
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import \
    BieIds


class ObjectTypeAIdentityVectorPlaces(
        NamedTuple):
    object_a_name: str


class ObjectTypeAIdentityVector(
        CommonIdentityVector):
    def __init__(
            self,
            *,
            bie_type: BieTypes,
            bie_hr_name: str,
            places: ObjectTypeAIdentityVectorPlaces) \
            -> None:
        super().__init__(
            bie_domain_type=bie_type,
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
            bie_type: BieTypes,
            bie_hr_name: str,
            places: ObjectTypeBIdentityVectorPlaces) \
            -> None:
        super().__init__(
            bie_domain_type=bie_type,
            bie_hr_name=bie_hr_name,
            places=places,
            bie_vector_structure_type=BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_SENSITIVE)
```

Notes:
- Identity vector classes subclass `CommonIdentityVector` — do NOT subclass `BieIdentityVectorBase` directly
- Constructor uses keyword-only args (`*`) and takes `bie_type`, `bie_hr_name`, and typed `places`
- `bie_type` is passed in (not hardcoded) — the domain object provides it when creating the vector
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

```python
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.identity_vectors import \
    BieIdentityVectorBase
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import \
    BieIds
from bclearer_core.bie.domain.bie_domain_objects import \
    BieDomainObjects
from your_domain.common_knowledge.your_domain_types import BieDomainNameTypes
from your_domain.bie.bie_id_creators.your_domain_identity_vectors import \
    ObjectTypeBIdentityVector, ObjectTypeBIdentityVectorPlaces


class ObjectTypeBObjects(
        BieDomainObjects):
    def __init__(
            self,
            object_a_bie_id: BieIds,
            object_b_value: str) \
            -> None:
        self.object_a_bie_id = \
            object_a_bie_id

        self.object_b_value = \
            object_b_value

        identity_vector = \
            self._create_vector()

        super().__init__(
            identity_vector=identity_vector)

    def _create_vector(
            self) \
            -> BieIdentityVectorBase:
        bie_type = \
            BieDomainNameTypes.BIE_OBJECT_TYPE_B

        bie_hr_name = \
            self.object_b_value

        vector_places = \
            self._create_vector_places()

        identity_vector = \
            ObjectTypeBIdentityVector(
                bie_type=bie_type,
                bie_hr_name=bie_hr_name,
                places=vector_places)

        return \
            identity_vector

    def _create_vector_places(
            self) \
            -> ObjectTypeBIdentityVectorPlaces:
        return \
            ObjectTypeBIdentityVectorPlaces(
                object_a_bie_id=self.object_a_bie_id,
                object_b_value=self.object_b_value)
```

Notes:
- Instance attributes are set BEFORE calling `super().__init__` (they are needed by `_create_vector`)
- `_create_vector()` implements the abstract method from `BieObjects` — constructs the identity vector
- `_create_vector_places()` creates the NamedTuple places from instance attributes
- `super().__init__(identity_vector=vector)` — `BieObjects` extracts `bie_hr_name`, `bie_type`, and computes `bie_id` from the vector
- Do NOT pass `bie_id`, `base_hr_name`, or `bie_domain_type` separately — they come from the vector

## Registration Helper Functions

Uses `EntityBieIdRequest` and `RelationBieIdRequest` frozen dataclasses for all registrations.

```python
from bclearer_core.bie.domain.bie_domain_objects import \
    BieDomainObjects
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.common_knowledge.types.bie_vector_structure_types import \
    BieVectorStructureTypes
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_core_relation_types import \
    BieCoreRelationTypes
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.registrations.bie_infrastructure_registries import \
    BieInfrastructureRegistries
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.registerers.bie_id_issue_requests import \
    BieIdIssueScopes, EntityBieIdRequest, RelationBieIdRequest
from bclearer_orchestration_services.identification_services.naming_service.b_sequence_names import \
    BSequenceNames


def register_bie_object_and_type_instance(
        bie_infrastructure_registry: BieInfrastructureRegistries,
        bie_domain_object: BieDomainObjects) \
        -> None:
    bie_sequence_name = \
        BSequenceNames(
            initial_b_sequence_name_list=[bie_domain_object.base_hr_name])

    object_issue_request = \
        EntityBieIdRequest(
            input_objects=(bie_domain_object.bie_id,),
            bie_id_type_id=bie_domain_object.bie_type.item_bie_identity,
            b_sequence_name=bie_sequence_name,
            issue_scope=BieIdIssueScopes.INFRASTRUCTURE,
            bie_vector_structure_type=BieVectorStructureTypes.SINGLE_DIMENSIONAL)

    object_issue_result = \
        bie_infrastructure_registry.create_and_register_bie_id(
            request=object_issue_request)

    bie_domain_object.bie_id = \
        object_issue_result.bie_id


def register_bie_whole_part(
        bie_infrastructure_registry: BieInfrastructureRegistries,
        bie_domain_object_whole: BieDomainObjects,
        bie_domain_object_part: BieDomainObjects) \
        -> None:
    relation_issue_request = \
        RelationBieIdRequest(
            bie_place_1_id=bie_domain_object_part.bie_id,
            bie_place_2_id=bie_domain_object_whole.bie_id,
            bie_relation_type_id=BieCoreRelationTypes.BIE_WHOLES_PARTS.item_bie_identity,
            b_sequence_name=BSequenceNames(
                initial_b_sequence_name_list=['whole_part']))

    bie_infrastructure_registry.create_and_register_bie_id(
        request=relation_issue_request)
```

Notes:
- `EntityBieIdRequest` registers an object and its type-instance relation in one call
- `RelationBieIdRequest` registers a relation between two objects
- Both use `bie_infrastructure_registry.create_and_register_bie_id()` as the single entry point
- `EntityBieIdRequest.input_objects` wraps the already-computed `bie_id` in a tuple for registration
- `EntityBieIdRequest.bie_vector_structure_type` is `SINGLE_DIMENSIONAL` when registering a pre-computed bie_id
- The result's `bie_id` is assigned back to the domain object
