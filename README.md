# OntoLedgy AI Context Library

Curated library of AI context artefacts for the OL AI Services platform — including prompts, skills, agent configurations, and workflow instructions. Designed as a code-free, installable collection for use across OntoLedgy's LLM-orchestrated chemical engineering workflows.

## Repository Contents

### Skills

Installable Claude Code skills for BIE (BORO Identity Ecosystem) development workflows.

| Skill | Description |
|-------|-------------|
| `bie-data-engineer` | Implements a BIE domain in Python from an approved ontology model. Creates domain enums, bie_id creator functions, BieDomainObjects subclasses, registration helpers, and domain universe setup. |
| `bie-domain-ontologist` | Designs and reviews BIE domain ontology models. Operates in Design Mode (new domain) or Review Mode (validate/extract from existing code). Produces the 4 ontology deliverables required before implementation. |

### Prompts

Reusable prompt libraries organised by domain.

#### Coding

- **Agents** — Specialised agent prompts for spec-driven and bug-fix workflows:
  - `spec-task-executor`, `spec-task-validator`, `spec-test-generator`, `spec-completion-reviewer`
  - `spec-design-validator`, `spec-requirements-validator`, `spec-dependency-analyzer`
  - `spec-breaking-change-detector`, `spec-duplication-detector`, `spec-performance-analyzer`
  - `spec-integration-tester`, `spec-documentation-generator`, `spec-task-implementation-reviewer`
  - `bug-root-cause-analyzer`, `steering-document-updater`

- **Commands** — Slash-command definitions for structured workflows:
  - Spec workflow: `spec-create`, `spec-execute`, `spec-list`, `spec-status`, `spec-steering-setup`
  - Bug workflow: `bug-create`, `bug-analyze`, `bug-fix`, `bug-status`, `bug-verify`

- **Standards** — Coding standards and guidelines:
  - `BCLEARER_FRAMEWORK` — bCLEARer pipeline architecture framework
  - `clean_coding/` — Clean code standards (naming, functions, classes, formatting, error handling, concurrency, etc.)
  - `cicd/` — CI/CD standards (commit conventions)
  - `testing/` — Testing guidelines and quality requirements

- **Templates** — Markdown templates for spec and bug workflow artefacts:
  - `design-template`, `product-template`, `requirements-template`, `structure-template`, `tasks-template`, `tech-template`
  - `bug-report-template`, `bug-analysis-template`, `bug-verification-template`

#### Data Modeling

Python prompt modules for BIE data model generation — initial and iterative modelling with formatting utilities.

#### Discovery

Python prompt modules for domain discovery workflows.

#### Form Extraction

Python prompt modules for extracting structured data from forms.

#### Graph RAG

Python prompt modules for graph-based retrieval-augmented generation.

#### Text Extraction

Python prompt modules for text extraction from documents.

## Installing Skills

Skills can be installed using [`npx skills`](https://github.com/vercel-labs/skills), the open agent skills CLI that supports Claude Code, OpenCode, Codex, Cursor, and more.

### List available skills

```bash
npx skills add OntoLedgy/ol_ai_context_library --list
```

### Install all skills

```bash
npx skills add OntoLedgy/ol_ai_context_library
```

### Install a specific skill

```bash
# Install the BIE data engineer skill
npx skills add OntoLedgy/ol_ai_context_library --skill bie-data-engineer

# Install the BIE domain ontologist skill
npx skills add OntoLedgy/ol_ai_context_library --skill bie-domain-ontologist
```

### Install to a specific agent

```bash
npx skills add OntoLedgy/ol_ai_context_library -a claude-code
```

### Install globally (available across all projects)

```bash
npx skills add OntoLedgy/ol_ai_context_library -g
```

### Managing installed skills

```bash
# List installed skills
npx skills list

# Check for updates
npx skills check

# Update to latest
npx skills update

# Remove a skill
npx skills remove bie-data-engineer
```

Once installed, skills are available in your coding agent sessions and can be triggered by describing a relevant task (e.g. "implement a BIE domain from this ontology model" or "design a BIE domain for spreadsheets").

## Project Structure

```
ol_ai_context_library/
├── skills/
│   ├── bie-data-engineer/
│   │   ├── SKILL.md
│   │   └── references/
│   └── bie-domain-ontologist/
│       ├── SKILL.md
│       └── references/
└── prompts/
    ├── coding/
    │   ├── agents/
    │   ├── commands/
    │   ├── standards/
    │   └── templates/
    ├── data_modeling/
    ├── discovery/
    ├── form_extraction/
    ├── graph_rag/
    ├── research/
    └── text_extraction/
```
