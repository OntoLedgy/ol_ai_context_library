# Pipeline Implementation Reference

Grounded in the bclearer PDK templates at `ol_bclearer_pdk/libraries/core/bclearer_core/pipeline_builder/templates/`
and the bclearer PDK source at `ol_bclearer_pdk/libraries/`.

---

## Canonical Reference

The canonical bclearer pipeline implementation is the File System Snapshot service:

```
bclearer_interop_services.file_system_service.bie_file_system_domain
```

Read this when implementing a pipeline that requires BIE identity construction — it
demonstrates stage separation, BIE factory construction order, and Universe wiring.

---

## Implementation Order

Follow this order within any pipeline implementation. Do not implement later layers
before earlier ones:

```
1. Common knowledge           — enums, types, constants for the pipeline
2. BIE domain objects         — delegate to bie-data-engineer (if pipeline uses BIE identity)
3. Stage B-units              — implement each stage in order: 1c → 2l → 3e → 4a → 5r
4. Stage orchestrators        — wire B-units into stages
5. Thin slice orchestrator    — wire stages into the thin slice
6. Pipeline orchestrator      — wire thin slices into the pipeline
7. Pipeline runner            — wrap the pipeline with @run_and_log_function()
8. Domain pipelines runner    — aggregate all pipeline runners for the domain
9. Application entry point    — wrap the domain runner with run_b_application()
```

---

## File Naming Conventions

Apply bclearer BORO naming (see `references/bclearer-code-style.md`):

| Artefact | File Name Pattern | Example |
|----------|------------------|---------|
| B-unit (bare) | `{stage_prefix}{letter}_b_units.py` | `ca_read_csv_b_units.py` |
| B-unit (object-passing) | same | `ea_build_transactions_b_units.py` |
| Stage orchestrator | `{pipeline_name}_{stage_name}_orchestrator.py` | `accounts_pipeline_1c_collect_orchestrator.py` |
| Sub-stage orchestrator | `{pipeline_name}_{stage}_{sub_stage}_orchestrator.py` | `accounts_pipeline_3e_evolve_parse_headers_orchestrator.py` |
| Thin slice orchestrator | `{thin_slice_name}_orchestrator.py` | `main_slice_orchestrator.py` |
| Pipeline orchestrator | `{pipeline_name}_orchestrator.py` | `accounts_pipeline_orchestrator.py` |
| Pipeline runner | `{pipeline_name}_runner.py` | `accounts_pipeline_runner.py` |
| Domain pipelines runner | `{domain_name}_b_clearer_pipelines_runner.py` | `finance_b_clearer_pipelines_runner.py` |
| Application entry point | `{domain_name}_b_clearer_pipeline_b_application_runner.py` | `finance_b_clearer_pipeline_b_application_runner.py` |
| Universe | `{pipeline_name}_universes.py` | `accounts_pipeline_universes.py` |
| Pipeline enums | `{concern}_enums.py` | `registry_names_enums.py`, `configuration_keys_enums.py` |
| B-unit creator helper | `b_unit_creator_and_runner.py` | (fixed name, in `common/operations/b_units/`) |

---

## Class Naming Conventions

| Artefact | Class Name Pattern | Example |
|----------|-------------------|---------|
| B-unit (bare) | `{NameInCamelCase}BUnits` | `CaReadCsvBUnits` |
| B-unit (object-passing) | same | `EaBuildTransactionsBUnits` |
| Stage orchestrator | (module-level functions only, no class) | — |
| Universe | `{PipelineName}Universes` | `AccountsPipelineUniverses` |
| Registry | `{Concern}Registries` | `TransactionRegistries` |
| Register | `{Concern}Registers` | `RawTransactionsRegisters` |

---

## Bare B-Unit Template

```python
# {stage_prefix}{letter}_{description}_b_units.py

from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_core.objects.b_units import BUnits
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


class CaReadCsvBUnits(BUnits):

    def __init__(self):
        pass

    def run(
            self) \
            -> None:
        log_inspection_message(
            message='Running bUnit: {}'.format(
                self.__class__.__name__),
            logging_inspection_level_b_enum=\
                LoggingInspectionLevelBEnums.INFO)
        self.b_unit_process_function()

    def b_unit_process_function(
            self) \
            -> None:
        # implement here
        pass
```

---

## Object-Passing B-Unit Template

```python
# {stage_prefix}{letter}_{description}_b_units.py

from bclearer_core.objects.b_units import (
    BUnitsWithObjectPassingAndReturning,
)


class EaBuildTransactionsBUnits(
        BUnitsWithObjectPassingAndReturning):

    def __init__(
            self,
            input_object=None):
        super().__init__(
            input_object=input_object)

    def _b_unit_process_function(
            self) \
            -> None:
        # self.input_object is the Universe (or other typed object)
        # read from registries, build domain objects, write back
        pass
```

---

## Stage Orchestrator Template

```python
# {pipeline_name}_{stage_name}_orchestrator.py

from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper_latest import (
    run_and_log_function,
)
from bclearer_pipelines.{domain_name}.b_source.common.operations.b_units.b_unit_creator_and_runner import (
    create_and_run_b_unit,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.objects.b_units.{pipeline_name}_1c_collect.ca_read_source_b_units import (
    CaReadSourceBUnits,
)


@run_and_log_function()
def orchestrate_{pipeline_name}_1c_collect() \
        -> None:
    __run_contained_bie_pipeline_components()


def __run_contained_bie_pipeline_components() \
        -> None:
    create_and_run_b_unit(
        b_unit_type=CaReadSourceBUnits)
```

For object-passing B-units, the universe is received as a parameter (created at the
runner level) and forwarded to each B-unit. Do not rename the parameter between stages:

```python
@run_and_log_function()
def orchestrate_{pipeline_name}_1c_collect(
        bclearer_run_universe: BClearerRunUniverses) \
        -> None:
    __run_contained_bie_pipeline_components(
        bclearer_run_universe=bclearer_run_universe)


def __run_contained_bie_pipeline_components(
        bclearer_run_universe: BClearerRunUniverses) \
        -> None:
    create_and_run_b_unit(
        b_unit_type=CaReadSourceBUnits,
        input_object=bclearer_run_universe)
    create_and_run_b_unit(
        b_unit_type=CbValidateInputBUnits,
        input_object=bclearer_run_universe)
```

---

## Thin Slice Orchestrator Template

For bare B-unit pipelines:

```python
# {thin_slice_name}_orchestrator.py

from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.stages.{pipeline_name}_1c_collect_orchestrator import (
    orchestrate_{pipeline_name}_1c_collect,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.stages.{pipeline_name}_3e_evolve_orchestrator import (
    orchestrate_{pipeline_name}_3e_evolve,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.stages.{pipeline_name}_5r_reuse_orchestrator import (
    orchestrate_{pipeline_name}_5r_reuse,
)


def orchestrate_{thin_slice_name}():
    __run_contained_bie_pipeline_components()


def __run_contained_bie_pipeline_components() \
        -> None:
    orchestrate_{pipeline_name}_1c_collect()
    orchestrate_{pipeline_name}_3e_evolve()
    orchestrate_{pipeline_name}_5r_reuse()
```

For object-passing pipelines, forward the universe with the same parameter name:

```python
# {thin_slice_name}_orchestrator.py

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.pipeline.universes.b_clearer_run_universes import (
    BClearerRunUniverses,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.stages.{pipeline_name}_1c_collect_orchestrator import (
    orchestrate_{pipeline_name}_1c_collect,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.stages.{pipeline_name}_3e_evolve_orchestrator import (
    orchestrate_{pipeline_name}_3e_evolve,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.stages.{pipeline_name}_5r_reuse_orchestrator import (
    orchestrate_{pipeline_name}_5r_reuse,
)


def orchestrate_{thin_slice_name}(
        bclearer_run_universe: BClearerRunUniverses) \
        -> None:
    __run_contained_bie_pipeline_components(
        bclearer_run_universe=bclearer_run_universe)


def __run_contained_bie_pipeline_components(
        bclearer_run_universe: BClearerRunUniverses) \
        -> None:
    orchestrate_{pipeline_name}_1c_collect(
        bclearer_run_universe=bclearer_run_universe)
    orchestrate_{pipeline_name}_3e_evolve(
        bclearer_run_universe=bclearer_run_universe)
    orchestrate_{pipeline_name}_5r_reuse(
        bclearer_run_universe=bclearer_run_universe)
```

---

## Pipeline Orchestrator Template

For bare B-unit pipelines:

```python
# {pipeline_name}_orchestrator.py

from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.thin_slices.{thin_slice_name}_orchestrator import (
    orchestrate_{thin_slice_name},
)


def orchestrate_{pipeline_name}():
    __run_contained_bie_pipeline_components()


def __run_contained_bie_pipeline_components() \
        -> None:
    orchestrate_{thin_slice_name}()
```

For object-passing pipelines:

```python
# {pipeline_name}_orchestrator.py

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.pipeline.universes.b_clearer_run_universes import (
    BClearerRunUniverses,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.thin_slices.{thin_slice_name}_orchestrator import (
    orchestrate_{thin_slice_name},
)


def orchestrate_{pipeline_name}(
        bclearer_run_universe: BClearerRunUniverses) \
        -> None:
    __run_contained_bie_pipeline_components(
        bclearer_run_universe=bclearer_run_universe)


def __run_contained_bie_pipeline_components(
        bclearer_run_universe: BClearerRunUniverses) \
        -> None:
    orchestrate_{thin_slice_name}(
        bclearer_run_universe=bclearer_run_universe)
```

---

## Pipeline Runner Template

For bare B-unit pipelines:

```python
# {pipeline_name}_runner.py

from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper_latest import (
    run_and_log_function,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.pipeline.{pipeline_name}_orchestrator import (
    orchestrate_{pipeline_name},
)


@run_and_log_function()
def run_{pipeline_name}() \
        -> None:
    orchestrate_{pipeline_name}()
```

For object-passing pipelines, the runner creates the universe and passes it into the
pipeline orchestrator. The runner may use a domain-specific variable name; from the
pipeline orchestrator onward, the parameter name is always `bclearer_run_universe`:

```python
# {pipeline_name}_runner.py

from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper_latest import (
    run_and_log_function,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.objects.universes.{pipeline_name}_universes import (
    {PipelineName}Universes,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.pipeline.{pipeline_name}_orchestrator import (
    orchestrate_{pipeline_name},
)


@run_and_log_function()
def run_{pipeline_name}() \
        -> None:
    {pipeline_name}_universe = \
        {PipelineName}Universes()

    orchestrate_{pipeline_name}(
        bclearer_run_universe={pipeline_name}_universe)
```

---

## Application Entry Point Template

```python
# {domain_name}_b_clearer_pipeline_b_application_runner.py

from bclearer_orchestration_services.b_app_runner_service.b_application_runner import (
    run_b_application,
)
from bclearer_pipelines.{domain_name}.b_source.app_runners.runners.{domain_name}_b_clearer_pipelines_runner import (
    run_{domain_name}_b_clearer_pipelines,
)


def run_{domain_name}_b_clearer_pipeline_b_application() \
        -> None:
    run_b_application(
        app_startup_method=run_{domain_name}_b_clearer_pipelines)
```

---

## Universe Template

Universe holds all registries and configuration for a pipeline run:

```python
# {pipeline_name}_universes.py

from bclearer_core.objects.universes.universes import Universes
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.objects.enums.registry_names_enums import (
    RegistryNamesEnums,
)


class AccountsPipelineUniverses(Universes):

    def __init__(self):
        super().__init__()
        self.__initialise_registries()

    def __initialise_registries(
            self) \
            -> None:
        self.set_registry(
            name=RegistryNamesEnums.RAW_DATA,
            registry=RawDataRegistries(
                owning_universe=self))
        self.set_registry(
            name=RegistryNamesEnums.TRANSACTIONS,
            registry=TransactionRegistries(
                owning_universe=self))
```

Enums for registry names, register names, and configuration keys live in
`{pipeline_name}/objects/enums/`.

---

## Standard Test Pattern

### Stage Unit Test

Build a Universe with test data in registers, run the stage orchestrator, assert
on Universe state afterwards. No mocking of other stages.

```python
def test_1c_collect_populates_raw_data_register():
    universe = \
        AccountsPipelineUniverses()
    # inject test config
    universe.set_configuration(
        name=ConfigKeysEnums.INPUT_PATH,
        value='tests/fixtures/sample.csv')

    orchestrate_accounts_pipeline_1c_collect(
        universe=universe)

    raw_register = \
        universe \
        .get_registry(RegistryNamesEnums.RAW_DATA) \
        .get_register(RegisterNamesEnums.CSV_ROWS)
    assert raw_register.has_content()
    assert len(raw_register.get_content()) > 0
```

### E2E Test

Calls the full application entry point. Setup/teardown fixtures manage test data:

```python
# tests/universal/e2e/test_{domain_name}_pipeline.py

def test_{domain_name}_b_clearer_pipeline_b_application(
        e2e_test_setup,
        e2e_test_teardown):
    run_{domain_name}_b_clearer_pipeline_b_application()
    # assert expected output files or database records exist
    assert True
```

---

## Verification Checklist

Beyond `ruff`, `mypy`, `pytest`, verify after implementation:

- [ ] Each stage B-unit file is in `{pipeline_name}/objects/b_units/{pipeline_name}_{stage_name}/`
- [ ] Each stage orchestrator is in `orchestrators/stages/`
- [ ] `@run_and_log_function()` applied to pipeline runners and stage orchestrators
- [ ] `create_and_run_b_unit()` used to instantiate and run all B-units (not direct instantiation)
- [ ] Universe created in the runner — not inside a stage orchestrator or B-unit
- [ ] Universe parameter named `bclearer_run_universe` consistently across all stages — not renamed per stage
- [ ] Interop service imports only in `1c_collect`, `2l_load`, `4a_assimilate` (master-store adapter only), and `5r_reuse` B-units — never in `3e_evolve`
- [ ] `2l_load` B-units do not change the data — no normalisation, no validation beyond parseability, no BIE-ing
- [ ] `4a_assimilate` B-units inject the evolved BIE fragment into the master BORO ontology object store — cross-slice merges live in `3e_evolve`, not here
- [ ] BIE factories only in `bie/` folder (if BIE domain used)
- [ ] No cross-stage imports (stage A B-units do not import stage B B-units)
- [ ] Configuration values read from Universe, not hardcoded in B-units
- [ ] Each stage has at least one independent unit test
- [ ] E2E test runs the full application entry point successfully
