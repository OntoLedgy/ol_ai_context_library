# Audit Checklist

The row-by-row checklist used in Audit Mode. Each row evaluates one
canonical aspect of the space and produces a finding with a severity and a
recommended action.

---

## Severity Ladder

| Severity | Meaning | Audit blocks merge? |
|----------|---------|---------------------|
| `critical` | Mandatory section missing or fundamentally broken (e.g., homepage has no JIRA linker on a JIRA-tracked project). | Always surface to user. |
| `high` | A section is misplaced in a way that breaks navigation (e.g., specs nested under reviews). | Always surface. |
| `medium` | Naming convention violation that confuses search (forbidden pattern). | Surface. |
| `low` | Naming preference (numeric prefix missing, hyphen vs em-dash). | Surface as batch suggestion. |
| `info` | Bespoke page or convention deviation that may be intentional. | Surface for human review only. |

Audit mode is **non-blocking** — it never refuses to publish. It produces a
report; Align mode applies user-approved actions.

---

## Coverage Score

```
coverage = present / (present + missing + misnamed + misplaced)
```

Calculated over the **mandatory** sections only (those marked ✅ Always in
`canonical-space-structure.md`). Range: 0.0 – 1.0. Reported in the audit
header as a percentage.

The score is informative — used to track drift over time across multiple
audits of the same space, not as a gate.

---

## Checklist Rows

Each row is structured as:
- **What** — the canonical thing being checked
- **How** — the API/MCP call or comparison performed
- **Severity** if absent or broken
- **Recommended action** when violated

### Row A — Homepage Exists and Has JIRA Linker

- **What:** the space's homepage exists and contains a
  `com.atlassian.confluence.project-linker` extension.
- **How:** `getConfluencePage(homepageId)`; scan `body.content` for the
  extension node.
- **Severity if missing:** `critical` (if a JIRA project is configured) or
  `medium` (if no JIRA project — recommend setting one up).
- **Recommended action:** append a "Project Tracker" section with the
  project-linker macro.

### Row B — Homepage Has Activity Macros

- **What:** homepage contains `recently-updated` and `contributors` macros.
- **How:** scan `body.content`.
- **Severity if missing:** `low`.
- **Recommended action:** append the macros to the homepage.

### Row C — Mandatory Sections Present

For each section marked ✅ Always in `canonical-space-structure.md`:

- **What:** a top-level child of the homepage exists with the canonical
  title or an accepted variant.
- **How:** `getConfluencePageDescendants(homepageId, depth=1)`; compare
  titles.
- **Severity if missing:** `critical` for `01 Overview`, `02 Steering`,
  `04 Architecture`, `09 References`. `high` for `07 Reviews`. `medium`
  otherwise.
- **Recommended action:** `create` the section using the appropriate
  template from `page-templates.md`.

### Row D — Section Titles Match Canonical Form

- **What:** each present section uses the canonical title (numeric prefix
  + Title Case).
- **How:** string compare against canonical title; if it matches an accepted
  variant, classify as misnamed (low).
- **Severity if violated:** `low`.
- **Recommended action:** `rename` to canonical form.

### Row E — Conditional Sections Match Scope

- **What:** if scope = `research-bid`, `Proposal` exists; if scope ≠
  `research-bid`, `Proposal` is absent or moved to `99 WIP`.
- **How:** scan top-level children for `Proposal`; check repo for scope
  flag in `.claude/workflow-config.md`.
- **Severity if mismatched:** `info` (intentional choice possible).
- **Recommended action:** flag for user review; do not auto-act.

### Row F — Steering Mirror Complete

- **What:** `02 Steering` has three children: `Product Vision`,
  `Technology Stack`, `Project Structure` (or accepted variants
  `product.md` / `tech.md` / `structure.md` titles).
- **How:** `getConfluencePageDescendants(steeringPageId, depth=1)`.
- **Severity if missing:** `medium` if `.claude/steering/` exists in repo;
  `info` otherwise.
- **Recommended action:** `create` placeholders and route the user to
  `product-vision-steering` to populate.

### Row G — Releases Mirror Reflects Repo

- **What:** for each `.claude/releases/{name}/` in the repo, a child page
  named `{name}` exists under `03 Releases`.
- **How:** read repo + `getConfluencePageDescendants(releasesPageId)`.
- **Severity if mismatched:** `medium` (known release missing on
  Confluence) or `info` (page exists with no repo backing — could be
  retired).
- **Recommended action:** `create` for missing; flag for review for
  unbacked.

### Row H — Specs Mirror Reflects Repo

- **What:** for each `.claude/specs/{feature}/` in the repo, a child page
  exists under `05 Specs` with three grandchildren.
- **How:** read repo + descendants.
- **Severity:** `medium` if repo spec is missing on Confluence; `info` if
  Confluence-only spec.
- **Recommended action:** `create` for missing.

### Row I — Reviews Are Date-Stamped

- **What:** every page under `07 Reviews / Code Reviews` follows the
  date-stamped naming convention.
- **How:** descendants + regex `^.*\sReview\s-\s\d{4}-\d{2}-\d{2}.*$` or
  similar.
- **Severity if violated:** `low`.
- **Recommended action:** `rename` (with user approval; some review pages
  may legitimately summarise multiple dates).

### Row J — No Mixed Em-dash/Hyphen in Titles

- **What:** titles use either em-dash or hyphen consistently within a
  single title.
- **How:** regex on each title.
- **Severity if violated:** `medium`.
- **Recommended action:** `rename` to use the canonical separator
  (`—` for `Component — Aspect`, `-` for `Ontology - Domain`).

### Row K — Forbidden Patterns Absent

- **What:** no titles contain trailing whitespace, double spaces,
  non-ISO dates, or all-caps section names.
- **How:** regex sweep across all titles.
- **Severity if violated:** `medium`.
- **Recommended action:** `rename`.

### Row L — Numeric Prefix Adoption

- **What:** top-level sections use the `NN ` prefix.
- **How:** regex `^\d{2}\s` on top-level child titles.
- **Severity if absent:** `low`.
- **Recommended action:** batch `rename` proposal — present all top-level
  sections together so the user can approve in one pass.

### Row M — Extra Top-Level Pages

- **What:** any top-level page that does not match a canonical section or
  an accepted variant.
- **How:** subtract canonical from descendants(depth=1).
- **Severity:** `info`.
- **Recommended action:** flag for review with three options:
  - `accept` — page is intentional (default for research-bid spaces).
  - `move` — relocate under a canonical section.
  - `archive` — explicit removal (requires user confirmation).

### Row N — Sprint Pages Under 06 Sprints

- **What:** sprint kick-off pages live under `06 Sprints`, not under
  `Planning` or `Architecture`.
- **How:** search for `Sprint Planning` / `Sprint Kickoff` titles
  anywhere in the space; check parent.
- **Severity if misplaced:** `medium`.
- **Recommended action:** `move` to `06 Sprints`.

### Row O — Per-Component Architecture Pages Have Designs or Stubs

- **What:** each child of `04 Architecture / Components` has either a
  `Design v{N}` child or is explicitly marked as a stub.
- **How:** descendants(depth=2); check for child page matching design
  pattern.
- **Severity if missing:** `low` (a component listed without a design is
  an open task, not a structural error).
- **Recommended action:** `create` design placeholder; route user to the
  appropriate architect skill.

### Row P — Audit Reports Archived in 09 References

- **What:** prior audit reports exist under
  `09 References / Space Audits` and are listed reverse-chronologically.
- **How:** descendants + title match.
- **Severity if missing:** `info` (first audit ever — expected).
- **Recommended action:** `create` the `Space Audits` parent and publish
  the current report there.

---

## Output — Audit Report Schema

The report is written to
`.claude/confluence/{space-key}-audit-{YYYY-MM-DD}.md` and mirrored to
Confluence under `09 References / Space Audits / {YYYY-MM-DD}`.

Schema:

```markdown
# Confluence Space Audit — {space-key} — {YYYY-MM-DD}

**Coverage:** {coverage}% ({present} of {total} mandatory sections present)
**Audited by:** confluence-space-manager
**Cloud ID:** {cloudId}
**Space ID / Key:** {spaceId} / {spaceKey}

## Summary

{N} critical, {N} high, {N} medium, {N} low, {N} info findings.

## Findings

| # | Row | What | Status | Severity | Recommended Action | Approve? |
|---|-----|------|--------|----------|-------------------|----------|
| 1 | A | Homepage JIRA linker | ❌ missing | critical | append project-linker macro | [ ] |
| 2 | C | `01 Overview` section | ❌ missing | critical | create with Overview template | [ ] |
| 3 | C | `02 Steering` section | ✅ present | — | — | n/a |
| 4 | D | `Architecture` (no prefix) | ⚠ misnamed | low | rename to `04 Architecture` | [ ] |
| ... |

## Changelog

(populated by Align mode)

| Timestamp | Action | Page | Result |
|-----------|--------|------|--------|

## Open Questions

- (Audit may surface ambiguities for human decision — list here.)
```

The `Approve?` column is the user's input — they tick the box (`[x]`) for
each action they want Align mode to apply, then call Align mode against
this file.

---

## Notes on False Positives

Some real-world cases the checklist may flag but are intentional:

- **ACE (`SAKE`) `Proposal` and `Scope - Requirement`** — research-bid
  scope; legitimate top-level pages. Audit should be invoked with
  `scope: research-bid` to suppress these as `extra`.
- **TBMLI `Ontology - Addressess`** — typo, but the page has accumulated
  links. Rename only with explicit user approval; consider creating a
  redirect note on the renamed page.
- **Reviews under `Architecture / Code Reviews`** (SAA) — reviews nested
  inside architecture is a valid alternative layout. The canonical form
  is `07 Reviews` at top level; recommend `move` but accept `keep` if the
  user prefers the alternative.
