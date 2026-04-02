# Design System Principles and ol_ui_library

## What Is a Design System?

A design system is the single source of truth for UI: shared components, patterns, tokens,
and guidelines that allow multiple teams to build consistent interfaces efficiently without
rebuilding shared solutions.

**Business impact** (industry benchmarks for teams > 100 people):
- 46% reduction in design and development costs
- 22% faster time to market
- 40% faster release cadence for SaaS products

---

## ol_ui_library

### Purpose

`ol_ui_library` is the OntoLedgy shared UI component library. It is the UI equivalent of
`bclearer_pdk` for backend code: a **platform library** that all UI solutions depend on
rather than rebuild. When a UI feature needs a button, table, or chart panel, it comes from
`ol_ui_library` — it is not re-implemented per product.

**Repository**: `https://github.com/OntoLedgy/ol_ui_library`

### Position in the Architecture

UI components are **infrastructure**. They sit at the bottom of the dependency stack:

```
Domain Layer       business rules, ontological models
Service Layer      orchestration, data processing
Adapter Layer      API clients, data transformers
Infrastructure  ←  ol_ui_library components, routing, HTTP clients
```

UI components accept props and emit events. They carry **no domain knowledge**.
A `DataTable` does not know what an ontological `Element` is. It renders rows.

### Library Structure (Atomic Design)

```
ol_ui_library/
  atoms/        Button, Input, Label, Icon, Badge, Spinner, Avatar, Tooltip
  molecules/    FormField, SearchBox, FileDropZone, ProgressBar, Alert, Pagination
  organisms/    DataTable, NavigationBar, DocumentUploader, ChartPanel, WizardContainer
  templates/    DashboardTemplate, WizardTemplate, ResultsTemplate, EmptyStateTemplate
  tokens/       colour, spacing, typography, border-radius, shadow design tokens
  hooks/        useDebounce, useMediaQuery, useLocalStorage, usePrevious
```

---

## Design Tokens

Design tokens are the atomic values from which all visual properties are derived. They are
the bridge between design intent and code implementation.

### Token Categories

| Category | Example Tokens |
|----------|---------------|
| **Colour** | `color.brand.primary`, `color.status.error`, `color.neutral.50`, `color.status.success` |
| **Typography** | `font.size.base`, `font.weight.semibold`, `font.family.mono`, `font.line-height.tight` |
| **Spacing** | `space.1` (4px), `space.2` (8px), `space.4` (16px), `space.8` (32px) |
| **Border radius** | `radius.sm` (4px), `radius.md` (8px), `radius.lg` (16px), `radius.full` (9999px) |
| **Shadow** | `shadow.sm`, `shadow.md`, `shadow.focus` (keyboard focus ring) |
| **Z-index** | `z.modal`, `z.tooltip`, `z.dropdown` |

### Rules
- **Components reference tokens only** — no hardcoded hex, pixel, or em values in component code
- Tokens are defined once; theming is achieved by swapping token values (e.g. dark mode = token set swap)
- Token names encode **semantic intent**, not visual values (`color.status.error` not `color.red.500`)

---

## Component Contract Standard

Every component in `ol_ui_library` must have all of the following:

| Requirement | Description |
|-------------|-------------|
| **Props interface** | Fully typed TypeScript; no `any`; all props documented with JSDoc |
| **States** | default, hover, focus, active, disabled, error, loading (where applicable) |
| **Variants** | size (sm/md/lg), intent (primary/secondary/danger/ghost/warning), theme |
| **Accessibility contract** | ARIA role, keyboard shortcuts, required contrast ratio |
| **Usage examples** | Correct usage AND common misuse patterns (what not to do) |
| **Storybook story** | Interactive preview covering all states and variants |
| **Changelog entry** | What changed, why, and the semver impact |

---

## Maintaining and Extending ol_ui_library

### When to Add a Component to the Library

Add to `ol_ui_library` when:
- The same pattern is needed in **2 or more** product features or applications
- The component encapsulates complex accessibility logic (e.g. modal focus trap, keyboard navigation, skip-nav link)
- The pattern requires non-trivial shared state that consumers should not manage themselves

Keep in product code when:
- The component is specific to one business domain (e.g. `PipelineStageCard` — too specific)
- The component depends on domain types or services
- The component is a one-off for a single feature that is unlikely to recur

### Contribution Workflow

```
1. Architect designs component spec in Library Maintenance Mode
   ↓ (approval required before implementation)
2. ui-engineer implements following component standards
   ↓
3. Storybook story added covering all states and variants
   ↓
4. Usage documentation written (correct + incorrect examples)
   ↓
5. Semver bump applied; changelog entry written
   ↓
6. PR reviewed and merged
```

### Breaking Change Policy (semver)

| Version Bump | Trigger |
|-------------|---------|
| **PATCH** | Bug fix, accessibility improvement, visual polish — no API change |
| **MINOR** | New optional props, new variants, new atoms, new molecules — backwards compatible |
| **MAJOR** | Props renamed or removed, behaviour changes to existing API, Atomic-level reassignment |

**Never introduce a MAJOR change without a migration guide.**

---

## Storybook as Living Documentation

Storybook is the primary documentation surface for `ol_ui_library`:

- Each component has a dedicated story file: `ComponentName.stories.tsx`
- Stories cover: default, all states, all variants, error conditions, accessibility states, edge cases
- The Docs addon generates interactive documentation from story metadata
- Stories serve as the baseline for visual regression testing (Chromatic or equivalent)

### Minimum Story Coverage

Every component story must include:

| Story | What It Shows |
|-------|--------------|
| `Default` | Component with minimal required props |
| `AllVariants` | All size and intent combinations |
| `AllStates` | Hover, focus, active, disabled, error, loading |
| `WithError` | Error state with message |
| `Interactive` | User can interact with the component in the story panel |

---

## Accessibility Standards

All components in `ol_ui_library` must meet **WCAG 2.2 AA** minimum. The POUR framework
organises every requirement into four pillars:

| Pillar | Meaning | Examples |
|--------|---------|---------|
| **Perceivable** | Content can be perceived through multiple senses | Alt text, colour contrast, captions |
| **Operable** | All functionality works without a mouse | Keyboard nav, focus management, no time traps |
| **Understandable** | Content and UI behaviour are predictable | Consistent nav, clear errors, explicit labels |
| **Robust** | Works with current and future assistive technologies | Semantic HTML first; ARIA only when HTML is insufficient |

### Hard Requirements (Level AA)

| Requirement | Standard |
|-------------|---------|
| Colour contrast (text) | 4.5:1 minimum against background |
| Colour contrast (large text ≥ 18pt or 14pt bold) | 3:1 minimum |
| Colour contrast (UI components, focus rings) | 3:1 minimum |
| Keyboard navigation | All interactive elements reachable and operable via keyboard alone |
| Focus indicator | Visible `:focus-visible` ring on all interactive elements — never `outline: none` without replacement |
| Screen reader | Meaningful ARIA labels; correct semantic roles; `aria-live` regions for dynamic content |
| Focus not obscured | Focused element must not be entirely hidden by sticky headers or overlays (new in WCAG 2.2) |
| Dragging alternatives | Any drag-and-drop functionality has a single-pointer alternative (new in WCAG 2.2) |
| Target size | Interactive targets ≥ 24×24 CSS pixels (new in WCAG 2.2) |
| Motion | Respect `prefers-reduced-motion` — disable or significantly reduce animations when set |
| Colour alone | Colour is never the sole means of conveying information — use shape, label, or pattern as secondary encoding |

### Implementation Rules

- **Native HTML first**: `<button>`, `<a>`, `<input>` carry accessibility semantics for free. Use ARIA only when there is no native element for the role.
- **Focus trapping**: Components that manage focus (modals, dropdowns, tooltips) must trap focus within the component while open and return focus to the trigger element on close.
- **Functional images**: `alt` text describes the image's function, not appearance. Decorative images: `alt=""`.
- **Form errors**: `aria-describedby` links the input to its error message. Error summary at top of form focuses the first error field on submit.
