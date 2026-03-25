# Code Locations

## Core Framework

### Identification Services

Package: `bclearer_orchestration_services.identification_services.b_identity_ecosystem`

| Class | Module path (relative to package) |
|-------|----------------------------------|
| BieIds | `objects.bie_ids` |
| BieEnums | `common_knowledge.bie_enums` |
| BieDomainTypes | `common_knowledge.bie_domain_types` |
| BieCoreRelationTypes | `common_knowledge.bie_core_relation_types` |
| BieCoreDomainTypes | `common_knowledge.bie_core_domain_types` |
| BieIdCreationFacade | `bie_id_creation_module.bie_id_creation_facade` |
| BieIdentityVectorBase | `bie_id_creation_module.identity_vectors.bie_identity_vector_base` |
| CommonIdentityVector | `bie_id_creation_module.identity_vectors.common_identity_vector` |
| BieVectorStructureTypes | `bie_id_creation_module.common_knowledge.types.bie_vector_structure_types` |
| BieIdRegistries | `objects.bie_id_registries` |
| BieIdUniverses | `objects.bie_id_universes` |
| BieInfrastructureRegistries | `infrastructure.registrations.bie_infrastructure_registries` |
| EntityBieIdRequest | `registrations.helpers.registerers.bie_id_issue_requests` |
| RelationBieIdRequest | `registrations.helpers.registerers.bie_id_issue_requests` |
| BieIdIssueScopes | `registrations.helpers.registerers.bie_id_issue_requests` |
| BieIdIssueResult | `registrations.helpers.registerers.bie_id_issue_result` |

### Naming Service

Package: `bclearer_orchestration_services.identification_services.naming_service`

| Class | Module path (relative to package) |
|-------|----------------------------------|
| BSequenceNames | `b_sequence_names` |

### Base Object Classes

Package: `bclearer_core.bie`

| Class | Module path (relative to package) |
|-------|----------------------------------|
| BieObjects | `top.bie_objects` |
| BieDomainObjects | `domain.bie_domain_objects` |
| BieBaseIdentities | `top.bie_base_identities` |
| create_bie_base_identity_from_bie_identity_vector | `top.bie_base_identities` |

### Registration Helpers

Package: `bclearer_core.infrastructure.session`

| Class | Module path (relative to package) |
|-------|----------------------------------|
| BieIdRegisterer | `bie_id_registerers.bie_id_registerer` |
| NoOpBieIdRegisterer | `bie_id_registerers.bie_id_registerer` |

## File System Snapshot Domain Reference (canonical implementation example)

Package: `bclearer_orchestration_services.file_system_snapshot_service.universe`

| File | Purpose |
|------|---------|
| `common_knowledge/bie_file_system_snapshot_domain_types.py` | Domain types enum (extends `BieDomainTypes`) |
| `bie/bie_id_creators/file_system_snapshot_identity_vectors.py` | Identity vectors (NamedTuple places + `CommonIdentityVector` subclasses) |
| `bie/bie_id_creators/file_system_snapshot_object_bie_id_creator.py` | Three-tier creator (create/calculate/issue) |
| `bie/bie_id_creators/file_reference_number_extended_object_bie_id_creator.py` | Three-tier creator for extended object |
| `objects/snapshots/file_system_snapshot_objects.py` | Domain object base class |
| `objects/snapshots/individual_file_system_snapshot_objects.py` | Domain object — receives `bie_base_identity`, no `_create_vector()` |
| `objects/snapshots/individual_file_system_snapshot_files.py` | Concrete domain object — receives `bie_base_identity` |
| `objects/snapshots/factories/individual_file_system_snapshot_files_factory.py` | Factory — places → vector → BieBaseIdentities → object → register |
| `objects/extended/file_reference_numbers.py` | Extended object — receives `bie_base_identity` |
| `objects/extended/factories/file_reference_numbers_factory.py` | Factory for extended object |
| `objects/verses/file_system_snapshot_universes.py` | Universe setup and orchestration |
| `objects/verses/factories/file_system_snapshot_universes_factory.py` | Universe factory |

## Documentation

| File | Purpose |
|------|---------|
| `docs/bie_implementation_analysis.md` | Full BIE design and implementation guide |
