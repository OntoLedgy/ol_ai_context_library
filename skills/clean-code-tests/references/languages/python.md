# Clean Code Tests — Python

Language-specific testing patterns for Python (pytest).
Read alongside `references/testing-philosophy.md` and `references/testing-standards.md`.

---

## Framework and Tooling

| Tool | Purpose |
|------|---------|
| `pytest` | Test runner and fixture system |
| `unittest.mock` | Mocking — `MagicMock`, `patch`, `call` |
| `pytest-anyio` | Async test runner — `@pytest.mark.anyio` |
| `pytest-cov` | Coverage reporting |
| `testcontainers` | Docker-based external services in integration tests |

---

## File and Class Structure

```python
"""Test module for ComponentName functionality."""
from __future__ import annotations  # always first

from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, call, patch

import pytest

from src.module.component import ComponentName


class TestComponentName:
    """Test suite for ComponentName.

    Covers initialisation, processing, and error handling.
    """

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Set up a fresh ComponentName before each test."""
        self.component = ComponentName()

    def test_process_valid_input_returns_expected_output(self) -> None:
        """Test that valid input is processed correctly."""
        # Arrange
        input_data = {"key": "value"}
        expected = {"processed": True, "key": "value"}

        # Act
        result = self.component.process(input_data)

        # Assert
        assert result == expected
        assert result["processed"] is True

    def test_process_none_input_raises_value_error(self) -> None:
        """Test that None input raises ValueError with descriptive message."""
        with pytest.raises(ValueError, match="Input cannot be None"):
            self.component.process(None)
```

Rules:
- Every test method annotated `-> None`
- `from __future__ import annotations` always first
- One test class per source class
- `autouse=True` fixture for per-test setup

---

## Naming

| Unit | Pattern | Example |
|------|---------|---------|
| Test class | `Test<ComponentName>` | `TestTransactionLoader` |
| Test method | `test_<action>_<condition>_<result>` | `test_load_raises_file_not_found_when_path_missing` |
| Fixture | descriptive noun | `temp_output_folder`, `mock_registry` |

---

## Fixtures

### Scope and cleanup

```python
@pytest.fixture(scope="session")
def data_input_folder() -> Path:
    """Absolute path to the test input data directory."""
    return Path(__file__).parent / "data" / "input"


@pytest.fixture
def temp_output_folder() -> Iterator[Path]:
    """Temporary output folder; removed after each test."""
    import shutil, tempfile
    temp_dir = Path(tempfile.mkdtemp(prefix="test_output_"))
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
```

### Fixture composition

```python
@pytest.fixture
def snapshot_configuration(
    test_input_folder: Path,
    test_output_folder: Path,
) -> SnapshotConfiguration:
    """Fully wired snapshot configuration for tests."""
    return SnapshotConfiguration(
        input_folder=test_input_folder,
        output_folder=test_output_folder,
    )
```

### Shared fixtures

Place shared fixtures in `tests/fixtures/<category>.py` and import with wildcard
in `conftest.py`:

```python
# conftest.py
from tests.fixtures.paths import *
from tests.fixtures.configurations import *
```

---

## Mocking

### `@patch` decorator

```python
@patch("src.module.component.OpenAiClient")
def test_generates_summary_calls_api_once(mock_client: MagicMock) -> None:
    """Test that summary generation calls the API exactly once."""
    mock_client.return_value.generate.return_value = "summary text"

    result = generate_summary("input", client=mock_client.return_value)

    mock_client.return_value.generate.assert_called_once()
    assert result == "summary text"
```

### `monkeypatch` for method injection

```python
def test_pipeline_service_called(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that PipelineService.generate is called with the correct config."""
    called: dict[str, Any] = {}

    def fake_generate(config: dict[str, Any], out: str) -> str:
        called["args"] = (config, out)
        return str(tmp_path / "out")

    monkeypatch.setattr(PipelineService, "generate", staticmethod(fake_generate))

    run_pipeline(config={}, output_path=str(tmp_path))

    assert "args" in called
```

### Verifying mock interactions

```python
mock_registry = MagicMock()
register_items(registry=mock_registry, items=[item_a, item_b])

assert mock_registry.register.call_count == 2
mock_registry.register.assert_any_call(item=item_a)
```

---

## Error Path Testing

```python
def test_load_raises_file_not_found_when_path_missing(self) -> None:
    """Test that missing path raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="No such file"):
        self.loader.load(path=Path("/nonexistent/file.csv"))


def test_connect_raises_auth_error_on_invalid_credentials(self) -> None:
    """Test that invalid credentials raise AuthenticationError."""
    with pytest.raises(AuthenticationError, match="Invalid credentials"):
        self.client.connect(username="bad", password="bad")
```

---

## Parametrised Tests

```python
@pytest.mark.parametrize(
    ("input_value", "expected"),
    [
        ("hello", "HELLO"),
        ("world", "WORLD"),
        ("",      ""     ),
    ],
)
def test_transform_uppercases_input(self, input_value: str, expected: str) -> None:
    """Test that transform uppercases any string input."""
    assert self.component.transform(input_value) == expected


@pytest.mark.parametrize(
    ("bad_path", "expected_error"),
    [
        ("../etc/passwd", "path traversal"),
        ("/absolute/path", "absolute path"),
    ],
)
def test_load_rejects_unsafe_paths(self, bad_path: str, expected_error: str) -> None:
    """Test that unsafe paths are rejected with descriptive errors."""
    with pytest.raises(ValueError, match=expected_error):
        self.loader.load(path=bad_path)
```

---

## Async Tests

```python
import pytest


@pytest.mark.anyio
async def test_async_fetch_returns_result(self) -> None:
    """Test that async fetch returns a non-empty result."""
    result = await self.service.fetch("resource_id")
    assert result is not None


@pytest.mark.anyio
async def test_async_concurrent_operations_complete(self) -> None:
    """Test that concurrent operations all complete without error."""
    results = await self.service.fetch_all(["id_1", "id_2", "id_3"])
    assert len(results) == 3
```

---

## Markers and Categories

```python
# Lightweight unit test — no marker needed, runs in CI by default
def test_calculate_total_sums_all_amounts(self) -> None: ...


# Heavy test requiring external service
@pytest.mark.heavy
class TestNeo4jGraphExtraction:
    """Integration tests requiring a running Neo4j instance."""

    @pytest.mark.skipif(
        not os.environ.get("NEO4J_URI"),
        reason="NEO4J_URI environment variable not set",
    )
    def test_extract_graph_returns_populated_universe(self, neo4j_facade) -> None: ...


# Integration test
@pytest.mark.integration
@pytest.mark.heavy
class TestCsvPipelineIntegration:
    """End-to-end pipeline test using real file I/O."""
    ...
```

### pyproject.toml configuration

```toml
[tool.pytest.ini_options]
addopts = "--import-mode=importlib -m 'not heavy'"
markers = [
    "heavy: requires external services (deselect with -m 'not heavy')",
    "integration: component interaction tests",
]
```

### PYTHONPATH requirement

When using a `tests/fixtures/` directory with wildcard imports, the tests folder
must be on the path:

```bash
# Set before running tests
export PYTHONPATH="${PYTHONPATH}:$(pwd)/tests"

# Or inline
PYTHONPATH=tests pytest tests/unit_tests
```

---

## Test Output Conventions (bclearer / Python repos)

Tests that produce data for inspection or capture logging output MUST write to
structured, timestamped folders under `tests/data/`. This keeps outputs isolated
per run, traceable by test name, and out of source control (add to `.gitignore`).

### Folder layout

```
tests/data/
├── output/
│   └── <sanitized_test_name>/
│       └── <YYYY_MM_DD_HH_MM_SS>/   ← data files for inspection (JSON, CSV, etc.)
└── logs/
    └── <sanitized_test_name>/
        └── <YYYY_MM_DD_HH_MM_SS>/
            └── log_file<YYYY_MM_DD_HH_MM_SS>.txt   ← logging decorator output
```

Log output (from the bclearer orchestration logging decorator) goes to `logs/`.
Data output for inspection (JSON, CSV, graphs, etc.) goes to `output/`.
These are always separate — never mix logs and data in the same folder.

### Timestamp format

Use `now_time_as_string_for_files()` from bclearer orchestration:

```python
from bclearer_orchestration_services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)
# Returns: "YYYY_MM_DD_HH_MM_SS"
```

If the bclearer orchestration service is not available, fall back to:

```python
from datetime import datetime
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
```

### Test name sanitisation

Replace all non-alphanumeric characters (except `.`, `_`, `-`) with underscores.
This makes the folder name safe for all operating systems:

```python
import re

def _sanitize_test_name(test_name: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", test_name).strip("_")
    return sanitized or "run"
```

### Standard fixtures

Define these in `tests/fixtures/` and import in `conftest.py`. The `run_stamp`
and `test_run_name` fixtures feed into both `run_output_folder` and `run_log_folder`
so both folders always share the same timestamp.

```python
import re
import pytest
from pathlib import Path
from bclearer_orchestration_services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)
from bclearer_orchestration_services.reporting_service.reporters.log_file import LogFiles

_OUTPUT_ROOT = Path(__file__).resolve().parents[1] / "data" / "output"
_LOG_ROOT    = Path(__file__).resolve().parents[1] / "data" / "logs"


def _sanitize_test_name(test_name: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", test_name).strip("_")
    return sanitized or "run"


@pytest.fixture(scope="function")
def run_stamp() -> str:
    """Timestamp for the current test run: YYYY_MM_DD_HH_MM_SS."""
    return now_time_as_string_for_files()


@pytest.fixture(scope="function")
def test_run_name(request: pytest.FixtureRequest) -> str:
    """Sanitized test name, safe for use as a directory name."""
    return _sanitize_test_name(request.node.name)


@pytest.fixture(scope="function")
def run_output_folder(
    test_run_name: str,
    run_stamp: str,
) -> Path:
    """Create and return tests/data/output/<test_name>/<timestamp>/."""
    folder = _OUTPUT_ROOT / test_run_name / run_stamp
    folder.mkdir(parents=True, exist_ok=True)
    return folder


@pytest.fixture(scope="function")
def run_log_folder(
    test_run_name: str,
    run_stamp: str,
) -> Iterator[Path]:
    """Create tests/data/logs/<test_name>/<timestamp>/ and open the log file."""
    folder = _LOG_ROOT / test_run_name / run_stamp
    folder.mkdir(parents=True, exist_ok=True)
    LogFiles.open_log_file(folder_path=str(folder), now_time=run_stamp)
    try:
        yield folder
    finally:
        LogFiles.close_log_file()
```

### Using the fixtures in tests

Apply `run_log_folder` at module level so every test in the file gets logging:

```python
import pytest
from pathlib import Path

pytestmark = pytest.mark.usefixtures("run_log_folder")


class TestFileSystemSnapshotWorkflow:
    """Integration tests for the file system snapshot service."""

    def test_run_basic_snapshot(
        self,
        run_output_folder: Path,
        snapshot_configuration: FileSystemSnapshotConfigurations,
    ) -> None:
        """Test that a basic snapshot produces a populated universe."""
        # Act
        universe = FileSystemSnapshotServiceFacade.run_file_system_snapshot(
            configurations=snapshot_configuration,
        )

        # Assert
        assert universe is not None

        # Write data output for inspection (separate from logs)
        (run_output_folder / "universe_summary.json").write_text(
            json.dumps(universe.to_summary_dict(), indent=2),
        )
```

### Parallel execution (pytest-xdist)

When running with `-n auto`, isolate output by worker to avoid folder collisions:

```python
import os

worker_id = os.environ.get("PYTEST_XDIST_WORKER")
if worker_id:
    folder = _OUTPUT_ROOT / worker_id / test_run_name / run_stamp
```

### .gitignore entries

Add these to `.gitignore` — test outputs are never committed:

```
tests/data/output/
tests/data/logs/
```

---

## bclearer / BIE / BORO Patterns

### Identity vector tests

```python
def test_empty_vector_produces_zero_bie_id(self) -> None:
    """Test that an empty identity vector yields a zero-dimensional BIE ID."""
    vector = CommonIdentityVector()

    bie_id = BieIdCreationFacade.create_bie_id_from_identity_vector(
        identity_vector=vector,
    )

    assert bie_id.bie_vector_structure_type == BieVectorStructureTypes.ZERO_DIMENSIONAL


def test_populated_vector_produces_multi_dimensional_bie_id(self) -> None:
    """Test that a populated vector produces a multi-dimensional BIE ID."""
    vector = FileSystemObjectIdentityVector(
        absolute_path=Path("/home/user/file.txt"),
    )

    bie_id = BieIdCreationFacade.create_bie_id_from_identity_vector(
        identity_vector=vector,
    )

    assert bie_id.bie_vector_structure_type == BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_SENSITIVE
```

### Registry mock pattern (BORO)

```python
def test_register_enum_calls_registry_once(self) -> None:
    """Test that enum registration invokes the registry exactly once."""
    mock_registry = MagicMock()

    register_bie_enums_to_registry_base(
        bie_enum_leaf_type=BieEnums,
        bie_registry=mock_registry,
    )

    mock_registry.register_bie_id_if_required.assert_called_once()
    call_kwargs = mock_registry.register_bie_id_if_required.call_args
    assert call_kwargs.kwargs["bie_item_id"] == BieEnums.enum_bie_identity
```

### Internal test helper classes

Use an underscore prefix for test-internal subclasses:

```python
class _TestRegistry(BieIdRegistries):
    """Registry subclass used only within this test module."""
    ...
```

### Fixture file in bclearer layout

```python
# tests/fixtures/file_system_snapshot_service/configurations.py

@pytest.fixture
def snapshot_configuration(
    test_input_folder: Path,
    test_output_folder: Path,
) -> FileSystemSnapshotConfigurations:
    """Fully configured snapshot configuration for FSS tests."""
    return FileSystemSnapshotConfigurations(
        input_folder=Folders(absolute_path=test_input_folder),
        output_folder=Folders(absolute_path=test_output_folder),
    )
```
