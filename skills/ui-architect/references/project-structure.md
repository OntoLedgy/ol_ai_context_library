# Frontend Project Structure

## Naming Convention: `frontend/`

Use **`frontend/`** as the canonical name for the UI layer in every project.

| Name | Status | Reason |
|------|--------|--------|
| `frontend/` | **Canonical** | Clear, unambiguous, consistent across all OL projects |
| `ui/` | **Forbidden** | Ambiguous — conflicts with `ol_ui_library`; also used for UI component directories |
| `client/` | Forbidden | Implies client/server split as the primary concern; unclear in monorepo contexts |
| `web/` | Forbidden | Too narrow — assumes web-only; excludes desktop/mobile targets |
| `app/` | Forbidden | Collides with the `app/` directory used inside the frontend source |

This applies at every level: top-level project folders, CI/CD config paths, Docker compose
service names, import alias roots, and README references.

---

## Structure 1: Product Application (uses `ol_ui_library`)

For any product built on top of `ol_ui_library`. Uses Feature-Sliced Design adapted for the
OL platform.

```
my-product/
  frontend/
    src/
      app/                      Application bootstrap — runs once at startup
        providers.tsx           React Query, theme, auth, error boundary providers
        router.tsx              Route definitions (React Router / TanStack Router)
        App.tsx                 Root component: wraps providers around router
        main.tsx                Entry point: renders App into the DOM
      pages/                    Route-level thin shells — one file per route
        dashboard/
          DashboardPage.tsx
        upload/
          UploadPage.tsx
        pipeline/
          PipelineDetailPage.tsx
      features/                 User-facing business capabilities
        document-upload/
          DocumentUploadFeature.tsx     Orchestrates the upload journey
          useDocumentUpload.ts          Upload logic: validation, API calls, state
          documentUpload.constants.ts   Accepted types, size limits, copy strings
          documentUpload.types.ts       Feature-local types
        pipeline-wizard/
          PipelineWizardFeature.tsx
          usePipelineWizard.ts
          pipelineWizard.constants.ts
          pipelineWizard.types.ts
        pipeline-monitoring/
          PipelineMonitoringFeature.tsx
          usePipelineMonitoring.ts
          usePipelineLogStream.ts
        results-review/
          ResultsReviewFeature.tsx
          useResultsFilter.ts
      entities/                 Business domain entities — shared across features
        document/
          document.types.ts           TypeScript types for the Document entity
          document.api.ts             React Query query/mutation definitions
          DocumentSummaryCard.tsx     Entity-level presentational component
        pipeline/
          pipeline.types.ts
          pipeline.api.ts
          PipelineStatusBadge.tsx
        result/
          result.types.ts
          result.api.ts
      shared/                   Cross-cutting — no feature-specific code here
        ui/                     Local component compositions (thin; prefer ol_ui_library direct)
        hooks/                  Truly shared hooks used by 2+ features
          useDebounce.ts
          usePageTitle.ts
        api/                    API client setup, interceptors, base URL, auth headers
          client.ts
          queryClient.ts
        utils/                  Pure functions: formatters, validators, date helpers
          formatBytes.ts
          formatDate.ts
        constants/              App-wide constants (route paths, feature flags)
          routes.ts
          config.ts
        types/                  Shared TypeScript types used across layers
          api.types.ts
          pagination.types.ts
    public/                     Static assets: favicon.ico, og-image.png, robots.txt
    e2e/                        Playwright end-to-end journey tests
      fixtures/                 Static test data files (sample.pdf, test.csv)
      journeys/                 Journey test specs named after the journey
        document-upload.spec.ts
        pipeline-wizard.spec.ts
        pipeline-monitoring.spec.ts
    .storybook/                 Only if the product team builds product-specific stories
    index.html
    package.json
    tsconfig.json
    vite.config.ts
    vitest.config.ts
    playwright.config.ts
  backend/
  docs/
```

### Layer Import Rules (strictly enforced)

Each layer may only import from layers below it in this list:

```
pages       → features, entities, shared
features    → entities, shared
entities    → shared
shared      → (external packages only; no internal cross-imports)
app         → pages, shared
```

`features` never import from other `features`.
`entities` never import from `features`.

### Path Aliases (`tsconfig.json`)

```json
{
  "compilerOptions": {
    "paths": {
      "@/*":     ["./src/*"],
      "@olui/*": ["../../ol_ui_library/src/*"]
    }
  }
}
```

Use `@/features/document-upload/...` not `../../../features/document-upload/...`.
Use `@olui/atoms/Button` not `ol-ui-library/src/atoms/Button`.

---

## Structure 2: `ol_ui_library` Itself

For work on the shared component library. Uses Atomic Design with strict co-location.

```
ol_ui_library/
  src/
    atoms/                     Level 1 — smallest indivisible elements
      Button/
        Button.tsx
        Button.test.tsx
        Button.stories.tsx
        Button.module.css
        index.ts               Public export: export { Button } from './Button'
      Input/
      Label/
      Icon/
      Badge/
      Spinner/
      Avatar/
      Tooltip/
    molecules/                 Level 2 — functional combinations of atoms
      FormField/
        FormField.tsx
        FormField.test.tsx
        FormField.stories.tsx
        FormField.module.css
        index.ts
      FileDropZone/
      ProgressBar/
      SearchBox/
      Alert/
      Pagination/
    organisms/                 Level 3 — complex compositions of molecules and atoms
      DataTable/
        DataTable.tsx
        DataTable.test.tsx
        DataTable.stories.tsx
        DataTable.module.css
        useDataTable.ts        Co-located hook (used only by DataTable)
        dataTable.constants.ts
        index.ts
      DocumentUploader/
      NavigationBar/
      ChartPanel/
      WizardContainer/
    templates/                 Level 4 — structural page layouts; no data, no domain logic
      DashboardTemplate/
        DashboardTemplate.tsx
        DashboardTemplate.stories.tsx
        DashboardTemplate.module.css
        index.ts
      WizardTemplate/
      ResultsTemplate/
      EmptyStateTemplate/
    tokens/                    Design tokens — the visual vocabulary of the library
      colours.css              --color-brand-primary, --color-status-error, etc.
      spacing.css              --space-1 through --space-16
      typography.css           --font-size-sm, --font-weight-semibold, etc.
      borders.css              --radius-sm, --radius-md, --radius-full
      shadows.css              --shadow-sm, --shadow-md, --shadow-focus
      z-index.css              --z-modal, --z-tooltip, --z-dropdown
      tokens.css               Master file: @import all token files above
    hooks/                     Shared hooks exported by the library
      useDebounce.ts
      useMediaQuery.ts
      useLocalStorage.ts
      usePrevious.ts
    types/                     TypeScript types exported by the library
      component.types.ts       Base prop types: Size, Intent, etc.
      token.types.ts
    utils/                     Pure utility functions exported by the library
      formatBytes.ts
      formatDuration.ts
      accessibility.ts         Shared ARIA helpers
    index.ts                   Library barrel export — the public API of the library
  .storybook/
    main.ts
    preview.ts                 Injects tokens.css; global decorators
  e2e/                         Playwright tests for complex multi-step component interactions
  package.json
  tsconfig.json
  vite.config.ts               Also the Storybook build target
  vitest.config.ts
```

### Component Folder Rule

Every component in `ol_ui_library` lives in its own folder with exactly these files:

| File | Required | Purpose |
|------|----------|---------|
| `ComponentName.tsx` | Yes | Implementation |
| `ComponentName.test.tsx` | Yes | React Testing Library tests |
| `ComponentName.stories.tsx` | Yes | Storybook stories |
| `ComponentName.module.css` | Yes | Scoped styles (tokens only — no hardcoded values) |
| `index.ts` | Yes | `export { ComponentName } from './ComponentName'` |
| `useComponentName.ts` | If needed | Co-located hook — only if used by this component alone |
| `componentName.constants.ts` | If needed | Constants specific to this component |

Never add a component file without all required files. A component without tests or stories
is not complete.

---

## File Naming Conventions

Consistent across both product applications and `ol_ui_library`:

| File Type | Convention | Example |
|-----------|-----------|---------|
| React component | `PascalCase.tsx` | `DocumentUploader.tsx` |
| Custom hook | `camelCase.ts` (must start `use`) | `useDocumentUpload.ts` |
| Types file | `camelCase.types.ts` | `document.types.ts` |
| API module | `camelCase.api.ts` | `document.api.ts` |
| Constants | `camelCase.constants.ts` | `documentUpload.constants.ts` |
| CSS Module | `PascalCase.module.css` (matches component) | `DocumentUploader.module.css` |
| Unit test | `PascalCase.test.tsx` / `camelCase.test.ts` | `DocumentUploader.test.tsx` |
| Story file | `PascalCase.stories.tsx` | `DocumentUploader.stories.tsx` |
| Barrel export | `index.ts` | `atoms/Button/index.ts` |
| Playwright spec | `kebab-case.spec.ts` (named after journey) | `document-upload.spec.ts` |
| **Folder names** | `kebab-case` | `document-upload/`, `pipeline-wizard/` |

No abbreviations: `document-upload/` not `doc-upload/`, `pipeline-wizard/` not `pipe-wiz/`.

---

## What Goes Where: Decision Table

| Code | Location |
|------|----------|
| Button, Input, Label | `ol_ui_library/src/atoms/` |
| FormField, ProgressBar, FileDropZone | `ol_ui_library/src/molecules/` |
| DataTable, DocumentUploader, NavigationBar | `ol_ui_library/src/organisms/` |
| DashboardTemplate, WizardTemplate | `ol_ui_library/src/templates/` |
| Design tokens (colour, spacing, typography) | `ol_ui_library/src/tokens/` |
| Upload journey orchestration | `frontend/src/features/document-upload/` |
| Pipeline API calls and query keys | `frontend/src/entities/pipeline/pipeline.api.ts` |
| Pipeline TypeScript types | `frontend/src/entities/pipeline/pipeline.types.ts` |
| PipelineStatusBadge (entity-level presentation) | `frontend/src/entities/pipeline/` |
| Route definitions | `frontend/src/app/router.tsx` |
| Auth/React Query providers | `frontend/src/app/providers.tsx` |
| Format utility used by 2+ features | `frontend/src/shared/utils/` |
| Format utility used only by one component | Co-locate in the component's folder |
| App-wide constants (routes, env config) | `frontend/src/shared/constants/` |
| Domain-specific constants (file size limits) | `frontend/src/features/document-upload/documentUpload.constants.ts` |

**Rule of thumb**: If in doubt about placement, ask "which layer is this responsible to?"
A component that knows about `Pipeline` domain types belongs in `entities`; a component
that orchestrates the pipeline kick-off journey belongs in `features`.
