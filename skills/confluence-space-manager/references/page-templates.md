# Page Body Templates

Body templates for each canonical section. Each template lists:
- **Purpose** — what the page is for
- **Variables** — `{{...}}` placeholders filled from steering/release/spec metadata
- **Body** — Markdown body to publish (Atlassian MCP `createConfluencePage`
  accepts Markdown for top-level body content; macros use ADF extension
  blocks documented inline)

When creating pages via `mcp__atlassian__createConfluencePage`, the API accepts
plain Markdown for most content. For Confluence-specific macros (project
linker, recently updated, contributors, table of contents), include them as
embedded ADF extension blocks within the request body when the API surface
supports it; otherwise, ask the user to add the macro manually after page
creation. Always confirm placement of macros in the post-creation review.

---

## Homepage Template

**Purpose:** the front door of the space — describes the product in one
paragraph, surfaces the JIRA project, and shows recent activity.

**Variables:**
- `{{project-name}}` — full product name (from `product.md`)
- `{{description}}` — one-sentence purpose (from `product.md`)
- `{{jira-project-key}}` — e.g., `TBMLI`

**Body:**

```markdown
## Description

{{description}}

## Project Tracker

> Macro: `com.atlassian.confluence.project-linker` — bound to JIRA project
> `{{jira-project-key}}`. If the macro is not pre-rendered by the API, ask
> the user to insert "Project linker" via the Confluence editor and select
> the project.

## Recently Updated

> Macro: `recently-updated` — types: page, whiteboard, database, blog;
> max=10; theme=concise; hideHeading=true.

## Contributors

> Macro: `contributors` — scope=descendants; limit=10.

---

## Quick Links

- [Steering](./02 Steering)
- [Releases](./03 Releases)
- [Architecture](./04 Architecture)
- [Specs](./05 Specs)
- [Reviews](./07 Reviews)
```

---

## 01 Overview Template

**Purpose:** narrative description of what the system does, who uses it,
and the high-level architecture diagram. Stable — changes rarely.

**Variables:**
- `{{product-name}}`
- `{{description}}`
- `{{primary-users}}` — bullet list from `product.md`
- `{{key-features}}` — bullet list (top 3–5)
- `{{system-diagram}}` — ASCII or mermaid diagram

**Body:**

```markdown
## What the System Does

{{description}}

The {{product-name}} automates and augments the work traditionally
performed by {{primary-users}} by:

{{key-features}}

## System Structure (At a Glance)

\`\`\`
{{system-diagram}}
\`\`\`

## What is Novel

(populated by the architect during high-level design — link to
`04 Architecture / Architecture Principles`)

## Documentation Structure

This space is organised as follows:

1. **[01 Overview](./01 Overview)** — this page
2. **[02 Steering](./02 Steering)** — product vision, tech stack, project structure
3. **[03 Releases](./03 Releases)** — release plans and roadmap
4. **[04 Architecture](./04 Architecture)** — system architecture and component designs
5. **[05 Specs](./05 Specs)** — feature specifications
6. **[06 Sprints](./06 Sprints)** — sprint kick-offs and retros
7. **[07 Reviews](./07 Reviews)** — code and architecture reviews
8. **[08 Ontology](./08 Ontology)** — domain models
9. **[09 References](./09 References)** — external references and glossary
```

---

## 02 Steering Template (parent page)

**Purpose:** holder for the three steering documents.

**Body:**

```markdown
## Project Steering Documents

These three pages are mirrored from the repo's `.claude/steering/` directory.
They are the project's long-lived "constitution" — they change rarely and
intentionally.

| Document | Purpose | Last Updated |
|----------|---------|--------------|
| [Product Vision](./Product Vision) | Vision, users, key features, objectives | (auto) |
| [Technology Stack](./Technology Stack) | Stack, frameworks, libraries, tooling | (auto) |
| [Project Structure](./Project Structure) | Directory layout, naming conventions | (auto) |

The content of each child page is owned by `product-vision-steering`. To
refresh, run that skill against the repo.
```

The three child pages (`Product Vision`, `Technology Stack`,
`Project Structure`) are populated by `product-vision-steering` — this skill
only creates them as empty placeholders if they do not exist.

---

## 03 Releases Template (parent page)

**Purpose:** index of all releases, current and historic.

**Body:**

```markdown
## Releases

| Release | Status | Target Date | Plan | Roadmap |
|---------|--------|-------------|------|---------|
| {{release-name}} | {{status}} | {{date}} | [Plan](./{{release-name}}/Release Plan) | [Roadmap](./{{release-name}}/Roadmap) |

> Each release child page is owned by `release-planner`. Adding a new
> release requires running that skill — it creates the child page tree and
> the JIRA epic skeletons.
```

---

## 04 Architecture Template (parent page)

**Purpose:** index of architecture pages, with the canonical sub-pages
seeded.

**Body:**

```markdown
## Architecture

This section captures the system's architecture at three levels:

1. **Solution Architecture** — high-level component view, integration
   topology, deployment model.
2. **Architecture Principles** — non-functional decisions, constraints, and
   trade-offs that shape every component.
3. **Component / Service Designs** — one child page per component, each with
   its own `Architecture Design v{N}` and (optionally) `Architecture Review v{N}`.

| Page | Owner | Purpose |
|------|-------|---------|
| [Solution Architecture](./Solution Architecture) | `software-architect` | System-wide view |
| [Architecture Principles](./Architecture Principles) | `software-architect` | NFRs, constraints |
| [Domain Ontology](../08 Ontology) | `ob-ontologist` | Cross-link to ontology section |
| [Components](#components) | per-component architect skill | One child per component |

## Components

(One child page per service / pipeline / agent / UI component.)
```

---

## 05 Specs Template (parent page)

**Purpose:** index of feature specs, mirroring `.claude/specs/`.

**Body:**

```markdown
## Feature Specifications

| Feature | Status | Requirements | Design | Tasks | Tickets |
|---------|--------|--------------|--------|-------|---------|
| {{feature-name}} | {{status}} | [Reqs](./{{feature-name}}/Requirements) | [Design](./{{feature-name}}/Design) | [Tasks](./{{feature-name}}/Tasks) | [JIRA epic](#) |

> Each feature child page is owned by `feature-spec-author`. The three
> grandchildren (Requirements, Design, Tasks) are written from the
> approved spec files in `.claude/specs/{{feature-name}}/`.
```

---

## 06 Sprints Template (parent page)

**Purpose:** index of sprint kick-off and retro pages.

**Body:**

```markdown
## Sprints

| Sprint | Dates | Kick-off | Retro |
|--------|-------|----------|-------|
| {{N}} | {{start}} → {{end}} | [Kick-off](./Sprint {{N}} — {{dates}}) | (after sprint) |

> Sprint pages are owned by `sprint-planner` (kickoff) and `sprint-executor`
> (retro append).
```

---

## 07 Reviews Template (parent page)

**Purpose:** index of all reviews, grouped by area.

**Body:**

```markdown
## Reviews

Reviews are date-stamped, append-only pages. Never overwrite — create a new
page for each review pass.

### Code Reviews

Grouped by area. Naming convention: `{Area} — Review — {YYYY-MM-DD} {hostname}`.

- [Pipelines](./Code Reviews/Pipelines)
- [Frontend](./Code Reviews/Frontend)
- [General](./Code Reviews/General)

### Architecture Reviews

Naming convention: `{Component} — Architecture Review v{N}` (versioned)
or `{Component} — Architecture Review — {YYYY-MM-DD}` (dated).

> See `references/naming-conventions.md` in the
> `confluence-space-manager` skill for the full naming rules.
```

---

## 08 Ontology Template (parent page)

**Purpose:** index of domain ontology pages.

**Body:**

```markdown
## Domain Ontologies

| Domain | Page | Owner |
|--------|------|-------|
| {{domain}} | [Ontology - {{domain}}](./Ontology - {{domain}}) | `ob-ontologist` |

> Ontology pages are first-class artifacts — they are referenced by both
> architecture pages (`04 Architecture`) and feature specs (`05 Specs`).
> Each domain has its own page named `Ontology - {Domain}` (e.g.,
> `Ontology - Legal Entities`).
```

---

## 09 References Template (parent page)

**Purpose:** index of cross-cutting references and audit reports.

**Body:**

```markdown
## References

### External References

| Topic | Link | Notes |
|-------|------|-------|
| (add as you go) | | |

### Glossary

(Optional — link to a glossary page if it exists.)

### Space Audits

Reports produced by the `confluence-space-manager` skill. Latest first.

- (audits will appear here after the first run)
```

---

## 99 WIP Template (parent page)

**Purpose:** scratch / drafts area. No template content — intentionally blank.

**Body:**

```markdown
## Work in Progress

Scratch and drafts area. Pages here are exempt from naming conventions
and audit checks. Promote to a canonical section when a page is ready.
```

---

## Per-Component Architecture Design Template

**Purpose:** the body shape for `{Component} — Architecture Design v{N}`
pages. The `software-architect` (or scope-specific architect) skill is the
content owner — this template is what `confluence-space-manager` seeds when
it creates the page placeholder.

**Variables:**
- `{{component-name}}`
- `{{version}}`

**Body:**

```markdown
# {{component-name}} — Architecture Design v{{version}}

> Owner: `software-architect` (or scope-specific architect skill).
> This is a placeholder created by `confluence-space-manager`. Run the
> appropriate architect skill to populate the five canonical deliverables:
>
> 1. Solution Overview
> 2. Component Model
> 3. Technology Mapping
> 4. Integration Design
> 5. Open Questions and Risks
```

---

## Per-Feature Spec Template

**Purpose:** the body shape for `05 Specs / {feature-name} / {Requirements,
Design, Tasks}` pages. Owner is `feature-spec-author`. Placeholders only.

**Body for each grandchild (Requirements / Design / Tasks):**

```markdown
# {{section}} — {{feature-name}}

> Owner: `feature-spec-author`. This is a placeholder created by
> `confluence-space-manager`. Run `feature-spec-author` against
> `.claude/specs/{{feature-name}}/{{section-lowercase}}.md` to populate.
```

---

## Notes on Macro Embedding

The Atlassian MCP `createConfluencePage` tool accepts Markdown for body
content via the `bodyRepresentation: "markdown"` parameter (subject to API
surface — confirm at use time). For Confluence-specific macros, the
Markdown body cannot embed them directly. Two patterns:

1. **Post-creation update** — create the page with the Markdown body, then
   call `updateConfluencePage` with an ADF body that includes the macros
   as `extension` nodes. The ADF nodes for the macros used in the homepage
   template are documented in TBMLI's homepage (page ID `6487081701`) and
   SAA's homepage (page ID `6508381002`) as reference implementations.

2. **Manual macro insertion** — create the page with placeholders
   (`> Macro: ...`) in the body. After creation, prompt the user to insert
   the macros via the Confluence editor. Acceptable for first-pass scaffold
   — the Audit mode flags missing macros as `low` severity.

Pattern 1 is preferred when the API supports it. Pattern 2 is the fallback.

---

## Reference ADF — Macro Snippets

Copy these `extension` node shapes into ADF bodies as needed.

### project-linker

```json
{
  "type": "extension",
  "attrs": {
    "layout": "default",
    "extensionType": "com.atlassian.confluence.project-linker",
    "extensionKey": "project-linker",
    "localId": "<uuid>"
  }
}
```

### recently-updated

```json
{
  "type": "extension",
  "attrs": {
    "layout": "default",
    "extensionType": "com.atlassian.confluence.macro.core",
    "extensionKey": "recently-updated",
    "parameters": {
      "macroParams": {
        "types": {"value": "page,whiteboard,database,blog"},
        "max": {"value": "10"},
        "theme": {"value": "concise"},
        "hideHeading": {"value": "true"}
      },
      "macroMetadata": {
        "macroId": {"value": "<uuid>"},
        "schemaVersion": {"value": "1"},
        "title": "Recent updates"
      }
    },
    "localId": "<uuid>"
  }
}
```

### contributors

```json
{
  "type": "extension",
  "attrs": {
    "layout": "default",
    "extensionType": "com.atlassian.confluence.macro.core",
    "extensionKey": "contributors",
    "parameters": {
      "macroParams": {
        "scope": {"value": "descendants"},
        "limit": {"value": "10"}
      },
      "macroMetadata": {
        "macroId": {"value": "<uuid>"},
        "schemaVersion": {"value": "1"},
        "title": "Contributors"
      }
    },
    "localId": "<uuid>"
  }
}
```
