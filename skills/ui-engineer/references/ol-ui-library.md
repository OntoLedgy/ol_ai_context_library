# ol_ui_library: Usage and Contribution

## Core Principle

`ol_ui_library` is a platform library — the UI equivalent of `bclearer_pdk`. Before
implementing any UI component, **check if it already exists in the library**.

A custom component built alongside an existing library component is a violation.
Justify explicitly in the PR if you are not using an available library component.

---

## Component Catalogue

### Atoms

| Component | Props Summary | When to Use |
|-----------|--------------|-------------|
| `Button` | `intent`, `size`, `disabled`, `loading`, `onClick` | All interactive buttons |
| `Input` | `type`, `value`, `placeholder`, `error`, `disabled`, `onChange` | All text/number inputs |
| `Label` | `htmlFor`, `required` | All form field labels |
| `Icon` | `name`, `size`, `aria-hidden` | Decorative or semantic icons |
| `Badge` | `label`, `intent` | Status labels, counts |
| `Spinner` | `size`, `aria-label` | Loading states |
| `Avatar` | `src`, `alt`, `size`, `initials` | User identity display |
| `Tooltip` | `content`, `placement`, `children` | Contextual help on hover/focus |

### Molecules

| Component | Props Summary | When to Use |
|-----------|--------------|-------------|
| `FormField` | `label`, `error`, `required`, `children` | Wraps any input with label + error |
| `SearchBox` | `value`, `placeholder`, `onSearch`, `onClear` | Search inputs with clear control |
| `FileDropZone` | `acceptedTypes`, `maxSizeBytes`, `onFilesSelected` | File upload drop target |
| `ProgressBar` | `value` (0–100), `label`, `intent` | Upload progress, loading states |
| `Alert` | `intent`, `title`, `message`, `onDismiss` | Inline feedback messages |
| `Pagination` | `currentPage`, `totalPages`, `onPageChange` | Table and list pagination |

### Organisms

| Component | Props Summary | When to Use |
|-----------|--------------|-------------|
| `DataTable` | `columns`, `data`, `onSort`, `onFilter`, `isLoading` | All tabular data display |
| `NavigationBar` | `items`, `activeItem`, `onNavigate`, `user` | Application navigation |
| `DocumentUploader` | `acceptedTypes`, `maxSizeBytes`, `onUploadComplete` | File upload workflows |
| `ChartPanel` | `isLoading`, `error`, `title`, `children` | Chart container with states |
| `WizardContainer` | `steps`, `currentStep`, `onNext`, `onBack` | Multi-step form wrapper |

### Templates

| Component | Props Summary | When to Use |
|-----------|--------------|-------------|
| `DashboardTemplate` | `header`, `sidebar`, `main`, `footer` | Standard dashboard layout |
| `WizardTemplate` | `stepIndicator`, `stepContent`, `navigation` | Full wizard page layout |
| `ResultsTemplate` | `summary`, `explorer`, `visualisation` | Pipeline results layout |
| `EmptyStateTemplate` | `icon`, `title`, `description`, `action` | Empty/no-data states |

---

## Usage Patterns

### Correct: Using Library Components

```typescript
import { Button, FormField, Input } from '@ontoledgy/ol-ui-library';

function LoginForm({ onSubmit }: { onSubmit: (credentials: Credentials) => void }) {
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <FormField label="Email" required error={errors.email?.message}>
        <Input
          type="email"
          {...register('email', { required: 'Email is required' })}
        />
      </FormField>
      <Button type="submit" intent="primary" loading={isSubmitting}>
        Sign in
      </Button>
    </form>
  );
}
```

### Incorrect: Re-implementing a Library Component

```typescript
// VIOLATION: Button already exists in ol_ui_library
function PrimaryButton({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={onClick}>
      {label}
    </button>
  );
}
```

---

## Contributing to ol_ui_library

### When to Contribute

Contribute to `ol_ui_library` when:
- The same component pattern is needed in 2+ product features
- The component encapsulates accessibility logic that should not be duplicated
- The pattern is general enough to be useful across products

Do NOT contribute to the library when:
- The component is domain-specific (e.g. `PipelineStageCard`, `DocumentClassificationBadge`)
- The component depends on product-specific types or services

### Contribution Steps

**1. Get a design first**
Component contributions require an approved `ui-architect` Library Maintenance Mode
design before implementation begins. Never start coding a library component without
an approved spec.

**2. Implementation checklist**
- [ ] Props interface is `readonly` throughout
- [ ] No domain logic or service imports
- [ ] All states implemented: default, hover, focus, active, disabled, error, loading
- [ ] All variants implemented (size, intent, theme)
- [ ] CSS uses design tokens only — no hardcoded values
- [ ] WCAG 2.1 AA accessibility implemented (contrast, keyboard, ARIA)
- [ ] `prefers-reduced-motion` respected for animations

**3. Storybook story**
Every contribution requires a story file:

```typescript
// DocumentUploader.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { DocumentUploader } from './DocumentUploader';

const meta: Meta<typeof DocumentUploader> = {
  title: 'Organisms/DocumentUploader',
  component: DocumentUploader,
  parameters: { layout: 'padded' },
};
export default meta;
type Story = StoryObj<typeof DocumentUploader>;

export const Default: Story = {
  args: {
    acceptedTypes: ['.pdf', '.csv'],
    maxFileSizeBytes: 5 * 1024 * 1024,
  },
};

export const WithFilesSelected: Story = {
  args: { ...Default.args },
  play: async ({ canvasElement }) => {
    // Interaction test: simulate file selection
  },
};

export const Uploading: Story = {
  args: { ...Default.args, isUploading: true },
};

export const Disabled: Story = {
  args: { ...Default.args, disabled: true },
};
```

**4. Semver bump**
- New optional prop → `MINOR`
- New component → `MINOR`
- Renamed or removed prop → `MAJOR` (requires migration guide)
- Bug fix → `PATCH`

**5. Changelog entry**
Every contribution adds an entry to `CHANGELOG.md`:
```markdown
## [1.4.0] - 2026-04-02
### Added
- `DocumentUploader` organism: file drop zone with multi-file support, per-file progress,
  and validation. Supports drag-drop and browser file picker. WCAG 2.1 AA compliant.
```

---

## Design Token Usage in Components

```typescript
// Correct: reference tokens via CSS custom properties
// In DocumentUploader.module.css:
.dropZone {
  border: 2px dashed var(--color-neutral-300);
  border-radius: var(--radius-md);
  padding: var(--space-8);
  background: var(--color-neutral-50);
}

.dropZone:focus-within,
.dragOver {
  border-color: var(--color-brand-primary);
  background: var(--color-brand-50);
  outline: none;
  box-shadow: 0 0 0 3px var(--shadow-focus);
}
```

```typescript
// Incorrect: hardcoded values
.dropZone {
  border: 2px dashed #d1d5db;  // VIOLATION: use var(--color-neutral-300)
  padding: 32px;               // VIOLATION: use var(--space-8)
}
```
