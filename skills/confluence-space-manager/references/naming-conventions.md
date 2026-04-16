# Naming Conventions

These rules cover both *section* titles (the canonical top-level pages) and
*artifact* titles (designs, reviews, specs, sprints) — everything the
Confluence Space Manager creates or audits.

---

## Section Titles (Top-Level Pages)

Numeric-prefix format: `{NN} {Section Name}`.

- `NN` is a two-digit zero-padded integer (`01`–`99`).
- One space between `NN` and the section name.
- Section name uses Title Case.
- The numeric prefix is **part of the title** — Audit mode treats it as
  significant.

Reserved numbers:

| NN | Section |
|----|---------|
| 01 | Overview |
| 02 | Steering |
| 03 | Releases |
| 04 | Architecture |
| 05 | Specs |
| 06 | Sprints |
| 07 | Reviews |
| 08 | Ontology |
| 09 | References |
| 99 | WIP |

Numbers `10`–`98` are open for project-specific top-level sections (e.g.,
`50 Compliance` for a regulated product). Audit mode flags unknown
numbered sections as `extra` with severity `info`.

Conditional sections (no numeric prefix):

| Title | Condition |
|-------|-----------|
| `Proposal` | scope = research-bid |
| `Templates` | Confluence-auto |

---

## Artifact Titles

### Architecture Designs

Format: `{Component Name} — Architecture Design v{N}`

- Em-dash (`—`, U+2014), surrounded by single spaces.
- `Component Name` in Title Case, no acronyms expanded unless ambiguous.
- `v{N}` is a sequential integer starting at `1`. Increment on substantive
  redesign, not minor edits.

Examples:
- `Address Verification Services — Architecture Design v1`
- `Agent Harness — Design v2` (legacy variant — accepted, severity `low`)

### Architecture Reviews

Two valid formats:

1. **Versioned:** `{Component Name} — Architecture Review v{N}`
2. **Dated:**    `{Component Name} — Architecture Review — {YYYY-MM-DD}`

Dated form is preferred when the review is informal or AI-assisted (matches
the Code Review pattern). Versioned form is preferred when the review
formally accompanies a design version.

Examples:
- `Agent Harness - Architecture Review (agent-architect)` — accepted, low
- `Trades Pipeline — Architecture Review 2026-04-04` — accepted (dated)

### Code Reviews

Format: `{Area or Component} — Review — {YYYY-MM-DD} {hostname-or-codename}`

- The trailing host-or-codename token captures *which agent / machine*
  produced the review (e.g., `MAUDLIN`, `roy.corp.ontoledgy.io`,
  `poledouris`, `Boulez`). It is observed informally in TBMLI and ACE
  and is now canonical.
- The host token is optional but recommended — it disambiguates
  same-day reviews from different agents.

Examples:
- `File System Snapshot Service - Review - 2026-03-24-2216 MAUDLIN`
- `Document Control Identity Service - Review - 2026-03-11-0813 roy.corp.ontoledgy.io`
- `Code Review - Services - 2026-04-03` (no host — accepted, info)

### Implementation Plans

Format: `Implementation Path — {Component Name}`
or:     `{Component Name} — Implementation Plan`

Both are accepted. The first is observed in TBMLI, the second in earlier
spaces. Audit mode does not flag either.

### Feature Specs

Top-level child of `05 Specs`: `{feature-name}` (kebab-case, no spaces).

Grandchildren (canonical):
- `Requirements`
- `Design`
- `Tasks`

These are mirrored from `.claude/specs/{feature-name}/{requirements,design,tasks}.md`.

### Release Pages

Top-level child of `03 Releases`: `{Release Name}` (free text — typically
`MVP`, `v1.0`, `Q2-2026`).

Grandchildren:
- `Release Plan`
- `Roadmap`
- `Linked Epics`

### Sprint Pages

Format: `Sprint {N} — {start-date} → {end-date}`

Example: `Sprint 1 — 2026-04-14 → 2026-05-31`

Optionally augment with the sprint theme: `Sprint {N} — {dates} — {theme}`.

### Domain Ontology Pages

Under `08 Ontology`: `Ontology - {Domain}` (note hyphen-with-spaces, not em-dash).

Examples:
- `Ontology - Legal Entities`
- `Ontology - Trades`
- `Ontology - Addressess` (sic — typo in TBMLI; flag in audit, severity `low`)

The hyphen-form is preserved for backwards compatibility with TBMLI; new
spaces may use the em-dash form `Ontology — {Domain}` if preferred.

---

## Casing & Punctuation Rules

| Rule | Example |
|------|---------|
| Em-dashes for `Title — Subtitle` separation | `Component — Design v1` |
| Title Case for section names | `Architecture` not `architecture` |
| kebab-case for feature names | `licence-data-extraction` |
| Plain dates as `YYYY-MM-DD` | `2026-04-14` |
| Datetime as `YYYY-MM-DD-HHMM` (no colons) | `2026-03-24-2216` |
| ASCII hyphen `-` for `Ontology - {Domain}` | `Ontology - Trades` |

---

## Forbidden Patterns

These will be flagged by Audit mode at severity `medium`:

- Trailing whitespace in titles.
- Double spaces inside titles (e.g., `Code Review  -  2026-04-03`).
- Mixed em-dash and hyphen in the same title (`Component — Review - v1`).
- Date in non-ISO format (`24/03/2026`, `March 24 2026`).
- All-caps section titles (`ARCHITECTURE`).

These will be flagged at severity `low` (correctable but not blocking):

- Missing numeric prefix on a top-level section.
- Hyphen used where em-dash is canonical (`Component - Design v1`).
- Inconsistent version capitalisation (`V1` vs `v1`).
- Component name in lowercase (`agent harness — design v1`).

---

## Migration Rules

When Audit mode flags a misnamed page:

1. Generate the canonical title.
2. Diff: present before/after.
3. Recommend `rename` action (severity `low`/`medium`).
4. Wait for user approval — never auto-rename.
5. On approval, `updateConfluencePage` with the new title (body unchanged).

Renames preserve the page ID and URL slug — the slug typically updates
automatically but old URLs continue to resolve via Confluence's redirect.
