# Orchestration Conventions

Grounded in the bclearer PDK templates at `ol_bclearer_pdk/libraries/core/bclearer_core/pipeline_builder/templates/`.

---

## Execution Call Chain

The full call chain from application entry to atomic B-unit:

```
run_{domain}_b_clearer_pipeline_b_application()      ← application_runner.py
    ↓ run_b_application(app_startup_method=...)
run_{domain}_b_clearer_pipelines()                    ← domain_b_clearer_pipelines_runner.py
    ↓ @run_and_log_function()
run_{pipeline_name}()                                 ← {pipeline_name}_runner.py
    ↓ @run_and_log_function()
orchestrate_{pipeline_name}()                         ← pipeline_orchestrator.py
    ↓ __run_contained_bie_pipeline_components()
orchestrate_{thin_slice_name}()                       ← thin_slice_orchestrator.py
    ↓ __run_contained_bie_pipeline_components()
orchestrate_{pipeline_name}_{stage_name}()            ← stage orchestrator
    ↓ @run_and_log_function()  __run_contained_bie_pipeline_components()
[optional] orchestrate_{pipeline_name}_{stage}_{sub_stage}()  ← sub-stage orchestrator
    ↓ __run_contained_bie_pipeline_components()
create_and_run_b_unit(b_unit_type=SomeBUnits)         ← one per B-unit
```

---

## Application Entry Point

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

`run_b_application` is the bclearer application lifecycle wrapper — it handles
startup, logging initialisation, and top-level error reporting.

---

## Pipelines Runner

Aggregates all pipelines in the domain. Each pipeline has its own runner imported here:

```python
# {domain_name}_b_clearer_pipelines_runner.py

from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper_latest import (
    run_and_log_function,
)
try:
    from {domain_name}.b_source.app_runners.runners.{pipeline_name}_runner import (
        run_{pipeline_name},
    )
except ImportError:  # pragma: no cover - legacy package structure
    from bclearer_pipelines.{domain_name}.b_source.app_runners.runners.{pipeline_name}_runner import (
        run_{pipeline_name},
    )


@run_and_log_function()
def run_{domain_name}_b_clearer_pipelines() \
        -> None:
    run_{pipeline_name}()
    # add more pipeline calls here as domain grows
```

---

## Pipeline Runner

One per pipeline. Decorated with `@run_and_log_function()`:

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

---

## Pipeline Orchestrator

Calls thin slice orchestrators. Uses the `__run_contained_bie_pipeline_components`
private function pattern — the public orchestrate function delegates immediately.

For **bare B-unit** pipelines (no shared state):

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

For **object-passing** pipelines, the universe is received as a parameter and forwarded:

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

## Thin Slice Orchestrator

Calls stage orchestrators in fixed order (only the stages that exist).

For **bare B-unit** pipelines:

```python
# {thin_slice_name}_orchestrator.py

from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.stages.{pipeline_name}_1c_collect_orchestrator import (
    orchestrate_{pipeline_name}_1c_collect,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.stages.{pipeline_name}_3e_evolve_orchestrator import (
    orchestrate_{pipeline_name}_3e_evolve,
)


def orchestrate_{thin_slice_name}():
    __run_contained_bie_pipeline_components()


def __run_contained_bie_pipeline_components() \
        -> None:
    orchestrate_{pipeline_name}_1c_collect()
    orchestrate_{pipeline_name}_3e_evolve()
```

For **object-passing** pipelines, forward the universe — do not rename it:

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
```

---

## Stage Orchestrator

Each stage orchestrator is decorated with `@run_and_log_function()`. It either:
- Calls sub-stage orchestrators (if the stage has sub-stages), or
- Calls `create_and_run_b_unit()` for each B-unit directly

For **bare B-unit** pipelines:

```python
# {pipeline_name}_1c_collect_orchestrator.py

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

For **object-passing** pipelines, the universe is forwarded with the **same parameter
name** — it is not renamed per stage:

```python
# {pipeline_name}_1c_collect_orchestrator.py

from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper_latest import (
    run_and_log_function,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.pipeline.universes.b_clearer_run_universes import (
    BClearerRunUniverses,
)
from bclearer_pipelines.{domain_name}.b_source.common.operations.b_units.b_unit_creator_and_runner import (
    create_and_run_b_unit,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.objects.b_units.{pipeline_name}_1c_collect.ca_read_source_b_units import (
    CaReadSourceBUnits,
)


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
```

---

## Sub-Stage Orchestrator

Same pattern as stage orchestrator, without the `@run_and_log_function()` decorator:

```python
# {pipeline_name}_{stage_name}_{sub_stage_name}_orchestrator.py

def orchestrate_{pipeline_name}_{stage_name}_{sub_stage_name}():
    __run_contained_bie_pipeline_components()


def __run_contained_bie_pipeline_components() \
        -> None:
    create_and_run_b_unit(
        b_unit_type=Ea1SomeBUnits)
    create_and_run_b_unit(
        b_unit_type=Ea2AnotherBUnits)
```

---

## B-Unit Creation and Execution

B-units are instantiated and run via `create_and_run_b_unit()`:

```python
# common/operations/b_units/b_unit_creator_and_runner.py

def create_and_run_b_unit(
        b_unit_type,
        input_object=None) \
        -> None:
    if input_object is None:
        b_unit = b_unit_type()
    else:
        b_unit = b_unit_type(
            input_object=input_object)
    b_unit.run()
```

- **Bare B-unit**: `create_and_run_b_unit(b_unit_type=SomeBUnits)`
- **Object-passing B-unit**: `create_and_run_b_unit(b_unit_type=SomeBUnits, input_object=universe)`

---

## `@run_and_log_function()` Decorator

Applied to:
- All pipeline runners (`run_{pipeline_name}`)
- All pipelines runners (`run_{domain}_b_clearer_pipelines`)
- All stage orchestrators (`orchestrate_{pipeline_name}_{stage_name}`)

Import:
```python
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper_latest import (
    run_and_log_function,
)
```

The decorator logs function entry, exit, and any exceptions with timing information.
It is the bclearer mechanism for structured execution tracing.

---

## Universe Lifecycle

```
run_{domain}_b_clearer_pipeline_b_application()
    ↓
run_{pipeline_name}()                              ← Universe created here
    ↓ pass bclearer_run_universe
orchestrate_{pipeline_name}(bclearer_run_universe)
    ↓ pass bclearer_run_universe
orchestrate_{thin_slice_name}(bclearer_run_universe)
    ↓ pass bclearer_run_universe (same name at every stage)
orchestrate_{pipeline_name}_1c_collect(bclearer_run_universe)  → B-units populate registers
orchestrate_{pipeline_name}_2l_load(bclearer_run_universe)     → B-units process registers
orchestrate_{pipeline_name}_3e_evolve(bclearer_run_universe)   → B-units build domain objects
orchestrate_{pipeline_name}_4a_assimilate(bclearer_run_universe) → B-units reconcile registers
orchestrate_{pipeline_name}_5r_reuse(bclearer_run_universe)    → B-units export from Universe
    ↓
[Universe disposed or serialised via universe.export_to_disk()]
```

**Universe creation rule**: Create the Universe at the **runner level**,
not inside a stage. This ensures all stages share the same Universe instance.

**Universe naming rule**: Do not rename the universe parameter between stages.
Use `bclearer_run_universe` as the parameter name from the pipeline orchestrator
downward through all stages and sub-stages. The runner may use a domain-specific
variable name (e.g. `neo4j_import_spoke_bclearer_run_universe`) when creating the
universe, but the orchestrator parameter name is always the generic
`bclearer_run_universe`.

---

## Configuration Passing Convention

- Pipeline configuration (input paths, output paths, parameters) is injected into the
  Universe's configuration registry before stage execution begins
- Configuration is set in the pipeline runner or orchestrator, not in individual B-units
- B-units read configuration from `universe.get_configuration(ConfigEnum.SOME_KEY)`
- Enum keys for configuration live in `{pipeline_name}/objects/enums/`
- Environment variables are read **once** at the application entry point or pipeline
  runner, then injected into the Universe — B-units and orchestrators never call
  `os.getenv()`
- All file paths must be **absolute** by the time they enter the Universe — the
  application layer resolves relative paths before injection

For full configuration rules, templates, and the application-pipeline boundary
contract, see `bclearer-pipeline-engineer/references/configuration-management.md`.

---

## Environment Setup

bclearer pipelines require:

```bash
# Required environment variable
export BCLEARER_REPO_ROOT=/path/to/bclearer/ol_bclearer_pdk

# PYTHONPATH (set by startup.sh or test runner)
export PYTHONPATH="${BCLEARER_REPO_ROOT}/libraries/core:\
${BCLEARER_REPO_ROOT}/libraries/orchestration_services:\
${BCLEARER_REPO_ROOT}/libraries/interop_services"
```

---

## Testing Convention

### End-to-End Test

```python
# tests/universal/e2e/test_{domain_name}_pipeline.py

def test_{domain_name}_b_clearer_pipeline_b_application(
        e2e_test_setup,
        e2e_test_teardown):
    run_{domain_name}_b_clearer_pipeline_b_application()
    # assert expected outputs here
    assert True  # replace with meaningful assertions
```

### E2E Test Fixtures

```python
# conftest.py

@pytest.fixture(scope='module')
def e2e_test_setup():
    # set up test inputs (copy test data to expected input location, etc.)
    pass


@pytest.fixture(scope='module')
def e2e_test_teardown():
    # clean up test outputs
    pass
```

### Stage Unit Tests

Each stage is independently testable by constructing a Universe with test data in
registers and running only that stage's orchestrator. No mocking of other stages needed.

---

## Multi-Pipeline Orchestration

When a domain has multiple pipelines, each runs sequentially in the domain pipelines runner:

```python
@run_and_log_function()
def run_{domain_name}_b_clearer_pipelines() \
        -> None:
    run_pipeline_one()
    run_pipeline_two()
    run_pipeline_three()
```

Pipelines that depend on outputs from earlier pipelines read their inputs from the
file system (written by the prior pipeline's `5r_reuse` stage). They do not share a
Universe directly — data passes between pipelines via files, not in-memory objects.
