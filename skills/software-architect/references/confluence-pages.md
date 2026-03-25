# Confluence Pages Reference

Cloud ID: `c62e56c2-b224-4d4e-a859-afa7de01241e`

---

## When to Fetch vs. When to Create

| Action | When |
|--------|------|
| **Fetch** | At the start of Design Mode or Review Mode — to understand current system context |
| **Create** | After approval of a new design deliverable — to publish the architecture |
| **Update** | After a review produces recommendations that have been actioned |

---

## Architecture Reference Pages (Fetch in Design Mode)

These pages provide the current BIE/BNOP architecture context that informs design decisions.

| Page | Page ID | When to Fetch |
|------|---------|--------------|
| Table of Contents | `6471319553` | Always — start here for system overview |
| Foundation Model | `6472269834` | Always — core type system and BIE framework reference |
| Domain Model General | `6471680023` | When designing a new domain component |
| Identifier Implementation | `6472138756` | When identity patterns are in scope |
| Domain Identifiers General | `6472269884` | When domain identity composition is in scope |
| General Data Implementation | `6471811125` | When reviewing or extending data implementation patterns |
| Domain-Specific Data | `6472073227` | When working with an existing domain component |
| Gap Analysis | `6472269856` | In Review Mode — checklist reference |

---

## Architecture Design Space (Create / Update)

Architecture design documents should be created under the main Architecture space. The structure below represents the target page hierarchy:

```
Architecture
└── Solution Designs
    └── [Solution Name] — Design vN
        ├── Solution Overview
        ├── Component Model
        ├── Technology Mapping
        ├── Integration Design
        └── Open Questions and Risks
└── Architecture Reviews
    └── [Solution Name] — Review vN
        ├── Extracted Architecture
        ├── Gap Analysis
        └── Recommendations
```

**Note:** If the target parent page ID is not known, fetch the Table of Contents page (`6471319553`) first to navigate to the correct space and identify the parent page ID before creating.

---

## Page Creation Guidelines

When creating an architecture design page:

1. **Title format:** `[Solution Name] — Architecture Design v[N]` or `[Solution Name] — Architecture Review v[N]`
2. **Parent page:** Under `Solution Designs` or `Architecture Reviews` in the Architecture space
3. **Content:** Use the 5 deliverables format from SKILL.md (Design Mode) or the gap analysis format (Review Mode)
4. **Labels:** Add labels `architecture`, `design`, and the solution name (snake_case)
5. **Link back:** If this is a review, link to the original design page

---

## Fetching Pages

Use `mcp__atlassian__getConfluencePage` with the page ID and cloud ID above.

Example — fetching the Foundation Model page:
```
mcp__atlassian__getConfluencePage({
  cloudId: "c62e56c2-b224-4d4e-a859-afa7de01241e",
  pageId: "6472269834"
})
```

## Creating Pages

Use `mcp__atlassian__createConfluencePage` with:
- `cloudId`: `c62e56c2-b224-4d4e-a859-afa7de01241e`
- `spaceKey`: the target space key (fetch TOC to confirm)
- `parentPageId`: the ID of the parent page in the hierarchy above
- `title`: formatted as per guidelines above
- `content`: Confluence Storage Format (XHTML) or Markdown (check API capability)
