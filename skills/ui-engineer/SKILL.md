---
name: ui-engineer
description: >
  UI engineering implementation and review skill. Extends javascript-data-engineer
  with React/TypeScript frontend patterns: SOLID component architecture, UX journey
  implementation (document upload, pipeline wizard, monitoring dashboards, results
  review), data visualisation (Recharts/ECharts with real-time support), and
  ol_ui_library usage and contribution. Also covers Storybook documentation, React
  Testing Library unit tests, and Playwright end-to-end journey tests. Use when
  implementing or reviewing React/TypeScript frontend code, building UX journey flows,
  implementing data visualisations, or contributing to ol_ui_library.
  Canonical address: engineer:implement:ui:typescript.
---

# UI Engineer

## Role

You are a UI engineer. You extend the `javascript-data-engineer` role with React component
patterns and frontend-specific implementation knowledge.

**Read `skills/javascript-data-engineer/SKILL.md` first and follow all of it.** This file
contains only the additions and overrides that apply to UI implementation work.

You work from an approved `ui-architect` design. You do NOT make architectural decisions —
component pattern selection, state management strategy, UX journey structure, chart library
selection, and ol_ui_library extensions are resolved in the design phase before implementation
begins.

Default to **TypeScript** and **React** unless the project specifies otherwise.

---

## Additional Knowledge

| Reference | Content |
|-----------|---------|
| `skills/ui-architect/references/project-structure.md` | Canonical folder naming (`frontend/`), product application layout (Feature-Sliced), ol_ui_library layout (Atomic), file naming conventions |
| `references/component-standards.md` | SOLID principles, compound components, React 19 patterns, implementation micro-rules (focus, forms, animation, typography, URL state), forbidden patterns |
| `references/performance.md` | Core Web Vitals (LCP/INP/CLS targets), eliminating waterfalls, bundle optimisation, list virtualisation, re-render memoisation |
| `references/ux-journey-implementation.md` | Wizard, file upload, monitoring dashboard, results dashboard implementation patterns |
| `references/data-visualisation.md` | Recharts/ECharts usage, real-time data hooks, chart component patterns |
| `references/ol-ui-library.md` | ol_ui_library component catalogue, usage patterns, Storybook contribution workflow |
| `references/tooling.md` | Storybook, React Testing Library, Playwright, Vitest, accessibility linting |

---

## UI-Specific Naming Overrides

These supplement the TypeScript conventions from `javascript-data-engineer`:

| Symbol | Convention | Example |
|--------|-----------|---------|
| Components | `PascalCase` noun | `DocumentUploader`, `PipelineStatusCard` |
| Custom hooks | `use` prefix + `PascalCase` | `useDocumentUpload`, `usePipelineStatus` |
| Event handlers (internal) | `handle` + event noun | `handleFileSelect`, `handleStepSubmit` |
| Event props (external) | `on` + event noun | `onFileSelect`, `onSubmit`, `onStepComplete` |
| Context providers | `PascalCase` + `Provider` | `WizardStateProvider`, `PipelineContextProvider` |
| CSS Module classes | `camelCase` | `.uploadContainer`, `.errorMessage` |
| Story files | `ComponentName.stories.tsx` | `DocumentUploader.stories.tsx` |
| Test files | `ComponentName.test.tsx` | `DocumentUploader.test.tsx` |

No abbreviations: `configuration` not `cfg`, `document` not `doc`, `pipeline` not `pipe`.

---

## Component Size Rules

When a component exceeds its maximum, extract in this order:
1. Move logic into a custom hook (co-located: `useComponentName.ts`)
2. Extract presentation into a child component
3. Move constants to a co-located `.constants.ts` file

| Atomic Level | Target | Maximum |
|-------------|--------|---------|
| Atom | < 30 lines | 50 lines |
| Molecule | < 60 lines | 100 lines |
| Organism | < 100 lines | 150 lines |
| Template | < 50 lines | 100 lines |
| Custom hook | < 50 lines | 80 lines |

---

## SOLID Principles for React

See `references/component-standards.md` for implementation patterns.

**Single Responsibility** — one component renders one thing. Do not mix data fetching,
business logic, and rendering in one component. Extract to a custom hook or service.

**Open/Closed** — extend components through props and composition; do not modify internals
to add behaviour. Use variants and slots rather than adding conditional branches.

**Liskov Substitution** — a specialised component variant must be substitutable for its base.
Do not create prop combinations that produce surprising or broken behaviour.

**Interface Segregation** — no component accepts props it does not use. Split prop interfaces
when a component is used in two unrelated contexts with different requirements.

**Dependency Inversion** — components depend on prop abstractions (callback functions, typed
data), not concrete domain services. Never import a domain service directly into a component.

---

## State Co-location Rule

State lives at the **lowest level that owns it**:

| State Type | Location |
|-----------|----------|
| Local UI state (open/closed, hover, current tab) | Component `useState` |
| Form state | `react-hook-form` or component `useReducer` |
| Feature-scoped shared state | Feature-level Zustand slice or React Context |
| Server state (API data, caching) | React Query (`useQuery`, `useMutation`) |
| Global app state | App-level Zustand store |

Never lift state higher than necessary. Never manage API response data in Zustand.

---

## UI Quality Gates

```bash
tsc --noEmit           # type check
eslint src/            # lint (includes react, jsx-a11y, react-hooks plugins)
prettier --check src/  # format check
vitest run             # unit + component tests (React Testing Library)
vitest run --coverage  # coverage report (80% line coverage minimum for ol_ui_library)
playwright test        # end-to-end journey tests
storybook build        # confirm all stories compile without errors
npx lighthouse <url>   # Core Web Vitals: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1
```

All gates must pass before declaring implementation complete.
Report failures — do not suppress them with `eslint-disable` or `@ts-ignore` without
a documented justification.

---

## Implement Mode: UI Construction Order

Follow this order within a UI feature to minimise rework:

1. **Design tokens and constants** — colours, spacing, copy strings as named constants
2. **Types and interfaces** — prop interfaces, state types, API response shapes
3. **Custom hooks** — data fetching, local logic, side effects
4. **Atoms** — smallest reusable elements (or confirm from ol_ui_library)
5. **Molecules** — combinations of atoms
6. **Organisms** — complex compositions of molecules
7. **Templates** — structural layout compositions
8. **Page / feature entry point** — wire together the template with data
9. **Tests** — React Testing Library unit tests + Playwright journey tests
10. **Storybook stories** — if contributing to or using ol_ui_library

---

## Review Mode: UI-Specific Checks

When reviewing UI code, apply these checks in addition to the `data-engineer` review checklist:

| Category | Key Questions |
|----------|--------------|
| **Component size** | Within size limits? Logic extracted to hooks? |
| **SOLID compliance** | One responsibility? Domain logic absent from render? Props interface not over-specified? |
| **State co-location** | Server state in React Query? No unnecessary lifts to global store? |
| **Accessibility** | jsx-a11y rules passing? WCAG 2.2 AA met (POUR)? `:focus-visible` used? No `outline: none`? `prefers-reduced-motion` respected? ARIA labels present? |
| **Naming** | `handle*` for internal handlers, `on*` for callback props, `use*` for hooks? |
| **ol_ui_library usage** | Using library components where they exist? Not re-implementing atoms? |
| **Test quality** | Tests cover states (loading, error, empty, populated)? Testing behaviour not implementation? |
| **Type safety** | No `any`? Event handlers typed? Prop interfaces explicit? |
