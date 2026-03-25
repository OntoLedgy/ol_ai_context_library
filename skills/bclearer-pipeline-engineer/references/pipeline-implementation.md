# Pipeline Implementation Reference

> **Status: Skeleton** — populate with bclearer-confirmed implementation patterns as pipelines are built. Reference the File System Snapshot service as the canonical example.

---

## Canonical Reference

The canonical bclearer pipeline implementation is:

```
bclearer_orchestration_services.file_system_snapshot_service.universe
```

Read this before implementing any new pipeline. It demonstrates:
- Universe setup and wiring
- BIE factory construction order
- Stage separation (ingest → identify → export)

---

## File Naming Conventions

Follow bclearer `code-style.md` conventions (see `references/bclearer-code-style.md`):

| Artefact | Naming Pattern | Example |
|----------|---------------|---------|
| Stage adapter (ingest) | `[source]_ingest_adapter.py` | `excel_workbook_ingest_adapter.py` |
| Stage adapter (export) | `[target]_export_adapter.py` | `postgres_export_adapter.py` |
| Stage service | `[concern]_service.py` | `transaction_enrichment_service.py` |
| Stage orchestrator | `[stage_name]_orchestrator.py` | `identify_orchestrator.py` |
| Pipeline runner | `[pipeline_name]_runner.py` | `accounts_pipeline_runner.py` |
| Universe | `[pipeline_name]_universe.py` | `accounts_pipeline_universe.py` |

---

## Stage Adapter Template

> To be confirmed from codebase. Placeholder structure:

```python
# [source]_ingest_adapter.py
class SourceNameIngestAdapters:

    def __init__(
            self,
            source_path: str) \
            -> None:
        self._source_path = \
            source_path

    def read(self) \
            -> [ReturnType]:
        # call interop service here
        ...
```

---

## Stage Service Template

> To be confirmed from codebase. Placeholder structure:

```python
# [concern]_service.py
def process_[entities](
        input_objects: List[InputType],
        universe: PipelineUniverse) \
        -> List[OutputType]:
    ...
```

---

## Universe Template

> To be confirmed from codebase. Placeholder structure:

```python
# [pipeline_name]_universe.py
class PipelineNameUniverse:

    def __init__(self) -> None:
        self.bie_id_registerer = \
            BieIdRegisterer()
        # domain object registries...
```

---

## Patterns to Document (TODO)

- [ ] Confirmed stage adapter class structure
- [ ] Confirmed stage service function vs. class choice
- [ ] Confirmed universe class structure for new pipeline types
- [ ] Runner class structure (`b_app_runner_service` integration)
- [ ] How to wire configuration into the runner
- [ ] Standard test fixture pattern for pipeline stages
- [ ] Integration test pattern for a full pipeline run
