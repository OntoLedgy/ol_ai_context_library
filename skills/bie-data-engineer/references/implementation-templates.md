# Implementation Templates

All templates are derived from the actual Excel domain implementation. Follow these patterns exactly.

## Domain Types Enum

```python
from enum import auto
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import BieEnums


class BieDomainNameEnums(
        BieEnums):
    NOT_SET = \
        auto()

    BIE_ENTITY_A_TYPE = \
        auto()

    BIE_ENTITY_B_TYPE = \
        auto()
```

Notes:
- Extends `BieEnums` (not `Enum` directly)
- Class inheritance on separate indented line
- Each member on its own line with `= \` continuation and `auto()` indented below
- Always include `NOT_SET` as first member
- Member names: `BIE_` prefix + descriptive name + `_TYPE` suffix

## Single-Input BIE ID Creator Function

For entities identified by a single input value.

```python
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import BieIdCreationFacade
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.objects.bie_ids import BieIds
from your_domain.bie_infrastructure.your_domain_enums import BieDomainNameEnums


def create_entity_a_bie_id(
        entity_a_name: str) \
        -> BieIds:
    input_object = \
        entity_a_name

    bie_domain_type = \
        BieDomainNameEnums.BIE_ENTITY_A_TYPE

    entity_a_bie_id = \
        BieIdCreationFacade.create_bie_id_for_single_object(
            input_object=input_object,
            bie_domain_type=bie_domain_type)

    return \
        entity_a_bie_id
```

## Multi-Input (Order-Sensitive) BIE ID Creator Function

For entities identified by multiple ordered inputs.

```python
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import BieIdCreationFacade
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.objects.bie_ids import BieIds
from your_domain.bie_infrastructure.your_domain_enums import BieDomainNameEnums
from your_domain.bie_infrastructure.bie_id_creators.entity_a_bie_id_creator import create_entity_a_bie_id
from your_domain.bie_infrastructure.bie_id_creators.entity_b_bie_id_creator import create_entity_b_bie_id


def create_entity_c_bie_id(
        entity_a_name: str,
        entity_b_name: str) \
        -> BieIds:
    entity_a_bie_id = \
        create_entity_a_bie_id(
            entity_a_name=entity_a_name)

    entity_b_bie_id = \
        create_entity_b_bie_id(
            entity_b_name=entity_b_name)

    input_objects = \
        [
            entity_a_bie_id,
            entity_b_bie_id
        ]

    bie_domain_type = \
        BieDomainNameEnums.BIE_ENTITY_C_TYPE

    entity_c_bie_id = \
        BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
            input_objects=input_objects,
            bie_domain_type=bie_domain_type)

    return \
        entity_c_bie_id
```

## Domain Object Class (with base_bie_id_components pattern)

For objects that compute bie_id from components and delegate to a base class.

```python
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import BieIdCreationFacade
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.objects.bie_ids import BieIds
from your_domain.bie_infrastructure.your_domain_enums import BieDomainNameEnums
from your_domain.objects.your_domain_base_objects import YourDomainBaseObjects


class EntityCObjects(
        YourDomainBaseObjects):
    def __init__(
            self,
            entity_a_bie_id: BieIds,
            entity_b_name: str) \
            -> None:
        base_bie_id_components = \
            [
                BieDomainNameEnums.BIE_ENTITY_C_TYPE.item_bie_identity,
                entity_a_bie_id,
                entity_b_name
            ]

        base_bie_id = \
            BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
                input_objects=base_bie_id_components)

        super().__init__(
            base_bie_id=base_bie_id)

        self.entity_a_bie_id = \
            entity_a_bie_id

        self.entity_b_name = \
            entity_b_name
```

## Registration Helper Function

```python
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.common_knowledge.bie_core_relation_types import BieCoreRelationTypes
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import BieEnums
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.infrastructure.registrations.bie_infrastructure_registries import BieInfrastructureRegistries
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.objects.bie_ids import BieIds
from nf_common_base.b_source.services.identification_services.naming_service.b_sequence_names import BSequenceNames


def register_bie_ids(
        bie_infrastructure_registry: BieInfrastructureRegistries,
        bie_place_1_id: BieIds,
        bie_id_place_1_type: BieEnums,
        bie_place_2_id: BieIds,
        bie_place_1_object_name: str,
        bie_relation_type: BieCoreRelationTypes) \
        -> None:
    bie_place_1_object_name = \
        str(bie_place_1_object_name) if bie_place_1_object_name else 'None'

    bie_place_1_sequence_name = \
        BSequenceNames(
            initial_b_sequence_name_list=[bie_place_1_object_name])

    bie_infrastructure_registry.register_bie_id_and_type_instance(
        bie_item_id=bie_place_1_id,
        bie_sequence_name=bie_place_1_sequence_name,
        bie_id_type_id=bie_id_place_1_type.item_bie_identity)

    bie_infrastructure_registry.register_bie_relation(
        bie_place_1_id=bie_place_1_id,
        bie_place_2_id=bie_place_2_id,
        bie_relation_type_id=bie_relation_type.item_bie_identity)
```
