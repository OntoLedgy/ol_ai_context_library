# Reference Spaces — Annotated Tour

Three real Ontoledgy spaces that informed the canonical structure. Each is
mapped to the canonical sections so you can see the convention in action
(and where it bends).

Cloud ID for all: `c62e56c2-b224-4d4e-a859-afa7de01241e`.

---

## ACE — `SAKE` (Solution - Agentic Chemical Engineering)

**Most mature** space. Spans multiple repos (knowledge extraction service,
file system snapshot service, identification services, document control
identity service, BIE infrastructure, bclearer PDK). Originally a
research-bid space (Innovate UK / DSIT / HVMC application), evolved into a
multi-component product space.

- **URL:** https://ontoledgy.atlassian.net/wiki/spaces/ACE/overview
- **Space key:** `ACE` (CQL queries) — backing space ID is `SAKE` due to
  rename history. `getConfluenceSpaces({keys: ["ACE"]})` may return empty;
  use CQL `space = ACE` instead.
- **Homepage ID:** `6487081701`'s analogue — actual homepage ID:
  `6380716198` (parent of `Background`, `Proposal`, `WIP - Tasks`,
  `Current Assets/Infrastructure`, `Scope - Requirement`,
  `System Architecture and Agent Roles`, `WIP`, `References`, `Plans`).
- **Homepage style:** legacy — does **not** use the project-linker macro.
  Audit Row A would flag this as `medium` (no JIRA project bound).
- **Notable scope flag:** `research-bid`.

### Mapping to canonical structure

| ACE Page (current) | Canonical Section | Audit Severity |
|--------------------|-------------------|----------------|
| `Background` (with `Overview`, `Key Dates`, `Agentic Engineering Design Review Process`) | `01 Overview` | low (rename) + medium (`Key Dates` should move under `03 Releases` or `99 WIP`) |
| `Proposal` (with `Public Description`, `Scope`, `Question 09–15`, `Question 10 — Technical Approach`) | `Proposal` (conditional) | accepted (research-bid) |
| `WIP - Tasks` (with `Component Table`, `Proposal Prep Tasks`) | `99 WIP` (subsection) | low (rename) |
| `Current Assets/Infrastructure` (with `Code`, `Knowledge/Competencies`, `BIE Infrastructure`, `Ontologies`, `bCLEARer PDK and Architecture Framework`) | mixed: `04 Architecture` + `08 Ontology` | high (split — `Ontologies` belongs under `08 Ontology`; rest under `04 Architecture`) |
| `Scope - Requirement` (with `Advanced Manufacturing`, `Health and Life Sciences`, `Creative Industries`, `Categories of R&D`) | extra (research-bid) | info — funder-specific |
| `System Architecture and Agent Roles` (with `Solution Architecture`, `Architecture Principles`, `Semantic Architecture`, `Tools/Compute/Environments`, `Performance Metrics and Validation`, `Transparency`, `APIs/Interfaces/Deployment Model`, `Verification and Validation Results`) | `04 Architecture` | low (rename) — content already canonical-ish |
| `WIP` (with `Chris Dump`, `Diagram drafts`, `Logos`, `Skill Work`) | `99 WIP` | low (rename) |
| `References` (with `Agent Engineering`, `Skills`, `Coding Agents`, `Agent Memory`, `Chemical Engineering`, `Chemical Engineering Design`, `IPFS/IPNS/DHT`, `Interoperability Costs`, `bCLEARer`, `Beyond Alignment`, `Innovate UK`, `DSIT`, `HVMC`, `Construction Engineering`) | `09 References` | low (rename) — exemplary content |
| `Plans` (with `MVP Plan`) | `03 Releases` | low (rename) |
| (missing) | `02 Steering` | medium — not yet adopted |
| (missing) | `05 Specs` | medium — specs ad-hoc, not in `.claude/specs/` form |
| (missing) | `06 Sprints` | medium |
| (missing) | `07 Reviews` (top-level) | high — reviews currently scattered (see Code Reviews / per-component reviews under `Current Assets/Infrastructure` and elsewhere) |

### What ACE teaches

- **References as a first-class section is right.** ACE's `References`
  subtree (Agent Engineering / Skills / Coding Agents / Chemical
  Engineering / external bodies) is a strong pattern.
- **Date-stamped review pages with hostname suffix are real.** Examples:
  `File System Snapshot Service - Review - 2026-03-24-2216 MAUDLIN`,
  `Document Control Identity Service - Review - 2026-03-11-0813 roy.corp.ontoledgy.io`.
- **Per-component depth is real.** `Current Assets/Infrastructure /
  bCLEARer PDK and Architecture Framework` is a deep sub-tree that maps
  cleanly to the per-component design pattern under `04 Architecture`.
- **Research-bid scope needs its own conditional section.** The `Proposal`
  + `Scope - Requirement` pages are essential to ACE but pollute the
  canonical structure if forced into it. Hence the `Proposal` conditional.
- **Numeric prefixes were never adopted.** Migration to `01..99` will be
  the largest cosmetic change.

---

## TBMLI (Trade Based Money Laundering Investigator)

**Mid-mature**, JIRA-integrated, sprint-driven product space. Single
solution, multiple services (Knowledge Extraction Services, Entity
Verification Services, Sanctions Screening, Address Verification Services,
Agent Harness). Created using the modern Confluence project-space
template.

- **URL:** https://ontoledgy.atlassian.net/wiki/spaces/TBMLI/overview
- **Space ID:** `6487080964`
- **Homepage ID:** `6487081701` — uses the modern template:
  - Description placeholder
  - **Project Tracker** macro (`com.atlassian.confluence.project-linker`)
  - Recently Updated macro
  - Contributors macro
- **JIRA project key:** `TBMLI`.

### Mapping to canonical structure

| TBMLI Page (current) | Canonical Section | Audit Severity |
|----------------------|-------------------|----------------|
| `Architecture` (with `Knowledge Extraction Services`, `Entity Verification Services`, `Sacations Screening` (sic), `Address Verification Services`, `Agent Harness`) | `04 Architecture` | low (rename — also fix typo `Sacations` → `Sanctions`) |
| `Code Reviews` (with `Pipelines`, `Frontend`, `General`) | `07 Reviews / Code Reviews` | high — should be nested under `07 Reviews` (currently top-level) |
| `Ontology` (with `Ontology - Addressess` (sic), `Ontology - Legal Entities`, `Ontology - Commodities`, `Ontology - Trades`) | `08 Ontology` | low (rename + fix typo) |
| `Planning` (with `Entity Journey — Implementation Plan`, `Sprint Planning — TBML Investigator Demo`) | split — `06 Sprints` + `04 Architecture` | medium — split: sprint pages under `06 Sprints`, implementation plans under each component in `04 Architecture` |
| (missing) | `01 Overview` | critical — homepage is template only |
| (missing) | `02 Steering` | medium |
| (missing) | `03 Releases` | medium |
| (missing) | `05 Specs` | medium |
| (missing) | `09 References` | medium |

### What TBMLI teaches

- **The modern Confluence space template is the baseline.** Project
  Tracker + Recently Updated + Contributors on the homepage. We adopt
  these in the canonical Homepage Template.
- **JIRA integration is first-class via project-linker.** New spaces must
  have this macro on the homepage; older spaces (ACE) lack it and the
  audit should flag it as `critical` once a JIRA project is attached.
- **Per-component sub-trees with `Design v{N}` and `Architecture Review`
  pages work well.** Examples:
  - `Architecture / Address Verification Services / Address Verification Services — Architecture Design v1 / Implementation Path — Address Verification Services`
  - `Architecture / Agent Harness / Agent Harness - Design v2 / Agent Harness - Architecture Review (agent-architect)`
- **`Pipelines` and `Frontend` are valid grouping subsections under
  `07 Reviews`.** The audit checklist accepts these as code-review
  sub-areas, alongside `General`.

---

## SAA (Solution - Agentic Accountant)

**Newest** space, sparse, more architecturally-organised. Demonstrates a
cleaner per-tier layout (Backend / Pipeline / UI under Solution
Architecture).

- **URL:** https://ontoledgy.atlassian.net/wiki/spaces/SAA/overview
- **Space ID:** `6508380165`
- **Homepage ID:** `6508381002` — same modern template as TBMLI
  (Description, Project Tracker, Recently Updated, Contributors).

### Mapping to canonical structure

| SAA Page (current) | Canonical Section | Audit Severity |
|--------------------|-------------------|----------------|
| `Template - Project plan`, `Template - Decision documentation`, `Template - Meeting notes` | `Templates` (conditional) | accepted (Confluence-auto) |
| `Architecture / Code Reviews` | `07 Reviews / Code Reviews` | high — top-level, not nested under `04` |
| `Architecture / Solution / Domain Ontology (BORO)` | `08 Ontology` | high — should be top-level |
| `Architecture / Solution / Solution Architecture / Backend / Data Models` | `04 Architecture / Components / Backend / Data Models` | medium — too deeply nested; could collapse one level |
| `Architecture / Solution / Solution Architecture / Backend / Services` | `04 Architecture / Components / Backend / Services` | medium |
| `Architecture / Solution / Solution Architecture / Pipeline` | `04 Architecture / Components / Pipeline` | medium |
| `Architecture / Solution / Solution Architecture / UI` | `04 Architecture / Components / UI` | medium |
| (missing) | `01 Overview, 02 Steering, 03 Releases, 05 Specs, 06 Sprints, 09 References` | medium each |

### What SAA teaches

- **Tier-based layout (Backend / Pipeline / UI) is a valid component
  grouping.** Adopted under `04 Architecture / Components`.
- **Confluence's auto-templates are tolerable as a conditional
  `Templates` section** — they don't need to be moved or renamed.
- **Greenfield spaces start almost empty.** The Create mode of this
  skill should be designed so an empty space gets the full canonical
  scaffold in one pass.

---

## Convergence Analysis

What's consistent across all three spaces:

- Architecture is always a top-level section (in some form).
- Per-component depth (Service → Design vN) is universal.
- Reviews are date-stamped, append-only.
- Domain ontology is a first-class concept (separate from architecture).
- The newer two adopt the JIRA project-linker; the oldest does not.

What's inconsistent (and resolved by the canonical structure):

- Section naming (Background vs Overview, Plans vs Releases, etc.).
- Whether reviews are nested under architecture or top-level (canonical
  says top-level).
- Whether ontology is under architecture or top-level (canonical says
  top-level).
- Whether sprint planning lives under "Planning" or its own section
  (canonical says `06 Sprints`).

---

## Quick Lookup — Page IDs for Reference Macro Implementations

If you need to study the exact ADF for the homepage macros (project-linker,
recently-updated, contributors), fetch:

- TBMLI homepage: `6487081701`
- SAA homepage: `6508381002`

Both contain the same three macro stack and serve as reference
implementations for the Homepage template in `page-templates.md`.
