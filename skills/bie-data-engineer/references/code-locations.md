# Code Locations

## Core Framework

Base path: `nf_common/nf_common_base/b_source/services/identification_services/b_identity_ecosystem/`

| Class | Path (relative to base) |
|-------|------------------------|
| BieIds | `objects/bie_ids.py` |
| BieObjects | (at `nf_common/nf_common_base/b_source/common/bie/top/bie_objects.py`) |
| BieDomainObjects | (at `nf_common/nf_common_base/b_source/common/bie/domain/bie_domain_objects.py`) |
| BieEnums | `common_knowledge/bie_enums.py` |
| BieCoreRelationTypes | `common_knowledge/bie_core_relation_types.py` |
| BieIdCreationFacade | `bie_id_creation_module/bie_id_creation_facade.py` |
| BieIdRegistries | `objects/bie_id_registries.py` |
| BieIdUniverses | `objects/bie_id_universes.py` |
| BieInfrastructureRegistries | `infrastructure/registrations/bie_infrastructure_registries.py` |
| BSequenceNames | (at `nf_common/nf_common_base/b_source/services/identification_services/naming_service/b_sequence_names.py`) |

## Excel Domain Reference (canonical implementation example)

Base path: `bie_excel/bie_excel_base/b_source/bie_excel_pipeline/`

| File | Purpose |
|------|---------|
| `bie_infrastructure/bie_excel_enums.py` | Domain types enum |
| `bie_infrastructure/bie_id_creators/excel_column_type_bie_id_creator.py` | Single-input creator |
| `bie_infrastructure/bie_id_creators/excel_row_type_bie_id_creator.py` | Single-input creator |
| `bie_infrastructure/bie_id_creators/excel_coordinate_type_bie_id_creator.py` | Multi-input creator |
| `bie_infrastructure/bie_ids_registerers/bie_ids_registerer.py` | Registration helper |
| `objects/structure/nf_openpyxl_wrappers/nf_openpyxl_wrappers.py` | Base wrapper (bie_id from components) |
| `objects/structure/nf_openpyxl_wrappers/workbook_wrappers.py` | Composite object |
| `objects/structure/nf_openpyxl_wrappers/worksheet_wrappers.py` | Composite object |
| `objects/structure/nf_openpyxl_wrappers/cell_wrappers.py` | Leaf object with registration |

## File System Domain

Base path: `nf_common/nf_common_base/b_source/services/identification_services/bie_file_system_domain/`

| File | Purpose |
|------|---------|
| `creators/file_immutable_stage_bie_id_creator.py` | Content-based file identity |

## Documentation

| File | Purpose |
|------|---------|
| `docs/bie_implementation_analysis.md` | Full BIE design and implementation guide |
