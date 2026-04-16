# Canonical Confluence Space Structure

This is the reference layout that every solution-specific Confluence space at
Ontoledgy should converge on. It is derived from the most mature space
(`SAKE`/ACE — Agentic Chemical Engineer), the JIRA-integrated mid-mature
space (`TBMLI`), and the newest space (`SAA` — Solution - Agentic Accountant).
See `reference-spaces.md` for an annotated tour of each.

The structure is opinionated but flexes per solution scope. **Mandatory**
sections must be present in every space. **Conditional** sections are present
only when the scope flag matches.

---

## Top-Level Tree

```
{Space Homepage}
│  ├─ Description (one-paragraph product purpose)
│  ├─ Project Tracker (com.atlassian.confluence.project-linker macro)
│  ├─ Recently Updated (recently-updated macro)
│  └─ Contributors (contributors macro)
│
├── 01 Overview                          [mandatory]
├── 02 Steering                          [mandatory]
│   ├── Product Vision                   [mirror of .claude/steering/product.md]
│   ├── Technology Stack                 [mirror of .claude/steering/tech.md]
│   └── Project Structure                [mirror of .claude/steering/structure.md]
│
├── 03 Releases                          [mandatory once a release exists]
│   └── {release-name}                   [one per release; e.g., "MVP", "v1.0"]
│       ├── Release Plan                 [mirror of .claude/releases/{name}/features.md]
│       ├── Roadmap                      [scope tiers + dependency diagram]
│       └── Linked Epics                 [JIRA epic links + status]
│
├── 04 Architecture                      [mandatory]
│   ├── Solution Architecture            [high-level across the system]
│   ├── Architecture Principles          [optional but recommended]
│   ├── Domain Ontology                  [BORO-grounded; or link to 08]
│   ├── Components / Services            [one child page per component]
│   │   └── {Component Name}
│   │       ├── {Component} — Architecture Design v{N}
│   │       ├── {Component} — Architecture Review v{N}  [optional]
│   │       └── Implementation Path — {Component}        [optional]
│   ├── APIs, Interfaces and Deployment Model   [optional]
│   └── Tools, Compute and Environments         [optional]
│
├── 05 Specs                             [mandatory once specs exist]
│   └── {feature-name}                   [one per feature; mirror of .claude/specs/{feature}/]
│       ├── Requirements
│       ├── Design
│       └── Tasks                        [with linked JIRA tickets]
│
├── 06 Sprints                           [mandatory once a sprint exists]
│   └── Sprint {N} — {dates}             [kickoff + retro]
│
├── 07 Reviews                           [mandatory]
│   ├── Code Reviews                     [grouped by area: Pipelines, Frontend, General]
│   │   └── {Area or Component} — Review — {YYYY-MM-DD} {hostname}
│   └── Architecture Reviews             [optional sub-grouping; same date-stamp pattern]
│
├── 08 Ontology                          [mandatory if domain modelling is in scope]
│   └── {Domain} — {Aspect}              [e.g., "Ontology - Legal Entities"]
│
├── 09 References                        [mandatory]
│   ├── External References              [links to standards, papers, vendor docs]
│   ├── Glossary                         [optional]
│   └── Space Audits                     [audit reports created by this skill]
│
├── 99 WIP                               [optional but expected]
│   └── (free-form scratch / drafts)
│
├── Proposal                             [conditional — scope = research-bid]
│   ├── Public Description
│   ├── Scope
│   ├── Question 09–15 (or as defined by the funder)
│   └── Question 10 — Technical Approach
│
└── Templates                            [conditional — auto-created by Confluence]
    ├── Template - Project plan
    ├── Template - Decision documentation
    └── Template - Meeting notes
```

---

## Section Ownership

Every canonical section has an *owner skill* — the skill responsible for
publishing or updating its content. The Confluence Space Manager owns the
*shape* (parent IDs, titles, ordering), not the *content*.

| Section | Owner Skill | Notes |
|---------|-------------|-------|
| 01 Overview | `confluence-space-manager` (initial), maintained by humans | Narrative + system diagram. Stable. |
| 02 Steering | `product-vision-steering` | Each child page mirrors a `.claude/steering/*.md` file. |
| 03 Releases | `release-planner` | One child per release; updated mid-release if scope changes. |
| 04 Architecture | `software-architect`, `bclearer-pipeline-architect`, `agent-architect`, `ui-architect`, `ob-architect` | Each architect skill writes under the appropriate component subpage. |
| 05 Specs | `feature-spec-author` | One child per feature, with three grandchildren (requirements, design, tasks). |
| 06 Sprints | `sprint-planner`, `sprint-executor` | Kickoff written by planner, retro appended by executor. |
| 07 Reviews | `clean-code-reviewer`, `clean-code-size`, `software-architect` (review mode) | Date-stamped pages — never overwrite. |
| 08 Ontology | `ontologist`, `ob-ontologist`, `bie-component-ontologist` | First-class domain models. |
| 09 References | Mixed (humans + this skill for audit reports) | Catch-all for cross-cutting references. |
| 99 WIP | Anyone | Tolerated — never enforced. Tracked but not audited for content. |
| Proposal | Humans (research / bid team) | Bespoke per funder; structure mirrors funder's question list. |
| Templates | Confluence (auto) | Don't move or rename — Confluence regenerates them. |

---

## Mandatory vs. Conditional Sections

| Section | Always present? | Triggering condition |
|---------|-----------------|---------------------|
| 01 Overview | ✅ Always | — |
| 02 Steering | ✅ Always | — |
| 03 Releases | Only after first release planned | `.claude/releases/` exists |
| 04 Architecture | ✅ Always | — |
| 05 Specs | Only after first feature specced | `.claude/specs/` exists |
| 06 Sprints | Only after first sprint planned | `.claude/sprints/` exists |
| 07 Reviews | ✅ Always | — |
| 08 Ontology | Domain modelling in scope | Repo contains BORO/BIE domain code |
| 09 References | ✅ Always | — |
| 99 WIP | Optional | Created on first scratch page |
| Proposal | scope = research-bid | Explicit flag |
| Templates | Optional (Confluence auto) | Created by Confluence |

A space passes the audit's *minimum viable structure* check if all sections
marked ✅ Always are present.

---

## Numeric Prefix Convention

Top-level section titles begin with a two-digit numeric prefix (e.g.,
`01 Overview`) so they render in the Confluence sidebar in a stable order.
This is observed informally in some spaces and is now the canonical rule.

- Numbers are zero-padded to two digits (`01`–`99`).
- Numbers are spaced from the title with a single space.
- The number is part of the canonical title — Audit mode treats
  `Overview` (no prefix) as **misnamed**, not missing.
- Existing spaces (ACE, TBMLI, SAA) use unprefixed titles. Audit mode
  flags this as misnamed with severity `low` — adoption is gradual and
  user-approved.

---

## Section-Title Variants — Acceptance Rules

Audit mode treats these variants as the same canonical section. Renaming is
recommended (severity `low`) but not blocking.

| Canonical Title | Accepted Variants | Severity if variant |
|-----------------|-------------------|---------------------|
| `01 Overview` | `Overview`, `Background`, `Introduction` | low |
| `02 Steering` | `Steering`, `Foundation`, `Project Steering` | low |
| `03 Releases` | `Releases`, `Plans`, `Roadmap` | low |
| `04 Architecture` | `Architecture`, `System Architecture`, `System Architecture and Agent Roles` | low |
| `05 Specs` | `Specs`, `Specifications`, `Features` | low |
| `06 Sprints` | `Sprints`, `Iterations` | low |
| `07 Reviews` | `Reviews`, `Code Reviews` (if no architecture reviews exist) | low |
| `08 Ontology` | `Ontology`, `Domain Ontology`, `Domain Models`, `Ontologies` | low |
| `09 References` | `References`, `Reference`, `External References` | low |
| `99 WIP` | `WIP`, `Drafts`, `Scratch`, `Sandbox` | low |

Anything that doesn't match the canonical title or any accepted variant is
classified as `extra` — flagged for human review, never auto-archived.

---

## Examples — How Real Spaces Map

A short summary; full annotated tour in `reference-spaces.md`.

### ACE (`SAKE`) — research-bid scope

| Existing Page | Canonical Section | Notes |
|---------------|-------------------|-------|
| Background | 01 Overview | misnamed (low) |
| Proposal | Proposal | conditional, present (research-bid scope) |
| WIP - Tasks | 99 WIP | misnamed (low) |
| Current Assets/Infrastructure | 04 Architecture (subsection) | misplaced (could move under Architecture) |
| Scope - Requirement | (scope-conditional, near Proposal) | extra; intentional for funding context |
| System Architecture and Agent Roles | 04 Architecture | misnamed (low) |
| WIP | 99 WIP | misnamed (low) |
| References | 09 References | misnamed (low) — missing prefix |
| Plans | 03 Releases | misnamed (low) |
| (missing) | 02 Steering | not yet created — recommend create |
| (missing) | 05 Specs | not yet created — recommend create |
| (missing) | 06 Sprints | not yet created — recommend create |
| (missing) | 07 Reviews | not yet created — recommend create |
| (missing) | 08 Ontology | partially under "Current Assets/Infrastructure → Ontologies" |

### TBMLI — solution scope, JIRA-integrated

| Existing Page | Canonical Section | Notes |
|---------------|-------------------|-------|
| Architecture | 04 Architecture | misnamed (low) — missing prefix |
| Code Reviews | 07 Reviews | misnamed (low) — should be `07 Reviews` with `Code Reviews` as subsection |
| Ontology | 08 Ontology | misnamed (low) |
| Planning | 03 Releases / 06 Sprints | misnamed + ambiguous (low/med) — split into two |
| (missing) | 01 Overview | recommend create |
| (missing) | 02 Steering | recommend create |
| (missing) | 05 Specs | recommend create |
| (missing) | 09 References | recommend create |

### SAA — solution scope, sparse

| Existing Page | Canonical Section | Notes |
|---------------|-------------------|-------|
| Architecture | 04 Architecture | misnamed (low) |
| Architecture → Code Reviews | 07 Reviews | misplaced + misnamed |
| Architecture → Solution → Domain Ontology (BORO) | 08 Ontology | misplaced |
| Architecture → Solution → Solution Architecture | 04 Architecture (subsection) | misplaced |
| Templates | Templates | conditional, present |
| (missing) | 01 Overview, 02 Steering, 03 Releases, 05 Specs, 06 Sprints, 09 References | mostly empty space |

---

## Why This Structure

1. **Predictability.** A new contributor to any space knows where to find
   architecture, releases, and reviews without orientation.
2. **Tool alignment.** The mirror sections (02 Steering, 03 Releases, 05
   Specs, 06 Sprints) match the `.claude/` repo layout so publishing skills
   know exactly where their output lands.
3. **JIRA integration is first-class.** The homepage's project-linker macro
   means tickets surface immediately rather than being buried.
4. **Reviews are durable.** Date-stamped review pages are append-only,
   preserving history rather than churning a single "Review" page.
5. **Audit-ability.** Numeric prefixes + acceptance rules make the audit
   deterministic and the gap report actionable.

---

## Open Questions

- Should `08 Ontology` be a child of `04 Architecture` instead of a top-level
  section? Pro: closer to where it is consumed. Con: ontologies are reused
  across architecture/specs/components and benefit from a dedicated home.
  **Current decision: top-level, with a "see also" link from `04`.**
- Should `Proposal` (research-bid) get a numeric prefix? **Current decision:
  no — it sits outside the canonical numeric series because it is conditional
  and bespoke per funder.**
