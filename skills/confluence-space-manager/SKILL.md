---
name: confluence-space-manager
description: >
  Bootstrap, audit, and align solution-specific Confluence spaces against the
  canonical Ontoledgy space structure. Operates in three modes: (1) Create —
  scaffold a new space's page tree (Overview, Architecture, Specs, Sprints,
  Reviews, Ontology, References, Releases) on top of an existing or newly
  provisioned space; (2) Audit — compare an existing space against the
  canonical structure and produce a gap report with concrete improvement
  actions; (3) Align — apply approved improvements (rename, move, create,
  archive). Use when: a new solution repo needs a Confluence home, an existing
  space has drifted from convention, or a team wants to align multiple spaces
  before a release. Reads the repo's `.claude/steering/`, `.claude/releases/`,
  and `.claude/specs/` to seed the structure with real project metadata.
  Companion to `product-vision-steering` (Phase 0) and `release-planner`
  (Phase 0.5) — provides the *Confluence-side* container they publish into.
---

# Confluence Space Manager

## Role

You are responsible for the shape and discoverability of a solution's Confluence
space. You do not author the *content* of architecture, specs, or sprint plans —
those come from the architect, spec-author, and sprint-planner skills. You
guarantee that:

- Every solution has a predictable top-level layout so collaborators know where
  things live.
- New spaces start with the right scaffolding and the JIRA project-linker so
  ticket integration is immediate.
- Mature spaces don't drift indefinitely — they are periodically audited
  against the canon and re-aligned with explicit user approval.

You are platform-agnostic with respect to Solution / Pipeline / Agent / UI scope —
the canonical structure flexes with optional sections per scope.

---

## Operating Modes

| Mode | Inputs | Output | When to use |
|------|--------|--------|-------------|
| **Create** | Repo path (with optional `.claude/steering/`), space key (existing or new), JIRA project key | Scaffold of canonical pages created in the space + `.claude/workflow-config.md` updated | New solution repo, new project, demo/POC kickoff |
| **Audit** | Existing space key | Gap report (Markdown table + Confluence page) listing missing/misplaced/misnamed pages, with severity and a recommended action per row | Periodic review, before a release, when onboarding a new contributor |
| **Align** | Audit report (from previous mode) + user approval per item | Pages renamed, moved, created, or archived in Confluence; audit report updated with status | After Audit, when actions are approved |

The mode is named explicitly by the caller. Default to Audit if ambiguous —
auditing is read-only and never destructive.

---

## Inputs

- **Cloud ID**: `c62e56c2-b224-4d4e-a859-afa7de01241e` (Ontoledgy default —
  override only for other tenants).
- **Space key** (e.g., `TBMLI`, `SAA`, `SAKE`/`ACE`). For Create mode, may be
  TBD if a fresh space is being provisioned.
- **JIRA project key** (e.g., `TI`, `TBMLI`) — used for the project-linker
  macro on the Overview page.
- **Repo root** — used to discover steering docs, releases, and specs that
  should be reflected in the space scaffold.
- **Solution scope** (optional, one of: `solution`, `pipeline`, `agent`, `ui`,
  `bie`, `research-bid`) — toggles optional sections (e.g., a research-bid space
  also gets a Proposal section, like ACE).

---

## Outputs

| Output | Where |
|--------|-------|
| Created/updated Confluence pages | The target space |
| Gap report (Audit mode) | `.claude/confluence/{space-key}-audit-{YYYY-MM-DD}.md` + Confluence page under "References" |
| Alignment changelog (Align mode) | Appended to the same audit file under a "Changelog" section |
| Workflow config update | `.claude/workflow-config.md` — confluence space key, parent IDs of canonical sections |

---

## Canonical Structure

The full canonical structure — including which sections are mandatory, which
are scope-conditional, and the ownership of each section — lives in
`references/canonical-space-structure.md`. **Always read it before any mode
runs.** A summary is reproduced here so you can sanity-check at a glance:

```
{Space Homepage}                         ← project-linker, recently-updated, contributors
├── 01 Overview                          ← what the system does (narrative + diagram)
├── 02 Steering                          ← mirror of .claude/steering/ (product, tech, structure)
├── 03 Releases                          ← mirror of .claude/releases/ — one child per release
├── 04 Architecture                      ← Solution Architecture, Domain Ontology, per-component designs
├── 05 Specs                             ← mirror of .claude/specs/ — one child per feature
├── 06 Sprints                           ← sprint kick-offs and retrospectives
├── 07 Reviews                           ← Code Reviews and Architecture Reviews (date-stamped)
├── 08 Ontology                          ← first-class domain ontology pages (BORO + BIE)
├── 09 References                        ← external docs, related work, glossary, audit reports
├── 99 WIP                               ← scratch / drafts (not for canonical content)
└── (scope-conditional)
    ├── Proposal                         ← only when scope = research-bid
    └── Templates                        ← Confluence's auto-templates (Project plan, Decision, Meeting notes)
```

Section numbering keeps the order stable in the Confluence sidebar. Numbers are
part of the canonical title and must be preserved by Audit/Align.

---

## Workflow — Create Mode

### Step 1 — Detect Existing State

- Confirm or fetch the space (`mcp__atlassian__getConfluenceSpaces` filtered by
  `keys`). If the space does not exist, ask the user to provision it via the
  Confluence UI (the MCP cannot create spaces). Provide a one-line instruction
  and the recommended template (Project space).
- Read the homepage. If it already contains content, skip the homepage
  rewrite and **only** add missing canonical sections. Never silently overwrite
  existing user content.
- Read repo `.claude/steering/`, `.claude/releases/`, `.claude/specs/` if they
  exist — used to seed sections 02, 03, 05.

### Step 2 — Confirm Plan with User

Show a preview tree of what will be created (sections + first-level children
seeded from repo metadata). Ask for approval. The user may opt out of any
section. **Gate: do not create anything until the plan is approved.**

### Step 3 — Create Sections

In order (01 → 99), use `mcp__atlassian__createConfluencePage` for each
canonical section that is missing. For each:
- Title exactly as in the canonical structure (with the numeric prefix).
- Parent: the homepage (top-level sections) or the appropriate section page.
- Body: load from `references/page-templates.md` (one template per section
  type). Templates contain placeholders that are filled from steering /
  release / spec metadata where available.

### Step 4 — Wire JIRA Integration

If the homepage is freshly created, ensure it contains the
`com.atlassian.confluence.project-linker` extension pointing at the JIRA
project key. If the homepage pre-exists and lacks the linker, append a
"Project Tracker" section with the linker rather than overwriting the page.

### Step 5 — Persist Mapping

Write/update `.claude/workflow-config.md` with:
- `confluence.cloudId`
- `confluence.spaceKey`
- `confluence.homepageId`
- `confluence.sections.{01-overview, 02-steering, ...}` page IDs

This mapping is what `product-vision-steering`, `release-planner`,
`feature-spec-author`, and `software-architect` use as the parent for *their*
Confluence publications. Without it they fall back to asking the user.

### Step 6 — Return

Report to caller: space URL, list of created sections (with IDs), warnings
about pre-existing content not modified, and the path to the updated
`workflow-config.md`.

---

## Workflow — Audit Mode

### Step 1 — Walk the Space

- Fetch the homepage and walk descendants 2 levels deep
  (`mcp__atlassian__getConfluencePageDescendants` with `depth=2`).
- Build a tree of (title, id, parentId, position).

### Step 2 — Compare Against Canon

Run the audit checklist in `references/audit-checklist.md`. For each
canonical section, classify:

| Status | Meaning |
|--------|---------|
| ✅ present | Section exists with the expected title and position |
| ⚠ misnamed | A section with a similar purpose exists but the title doesn't follow convention |
| ⚠ misplaced | The right section exists but at the wrong depth or order |
| ❌ missing | The section is not present |
| ➕ extra | A top-level page exists that doesn't map to any canonical section (could be valid; flag for review) |

For each row, produce a recommended action: `rename`, `move`, `create`,
`archive`, or `accept` (extra pages can be intentionally bespoke — never
auto-archive).

### Step 3 — Score

Compute a simple coverage score: `present / (present + missing + misnamed + misplaced)`.
This is informative only — used in the report header to track drift over
time, not as a pass/fail gate.

### Step 4 — Publish the Report

Write the report to `.claude/confluence/{space-key}-audit-{YYYY-MM-DD}.md` and
also create/update a child page under `09 References` titled
`Space Audit — {YYYY-MM-DD}`. Ask the user to review and select which
recommended actions to apply. Recommendations are presented as a checklist
the user can edit.

### Step 5 — Hand Off

Audit mode never modifies the space. End by asking the user whether to enter
Align mode with the approved actions.

---

## Workflow — Align Mode

### Step 1 — Load Approved Actions

Read the audit report. Extract the approved action rows (those the user
checked or otherwise confirmed).

### Step 2 — Apply in Safe Order

Execute approved actions in this order to minimise transient broken links:
1. **Create** missing canonical sections (so child pages have a target to move into).
2. **Rename** misnamed pages (`updateConfluencePage` with new title — body unchanged).
3. **Move** misplaced pages (`updateConfluencePage` with new `parentId`).
4. **Archive** explicitly approved removals (set status, do not hard delete —
   audit trail matters).

After each operation, update the audit report's "Changelog" section with the
operation, the page ID, and a timestamp.

### Step 3 — Re-Audit

Re-run Audit Mode silently and confirm the coverage score improved. If any
approved action failed, surface the failure to the user with the API error.

### Step 4 — Return

Report to caller: changes applied (count by type), new coverage score, and
audit report URL.

---

## Boundaries — What This Skill Does NOT Do

- **Does not author content** for steering / specs / architecture pages —
  those skills publish their own content under the canonical sections this
  skill provisions.
- **Does not create JIRA epics, stories, or subtasks** — that is
  `release-planner` (epics) and `backlog-manager` (stories/subtasks).
- **Does not provision new Confluence spaces** — the Atlassian MCP cannot
  create spaces. This skill scaffolds *within* a space the user has already
  created.
- **Does not delete content** — archive is the strongest action available, and
  only when explicitly approved per page.
- **Does not enforce content quality** inside individual pages — that is the
  responsibility of the publishing skill (`software-architect`,
  `feature-spec-author`, etc.). This skill enforces *structure*, not *prose*.
- **Does not fork or template a new space from scratch** — bootstrapping a
  brand-new space is a follow-up skill (see *Future Work*).

---

## Future Work — Space Template Skill

Once the canonical structure is stable across 3+ spaces, this skill's
`references/page-templates.md` should be promoted to a standalone
`confluence-space-template` artifact (a JSON or YAML manifest) that:

- Can be used by an external script to **provision** a new Confluence space
  via the Atlassian REST API (the MCP doesn't currently support space
  creation).
- Powers a `--bootstrap` flag on this skill that wires the new space directly
  to a freshly initialised repo.

This is explicitly out of scope for the first cut — the page-tree templates
captured in `references/page-templates.md` are the precursor.

---

## References

- `references/canonical-space-structure.md` — the canonical page tree, section
  ownership, mandatory vs. scope-conditional sections, and naming rules.
- `references/page-templates.md` — body templates for each canonical section
  (Overview, Steering, Releases, Architecture, Specs, Sprints, Reviews,
  Ontology, References, WIP).
- `references/naming-conventions.md` — title formats for design, review,
  spec, and dated artefacts; numeric prefix rules; the per-host date-stamping
  convention observed in TBMLI and ACE.
- `references/audit-checklist.md` — the row-by-row checklist used in Audit
  mode, plus the coverage score formula and severity ladder.
- `references/reference-spaces.md` — annotated tour of ACE (`SAKE`), TBMLI,
  and SAA showing how each maps onto the canonical structure (gaps and all).
- Atlassian MCP tools: `getConfluenceSpaces`, `getConfluencePage`,
  `getConfluencePageDescendants`, `createConfluencePage`,
  `updateConfluencePage`, `searchConfluenceUsingCql`.
- Companion skills: `product-vision-steering` (Phase 0),
  `release-planner` (Phase 0.5), `feature-spec-author` (Phase 1),
  `backlog-manager` (Phase 2), `software-architect` (architecture pages).
