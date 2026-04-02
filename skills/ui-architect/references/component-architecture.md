# Component Architecture Patterns

## Pattern Selection Guide

Choose one pattern per application before design begins. Do not mix patterns.

---

## Atomic Design

**Best for**: Building or extending a component library (ol_ui_library); ensuring a
consistent visual vocabulary across multiple products.

**Structure** (Brad Frost — industry standard for component libraries):

| Level | Description | Examples |
|-------|-------------|---------|
| **Atoms** | Smallest indivisible UI elements | Button, Input, Label, Icon, Badge, Spinner |
| **Molecules** | Combinations of atoms that form a functional unit | FormField (Label + Input + Error), SearchBox (Input + Button) |
| **Organisms** | Complex components composed of molecules and atoms | NavigationBar, DataTable, DocumentUploader, ChartPanel |
| **Templates** | Page-level wire-frame compositions of organisms | DashboardTemplate, WizardTemplate, ResultsTemplate |
| **Pages** | Templates with real data bound | DashboardPage, UploadPage |

**Key rules**:
- Each level depends only on levels below it — organisms use molecules; molecules use atoms
- Pages are never used inside organisms
- Templates contain no domain data — they are structural layouts only
- Atoms have no internal state — they are pure presentation

**When to choose Atomic Design**:
- You are designing or improving ol_ui_library itself
- The product needs a consistent visual language across many features
- The team will share components across multiple applications

---

## Feature-Sliced Design

**Best for**: Large applications with multiple distinct business domains where teams need
to own features independently without coupling.

**Structure**:

```
src/
  app/          Application-level setup: providers, routing, global styles
  pages/        Route-level compositions (thin — delegate to widgets)
  widgets/      Self-contained page blocks specific to a single page
  features/     User scenarios and business capabilities
  entities/     Business entities: User, Document, Pipeline
  shared/       Cross-cutting: UI kit (≈ ol_ui_library atoms/molecules), API client, utilities
```

**Import rule (strictly enforced)**: Each layer may only import from layers listed below it.
`features` know about `entities`; `entities` never import from `features`.

**Key rules**:
- `shared/ui` is effectively the component library layer — reference ol_ui_library here
- `entities` contain domain types, API schemas, and entity-level components
- `features` contain the orchestration logic for user-facing capabilities
- `widgets` are assemblers — they compose features and entities for a specific page context

**When to choose Feature-Sliced Design**:
- 3+ distinct business domains in a single application
- Multiple teams contributing independently
- You need to enforce clear import discipline to prevent cross-feature coupling

---

## Smart / Dumb (Container / Presenter)

**Best for**: Small to medium applications where simplicity and testability of presentation
logic are the primary goals.

| Component Type | Responsibility | Has State | Knows About API/Services |
|----------------|---------------|-----------|--------------------------|
| **Smart (Container)** | Fetches data, manages state, coordinates children | Yes | Yes |
| **Dumb (Presenter)** | Renders props; emits events via callbacks; no side effects | No | No |

**Key rules**:
- Dumb components are tested in isolation with props alone — no mocks needed
- Smart components are integration-tested
- Each dumb component has a clearly defined props interface
- Smart components do not render UI directly — they compose dumb components

**When to choose Smart/Dumb**:
- Single team, small to medium codebase
- Clear unidirectional data flow is the primary architectural goal
- You want maximum component testability with minimal test infrastructure

---

## State Management Selection

Separate server state from client state. Do not force one library to handle both.

| Solution | Use When | Avoid When |
|----------|----------|------------|
| **React Query / TanStack Query** | Server state: API data, caching, background refresh | Local UI state — this is not its purpose |
| **React Context + useReducer** | Shared state within a single feature tree; < 5 consumers; infrequent updates | High-frequency updates (triggers full re-renders across all consumers) |
| **Zustand** | App-wide client state; moderate update frequency; simple API preferred | You need strict Redux-style patterns with middleware |
| **Redux Toolkit** | Large team; strict patterns required; complex async flows with middleware | Small app — adds ceremony without benefit |
| **Jotai** | Complex interdependent state; fine-grained reactivity per atom | Team unfamiliar with atomic state model |
| **`useState` / `useReducer`** | Component-local state: open/closed, current tab, form input | State needed by sibling or distant components |

**Decision principle**: Use React Query for anything that comes from a server. Use Zustand
(or Context for small scope) for everything else. Never put API response data in Zustand.

---

## Module Federation (Micro-Frontends)

Use only when teams need to deploy UI slices independently. This is an advanced pattern
with significant operational overhead — do not default to it.

**Rules when used**:
- Split by **business domain**, not technical layer (not "all charts", but "reporting feature")
- Share `react` and `react-dom` as singletons — never allow multiple React versions to coexist
- Use CSS Modules or Shadow DOM to prevent style leakage across slices
- Do not share utility libraries across micro-frontend boundaries — controlled duplication is
  cheaper than shared-library coupling
- Prefer Server-Side Module Federation for SSR scenarios

**Avoid micro-frontends when**: A monorepo with a shared component library (ol_ui_library)
achieves the same independence goal at significantly lower complexity.
