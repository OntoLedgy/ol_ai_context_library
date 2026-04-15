# JIRA Implementation Log Template

Posted as a comment on the JIRA subtask by `jira-impl-logger`. This is the canonical record of what was implemented — not the git log, not the repo.

## Header Block

```markdown
## Implementation Log — {TICKET-KEY}

**Summary:** {one-line summary of what was implemented}
**Commit:** `{sha}` — {commit message first line}
**Date:** {ISO 8601 date}
**Implemented via:** skill `{engineer-skill-name}` (delegated by `sprint-executor`)
```

## Files Block

```markdown
### Files

**Created ({N}):**
- `{path1}`
- `{path2}`

**Modified ({M}):**
- `{path3}`
- `{path4}`

**Stats:** +{linesAdded} / -{linesRemoved} across {N+M} files
```

## Artifacts Block

Include only the artifact types produced. Empty sections are omitted.

### API Endpoints

```markdown
### API Endpoints

| Method | Path | Purpose | Location |
|--------|------|---------|----------|
| GET | `/api/licences/:id` | Fetch licence details | `backend/app/routers/licences.py:42` |
| POST | `/api/licences` | Create licence record | `backend/app/routers/licences.py:68` |

**Request/response formats:**
- `GET /api/licences/:id` — query params: none; response: `LicenceSchema` (see `backend/app/schemas/licences.py`)
- `POST /api/licences` — body: `LicenceCreateSchema`; response: `LicenceSchema`
```

### Components

```markdown
### Components

| Name | Type | Purpose | Location | Exports |
|------|------|---------|----------|---------|
| DocumentViewer | React | Display PDF/image documents with annotations | `frontend/src/components/DocumentViewer.tsx` | DocumentViewer (default) |

**Props:**
- `DocumentViewer`: `{ documentUrl: string, annotations?: Annotation[], onAnnotate?: (a: Annotation) => void }`
```

### Functions

```markdown
### Functions

| Name | Purpose | Location | Signature | Exported |
|------|---------|----------|-----------|----------|
| extractLicenceFields | Parse licence PDF into 11-field dict | `trade_analysis_services/common/clients/form_extraction_client/licence_extractor.py:15` | `(pdf_bytes: bytes) -> LicenceFields` | yes |
```

### Classes

```markdown
### Classes

| Name | Purpose | Location | Methods | Exported |
|------|---------|----------|---------|----------|
| LicenceExtractor | Orchestrates form extraction for licences | `trade_analysis_services/common/clients/form_extraction_client/licence_extractor.py` | `extract`, `validate`, `normalise` | yes |
```

### Integrations

```markdown
### Integrations

| Description | Frontend | Backend | Data flow |
|-------------|----------|---------|-----------|
| DocumentViewer loads a stored document from the backend | `DocumentViewer` | `GET /api/documents/:id` | mount → fetch metadata → fetch binary → render with react-pdf |
```

### Data Models

```markdown
### Data Models

| Name | Kind | Location | Migrations |
|------|------|----------|------------|
| LegalEntities (licence fields) | SQLAlchemy model | `trade_analysis_services/common/models/legal_entities.py:88` | `backend/alembic/versions/b2a1_add_licence_columns.py` |

**Fields added:** `licence_number`, `licence_type`, `licence_issued_at`, ... (11 fields total)
```

### Pipeline Stages

```markdown
### Pipeline Stages

| Name | Position | Purpose | Inputs | Outputs | Location |
|------|----------|---------|--------|---------|----------|
| licence_extraction | 7 | Extract licence data from uploaded docs | `legal_entity_id` | `licence_fields` | `trade_analysis_services/entities/onboarding/operations/licence_extraction_stage.py` |
```

## Searchable Keywords

```markdown
### Searchable Keywords

`LicenceExtractor`, `licence_extraction`, `extractLicenceFields`, `GET /api/licences`, `LegalEntities.licence_*`, `b2a1_add_licence_columns`
```

List every class name, exported function name, API route, table column group, migration ID, and component name so future AI agents can grep JIRA to find this log.

## Back-Link Block

```markdown
### Back-Links

- Spec: {Confluence URL}
- tasks.md: `documentation/specs/{feature-name}/tasks.md#{anchor}`
- Commit: {git commit URL or `git show {sha}` locally}
- Related tickets: {list of JIRA keys touched by dependent work}
```

## Full Example (composed)

A complete rendered comment might look like:

```markdown
## Implementation Log — TI-101

**Summary:** Added 11 licence columns to `LegalEntities` SQLAlchemy model with Alembic migration
**Commit:** `a3f1b29` — feat(licence): add licence columns to LegalEntities model
**Date:** 2026-04-15
**Implemented via:** skill `python-data-engineer` (delegated by `sprint-executor`)

### Files
**Created (1):**
- `backend/alembic/versions/b2a1_add_licence_columns.py`

**Modified (1):**
- `trade_analysis_services/common/models/legal_entities.py`

**Stats:** +112 / -2 across 2 files

### Data Models
| Name | Kind | Location | Migrations |
|------|------|----------|------------|
| LegalEntities | SQLAlchemy model | legal_entities.py:88 | b2a1_add_licence_columns.py |

**Fields added:** licence_number, licence_type, licence_issued_at, licence_expires_at, licence_issuing_authority, licence_jurisdiction, licence_status, licence_document_id, licence_extracted_at, licence_confidence, licence_raw_payload

### Searchable Keywords
`LegalEntities.licence_*`, `b2a1_add_licence_columns`

### Back-Links
- Spec: https://ontoledgy.atlassian.net/wiki/spaces/TBMLI/pages/6521323524
- tasks.md: `documentation/specs/licence-data-extraction/tasks.md` task 1
- Commit: git show a3f1b29
```

## Quality Rules

- **Never** post empty artifacts for non-refactor tasks
- **Do** repeat class/function names verbatim in "Searchable Keywords" even if they appear above — search depends on this
- **Don't** paraphrase code — quote signatures exactly
- **Do** use absolute file paths from repo root (no `./` prefix)
- **Don't** include secret values or tokens even if they appear in config files
