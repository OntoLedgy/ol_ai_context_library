# bclearer Code Style

> This reference mirrors `bie-data-engineer/references/code-style.md` and extends it
> with any pipeline-specific additions. Where this file specifies a rule, it takes
> precedence over the general clean coding standards from `data-engineer/references/clean-coding-index.md`.

---

## Source of Truth

The canonical bclearer code style is defined in:

```
skills/bie-data-engineer/references/code-style.md
```

Read that file for the full style guide. Key rules summarised below for quick reference.

---

## Quick Reference

### Line Continuations — use backslash

```python
result = \
    some_function()
return \
    result
```

### Named Keyword Arguments — always use after first positional

```python
BieIdCreationFacade.create_bie_id_for_single_object(
    input_object=input_object,
    bie_domain_type=bie_domain_type)
```

### Verbose Naming — no abbreviations

```python
# Correct
transactions_dataframe
account_bie_id
excel_workbook_ingest_adapter

# Avoid
df
acct_id
adapter
```

### Class Inheritance — parent on indented line

```python
class SomePipelineOrchestrators(
        BasePipelineOrchestrators):
```

### Function Signatures — parameters each on own line

```python
def create_pipeline_universe(
        source_path: str,
        target_path: str) \
        -> PipelineUniverse:
```

### Imports — full paths, backslash continuation for long imports

```python
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import \
    BieIds
```

---

## Pipeline-Specific Naming Additions

> To be confirmed as conventions solidify.

| Artefact | Convention | Example |
|----------|-----------|---------|
| Ingest adapter class | `[Source]IngestAdapters` | `ExcelWorkbookIngestAdapters` |
| Export adapter class | `[Target]ExportAdapters` | `PostgresExportAdapters` |
| Stage service class | `[Concern]Services` | `TransactionEnrichmentServices` |
| Stage orchestrator class | `[StageName]Orchestrators` | `IdentifyOrchestrators` |
| Runner class | `[PipelineName]Runners` | `AccountsPipelineRunners` |
| Universe class | `[PipelineName]Universes` | `AccountsPipelineUniverses` |
