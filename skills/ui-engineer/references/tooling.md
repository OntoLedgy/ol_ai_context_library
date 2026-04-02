# UI Tooling

## Core Toolchain

Inherits all tooling from `javascript-data-engineer` (`references/tooling.md`).
The following additions apply specifically to UI work:

| Tool | Purpose | Config File |
|------|---------|------------|
| **Storybook** | Component development environment + living documentation | `.storybook/` |
| **React Testing Library** | Component behaviour tests (unit/integration) | `vitest.config.ts` |
| **Playwright** | End-to-end journey tests | `playwright.config.ts` |
| **eslint-plugin-jsx-a11y** | Accessibility linting | `eslint.config.mjs` |
| **eslint-plugin-react-hooks** | Hooks rules enforcement | `eslint.config.mjs` |
| **CSS Modules** | Scoped component styles | Built into Vite / Next.js |

---

## ESLint Configuration (UI additions)

```javascript
// eslint.config.mjs — add these plugins to the base config
import reactHooks from 'eslint-plugin-react-hooks';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import react from 'eslint-plugin-react';

export default [
  // ... base config from javascript-data-engineer
  {
    plugins: {
      'react-hooks': reactHooks,
      'jsx-a11y': jsxA11y,
      react,
    },
    rules: {
      // React hooks rules (mandatory)
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',

      // Accessibility (mandatory — UI components must be accessible)
      'jsx-a11y/alt-text': 'error',
      'jsx-a11y/aria-props': 'error',
      'jsx-a11y/aria-role': 'error',
      'jsx-a11y/interactive-supports-focus': 'error',
      'jsx-a11y/click-events-have-key-events': 'error',
      'jsx-a11y/no-noninteractive-element-interactions': 'error',

      // React best practices
      'react/jsx-key': 'error',
      'react/no-array-index-key': 'warn',
      'react/no-unstable-nested-components': 'error',
    },
  },
];
```

---

## Storybook Setup

### Directory Structure

```
.storybook/
  main.ts         Storybook configuration: addons, framework, stories glob
  preview.ts      Global decorators, parameters, design token injection
src/
  **/*.stories.tsx  Story files co-located with components
```

### `main.ts`

```typescript
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(ts|tsx)'],
  addons: [
    '@storybook/addon-essentials',   // Controls, actions, docs, viewport
    '@storybook/addon-a11y',          // Accessibility tab in Storybook UI
    '@storybook/addon-interactions',  // Interaction tests via play() functions
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
};
export default config;
```

### `preview.ts`

```typescript
import type { Preview } from '@storybook/react';
import '../src/styles/tokens.css';  // Inject design tokens globally

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },  // Auto-detect onXxx props as actions
    controls: { matchers: { date: /Date$/i } },
    a11y: { config: { rules: [{ id: 'color-contrast', enabled: true }] } },
    viewport: {
      defaultViewport: 'desktop',
    },
  },
};
export default preview;
```

---

## React Testing Library

### Testing Philosophy

Test **behaviour**, not **implementation**. A test should survive a refactor of internal
component structure as long as the user-visible behaviour is unchanged.

```typescript
// Test what the user sees and does — not component internals
describe('DocumentUploader', () => {
  it('shows an error when an oversized file is dropped', async () => {
    const user = userEvent.setup();
    render(
      <DocumentUploader
        acceptedTypes={['.pdf']}
        maxFileSizeBytes={1024}
        onFilesSelected={vi.fn()}
      />
    );

    const oversizedFile = new File(['x'.repeat(2048)], 'large.pdf', { type: 'application/pdf' });
    const dropZone = screen.getByRole('button', { name: /drop files/i });

    await user.upload(dropZone, oversizedFile);

    expect(screen.getByText(/exceeds.*1 KB/i)).toBeInTheDocument();
  });
});
```

### Test Coverage Requirements

| Context | Minimum Coverage |
|---------|-----------------|
| ol_ui_library components | 80% line coverage |
| Product feature components | 60% line coverage |
| Custom hooks | 80% line coverage |

### What to Test for Each Component

- **Happy path**: renders correctly with valid props
- **Loading state**: shows loading indicator when `isLoading={true}`
- **Error state**: shows error message with recovery action
- **Empty state**: shows empty state when data is empty array
- **User interactions**: click, keyboard, form submission
- **Accessibility**: run `axe` via `@axe-core/react` or `@testing-library/jest-axe`

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

it('has no accessibility violations', async () => {
  const { container } = render(<DocumentUploader {...defaultProps} />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Vitest Configuration (React)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      exclude: ['**/*.stories.tsx', '**/*.constants.ts', 'src/test/**'],
    },
  },
});
```

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

afterEach(() => cleanup());
```

---

## Playwright: End-to-End Journey Tests

### Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Journey Test Pattern

Test complete user journeys — not individual components:

```typescript
// e2e/document-upload-journey.spec.ts
import { test, expect } from '@playwright/test';

test('user can upload a document and see confirmation', async ({ page }) => {
  await page.goto('/upload');

  // Step 1: Select file
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.getByRole('button', { name: /browse files/i }).click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles('./e2e/fixtures/sample.pdf');

  // Step 2: Verify file appears in list
  await expect(page.getByText('sample.pdf')).toBeVisible();

  // Step 3: Submit upload
  await page.getByRole('button', { name: /upload/i }).click();

  // Step 4: Verify success state
  await expect(page.getByRole('heading', { name: /upload complete/i })).toBeVisible();
  await expect(page.getByText('1 file uploaded successfully')).toBeVisible();
});

test('shows an error when a file exceeds the size limit', async ({ page }) => {
  await page.goto('/upload');
  // ... test error path
});
```

### Journey Test Coverage

Write an end-to-end test for each named UX journey:
- Document Upload — happy path + oversized file error + wrong type error
- Pipeline Kick-Off Wizard — complete flow + step validation + abandon confirmation
- Pipeline Monitoring — status transitions + real-time log display
- Results Review — filter, sort, export

---

## Quality Gate Summary

```bash
# Type check
tsc --noEmit

# Lint (includes react, hooks, a11y)
eslint src/

# Format
prettier --check src/

# Unit + component tests
vitest run

# Coverage
vitest run --coverage

# End-to-end tests
playwright test

# Storybook build (catches story compilation errors)
storybook build --quiet
```

All gates must pass before a PR is raised.
