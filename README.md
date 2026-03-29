# OntoLedgy AI Context Library

Curated library of AI context artefacts for the OL AI Services platform — including prompts, skills, agent configurations, and workflow instructions. Designed as a code-free, installable collection for use across OntoLedgy's LLM-orchestrated engineering, ontology, and delivery workflows.

## Repository Contents

### Skills

Installable agent skills for ontological analysis, architecture, implementation, and clean-code workflows.

| Skill Family | Examples | Purpose |
|-------------|----------|---------|
| Ontologists | `ontologist`, `ob-ontologist`, `bie-component-ontologist` | Analyse a domain, build ontology models, and validate ontological coherence before design or implementation |
| Architects | `software-architect`, `ob-architect`, `bclearer-pipeline-architect` | Design solution architecture, ontology-aware systems, and bclearer pipelines |
| Engineers | `data-engineer`, `python-data-engineer`, `javascript-data-engineer`, `csharp-data-engineer`, `rust-data-engineer`, `ob-engineer`, `bclearer-pipeline-engineer`, `bie-data-engineer` | Implement approved designs in the target language or platform |
| Clean Code | `clean-code-reviewer`, `clean-code-refactor`, `clean-code-naming`, `clean-code-tests`, `clean-code-commit` | Review, refactor, test, and commit changes using shared quality standards |

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

### Authentication (required for private repositories)

If this repository is private, `npx skills add` will fail with an authentication error. You must provide a GitHub token before running any skills command.

**Option 1 — Use the GitHub CLI token (recommended):**

```bash
# Log in once with the GitHub CLI
gh auth login

# Then prefix all skills commands with the token
GITHUB_TOKEN=$(gh auth token) npx skills add OntoLedgy/ol_ai_context_library -g
```

**Option 2 — Use a personal access token (PAT):**

```bash
# Create a PAT at https://github.com/settings/tokens (needs `repo` scope)
GITHUB_TOKEN=<your-token> npx skills add OntoLedgy/ol_ai_context_library -g
```

**Option 3 — Export once in your shell profile (recommended for daily use):**

Add the following to `~/.bashrc` or `~/.zshrc` so the token is always available:

```bash
export GITHUB_TOKEN=$(gh auth token)
```

Then reload your shell (`source ~/.bashrc`) and run skills commands without the prefix:

```bash
npx skills add OntoLedgy/ol_ai_context_library -g
```

> **Note:** The WSL2 browser-based `gh auth login` flow may fail to open a browser automatically. If it hangs, copy the one-time code shown in the terminal, open `https://github.com/login/device` manually in your browser, and enter the code there.

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
# Install the base ontologist skill
npx skills add OntoLedgy/ol_ai_context_library --skill ontologist

# Install the OB ontologist skill
npx skills add OntoLedgy/ol_ai_context_library --skill ob-ontologist

# Install the BIE data engineer skill
npx skills add OntoLedgy/ol_ai_context_library --skill bie-data-engineer

# Install the BIE component ontologist skill
npx skills add OntoLedgy/ol_ai_context_library --skill bie-component-ontologist
```

### Install to a specific agent

```bash
npx skills add OntoLedgy/ol_ai_context_library -a claude-code
```

### Install globally (available across all projects)

```bash
npx skills add OntoLedgy/ol_ai_context_library -g
```

### Updating skills

The skills CLI checks folder content hashes via the GitHub API to detect changes. For private repositories, unauthenticated requests cannot see the latest state, so `npx skills update` will report no changes even when the skill has been updated.

To update correctly, prepend a GitHub token:

```bash
# Using a personal access token
GITHUB_TOKEN=<your-token> npx skills update

# Or using the GitHub CLI token
GITHUB_TOKEN=$(gh auth token) npx skills update
```

You can also re-install a specific skill to force the update:

```bash
GITHUB_TOKEN=$(gh auth token) npx skills add OntoLedgy/ol_ai_context_library --skill bie-data-engineer
```

> **Tip:** Export `GITHUB_TOKEN` in your shell profile (e.g. `export GITHUB_TOKEN=$(gh auth token)` in `~/.zshrc`) so all skills commands authenticate automatically.

### Managing installed skills

```bash
# List installed skills
npx skills list

# Check for updates
GITHUB_TOKEN=$(gh auth token) npx skills check

# Remove a skill
npx skills remove bie-data-engineer
```

Once installed, skills are available in your coding agent sessions and can be triggered by describing a relevant task (e.g. "implement a BIE domain from this ontology model" or "design a BIE component for spreadsheets").

## Project Structure

```
ol_ai_context_library/
├── skills/
│   ├── ontologist/
│   ├── ob-ontologist/
│   ├── software-architect/
│   ├── ob-architect/
│   ├── data-engineer/
│   ├── python-data-engineer/
│   ├── rust-data-engineer/
│   ├── clean-code-reviewer/
│   ├── clean-code-refactor/
│   ├── bie-component-ontologist/
│   └── bie-data-engineer/
├── skills-lock.json
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
