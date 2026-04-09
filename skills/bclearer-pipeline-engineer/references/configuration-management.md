# Configuration Management

Grounded in the bclearer PDK Universe configuration API, the orchestration
conventions from `bclearer-pipeline-architect/references/orchestration-conventions.md`,
and the PDK exemplar pipeline (`bie_core_graph`).

---

## Configuration Flow

Configuration flows one way, top-down:

```
Application layer (FastAPI, CLI, UI, test harness)
    ↓ provides configuration values
Pipeline runner / pipeline orchestrator
    ↓ injects into Universe (constructor params or set_configuration())
Stage orchestrators
    ↓ pass Universe as input_object
B-units
    ↓ read from Universe (instance attributes or get_configuration())
```

**Rules:**

- The application layer is the **only** place that determines configuration values
- The pipeline runner or pipeline orchestrator is the **only** place that injects
  configuration into the Universe
- B-units and stage orchestrators **only read** configuration — they never set it
- Configuration is never passed as function arguments between stages — it lives in
  the Universe

### Two Injection Mechanisms

The Universe supports two ways to carry configuration. Both are valid:

| Mechanism | When to use | PDK example |
|-----------|------------|-------------|
| **Constructor injection** | Typed configuration objects (workspace, source files, service configs) | `Neo4JImportSpokeBClearerRunUniverses(workspace_config=..., source_file=...)` |
| **Key-value registry** | Simple scalar values (paths, URLs, thresholds, flags) | `universe.set_configuration(name=ConfigKeysEnums.INPUT_PATH, value=...)` |

The PDK exemplar (`bie_core_graph`) uses constructor injection — the Universe
receives `WorkspaceConfigurations`, `BiePipelineUniverses`, and `Files` as
constructor parameters, and B-units access them as typed instance attributes
(`self.input_object.neo4j_entification_pipelines_workspace_configuration`).

Simpler pipelines that don't need typed configuration objects can use the
key-value registry pattern with `set_configuration()` / `get_configuration()`
and a `ConfigurationKeysEnums` enum.

Either way, the top-down flow is the same: the application layer provides values,
the pipeline runner injects them into the Universe, and B-units only read.

---

## Environment Variables

Environment variables are acceptable **only at the application entry point**.

**Rule:** Read `os.getenv()` once, at the application layer or pipeline runner.
Inject the resolved value into the Universe. B-units, orchestrators, and services
never call `os.getenv()`.

```python
# CORRECT — application entry point or pipeline runner
import os
from pathlib import Path

def run_trades_pipeline() \
        -> None:
    universe = \
        TradesPipelineUniverses()

    input_path = \
        Path(
            os.getenv(
                'TRADES_INPUT_PATH',
                '/default/path/to/trades'))

    universe.set_configuration(
        name=TradesConfigurationKeysEnums.INPUT_PATH,
        value=input_path)

    orchestrate_trades_pipeline(
        universe=universe)
```

```python
# WRONG — env var read inside a B-unit
class CaReadTradesBUnits(BUnitsWithObjectPassingAndReturning):
    def _b_unit_process_function(self) -> None:
        path = os.getenv('TRADES_INPUT_PATH')  # VIOLATION
```

---

## Path Resolution

All file paths must be **absolute** by the time they enter the Universe.

**Rules:**

- The application layer resolves relative paths to absolute paths
- The pipeline layer receives only absolute `Path` objects in configuration
- B-units never resolve paths — they read ready-to-use absolute paths from
  the Universe
- Directory creation (`mkdir`) is the responsibility of the layer that owns
  the path — typically the application layer for input paths, and the `5r_reuse`
  B-unit for output paths it writes to

```python
# CORRECT — application layer resolves to absolute
input_path = \
    Path(
        os.getenv(
            'TRADES_INPUT_PATH',
            './data/trades')) \
    .resolve()

universe.set_configuration(
    name=TradesConfigurationKeysEnums.INPUT_PATH,
    value=input_path)
```

```python
# WRONG — relative path fragility inside pipeline code
path = Path(__file__).resolve().parents[6] / 'data'  # VIOLATION
```

---

## Configuration Keys Enum Template

Every pipeline defines its configuration keys in an enum file:

```
{pipeline_name}/objects/enums/configuration_keys_enums.py
```

### Required Keys

Every pipeline must define at least:

```python
# configuration_keys_enums.py

from enum import Enum


class TradesConfigurationKeysEnums(
        Enum):

    INPUT_PATH = \
        'input_path'
    OUTPUT_PATH = \
        'output_path'
```

### Extended Keys

Add domain-specific keys as needed:

```python
class TradesConfigurationKeysEnums(
        Enum):

    INPUT_PATH = \
        'input_path'
    OUTPUT_PATH = \
        'output_path'
    SERVICE_URL = \
        'service_url'
    BATCH_SIZE = \
        'batch_size'
    COMPLEXITY_THRESHOLD = \
        'complexity_threshold'
```

**Naming convention:** Keys use `UPPER_SNAKE_CASE`. Values use `lower_snake_case`
strings that describe the configuration concern.

---

## Application-Pipeline Boundary Contract

The application layer and the pipeline layer have a strict contract:

### What the Application Must Provide

Before calling `run_{pipeline_name}()` or `orchestrate_{pipeline_name}()`,
the application layer must:

1. Create the Universe instance
2. Populate all required configuration keys via `universe.set_configuration()`
3. Ensure all path values are absolute and the input paths exist
4. Pass the populated Universe to the pipeline orchestrator

### What the Pipeline Must Not Do

The pipeline (orchestrators and B-units) must not:

- Read environment variables
- Resolve relative paths
- Hardcode file paths or service URLs
- Assume a working directory
- Import application-layer modules

### Standalone Pipeline Entry Point

When a pipeline runs standalone (not behind an application server), the pipeline
runner acts as its own application layer:

```python
# {pipeline_name}_runner.py (standalone mode)

import os
from pathlib import Path

from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper_latest import (
    run_and_log_function,
)


@run_and_log_function()
def run_trades_pipeline() \
        -> None:
    universe = \
        TradesPipelineUniverses()

    # --- application-layer responsibility (env → universe) ---
    universe.set_configuration(
        name=TradesConfigurationKeysEnums.INPUT_PATH,
        value=Path(
            os.getenv(
                'TRADES_INPUT_PATH',
                '/data/trades/input')) \
            .resolve())

    universe.set_configuration(
        name=TradesConfigurationKeysEnums.OUTPUT_PATH,
        value=Path(
            os.getenv(
                'TRADES_OUTPUT_PATH',
                '/data/trades/output')) \
            .resolve())

    # --- pipeline-layer responsibility ---
    orchestrate_trades_pipeline(
        universe=universe)
```

### Application Server Entry Point

When a pipeline is invoked from an application server (e.g. FastAPI), the
application service creates and populates the Universe before invoking the
pipeline:

```python
# application_service.py (e.g. FastAPI route handler)

class PipelineOrchestrationOperation:

    def execute(
            self,
            input_path: Path,
            output_path: Path) \
            -> None:
        universe = \
            TradesPipelineUniverses()

        universe.set_configuration(
            name=TradesConfigurationKeysEnums.INPUT_PATH,
            value=input_path.resolve())

        universe.set_configuration(
            name=TradesConfigurationKeysEnums.OUTPUT_PATH,
            value=output_path.resolve())

        orchestrate_trades_pipeline(
            universe=universe)
```

---

## Non-BIE Pipeline Configuration

Pipelines that do not use BIE identity follow the same configuration pattern.
The only difference is that they have no BIE-specific enums or registries.

```python
# For a non-BIE pipeline (e.g. trades, invoices, reports):

class TradesConfigurationKeysEnums(
        Enum):
    INPUT_PATH = 'input_path'
    OUTPUT_PATH = 'output_path'
    # domain-specific keys — no BIE keys needed
    SOURCE_FORMAT = 'source_format'
    TRADE_DATE_COLUMN = 'trade_date_column'
```

The Universe template, configuration flow, and boundary contract are identical
regardless of whether the pipeline produces BIE domain objects.

---

## PDK Framework Feature Flags

PDK-level static configuration classes are a separate category from pipeline
configuration. These are framework toggles that control cross-cutting concerns
(output format, inspection, database export) and are acceptable to read directly
in pipeline runners and orchestrators:

```python
# These are PDK framework flags — OK to read directly
from bclearer_core.configurations.bclearer_configurations import (
    BClearerConfigurations,
)
from bclearer_core.configurations.bclearer_domain_configurations import (
    BClearerDomainConfigurations,
)

if BClearerConfigurations.ENABLE_SQLITE_DATABASE_INSPECTION:
    export_to_sqlite(...)

if BClearerDomainConfigurations.ENABLE_B_CLEARER_DOMAIN_INSPECTION:
    finalise_pipeline_run(...)
```

**The distinction:**

| Category | Examples | Where to read | Inject into Universe? |
|----------|---------|--------------|----------------------|
| Pipeline configuration | Input paths, output paths, service URLs, thresholds | Application entry point only | Yes — always |
| PDK framework flags | `ENABLE_SQLITE_DATABASE_INSPECTION`, `ENABLE_B_CLEARER_DOMAIN_INSPECTION` | Pipeline runner or orchestrator | No — read from static class |

PDK framework flags are set at application startup (via `BConfigurations`,
`BClearerConfigurations`, etc.) and are immutable for the lifetime of the process.
They are not pipeline-specific — they apply to all pipelines in the domain.

Do not use static configuration classes for pipeline-specific values like file
paths, service URLs, or processing parameters. Those must flow through the Universe.

---

## Verification Checklist

After implementing configuration for a pipeline, verify:

- [ ] Pipeline configuration is injected into the Universe (via constructor params
  or `set_configuration()`) — not read ad-hoc by B-units
- [ ] If using key-value registry: configuration keys enum exists in
  `{pipeline_name}/objects/enums/configuration_keys_enums.py`
- [ ] If using constructor injection: Universe constructor accepts typed
  configuration objects with all required values
- [ ] All configuration values are set in the pipeline runner or application entry point
- [ ] No `os.getenv()` calls in B-units, orchestrators, or services
- [ ] No hardcoded file paths in B-units, orchestrators, or services
- [ ] No `Path(__file__).parents[N]` patterns in pipeline code
- [ ] All paths in the Universe are absolute
- [ ] B-units read configuration only from the Universe (`self.input_object`)
- [ ] Only PDK framework flags (`BClearerConfigurations`, `BClearerDomainConfigurations`)
  are read from static classes — pipeline-specific values always go through the Universe
- [ ] Application-pipeline boundary is clean — pipeline code does not import
  application-layer modules
- [ ] Test fixtures inject configuration via Universe (constructor or
  `set_configuration()`), not via environment variables or monkeypatching
