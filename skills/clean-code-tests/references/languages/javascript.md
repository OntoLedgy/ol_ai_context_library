# Clean Code Tests — JavaScript / TypeScript

Language-specific testing patterns for JavaScript and TypeScript.
Read alongside `references/testing-philosophy.md` and `references/testing-standards.md`.

---

## Framework and Tooling

| Tool | Purpose |
|------|---------|
| `vitest` | Preferred test runner (fast, ESM-native, Vite-integrated) |
| `jest` | Alternative runner (CommonJS projects, existing jest setups) |
| `@testing-library/react` | React component testing |
| `@testing-library/user-event` | Simulating user interactions |
| `vi.fn()` / `jest.fn()` | Mock functions |
| `msw` | Mock Service Worker — intercept HTTP at network level |

---

## File and Class Structure

```typescript
// tests/unit/module/component.test.ts

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { ComponentName } from '../../../src/module/component';

describe('ComponentName', () => {
  let component: ComponentName;

  beforeEach(() => {
    component = new ComponentName();
  });

  describe('process', () => {
    it('returns expected output for valid input', () => {
      // Arrange
      const input = { key: 'value' };
      const expected = { processed: true, key: 'value' };

      // Act
      const result = component.process(input);

      // Assert
      expect(result).toEqual(expected);
      expect(result.processed).toBe(true);
    });

    it('throws TypeError when input is null', () => {
      expect(() => component.process(null)).toThrow(
        new TypeError('Input cannot be null'),
      );
    });
  });
});
```

Rules:
- Use `describe` to group by class/function, nested `describe` for method
- Use `it` (not `test`) for individual cases — reads as a sentence
- `beforeEach` / `afterEach` for setup and teardown
- `beforeAll` / `afterAll` only for truly expensive shared resources (DB connections)

---

## Naming

| Unit | Pattern | Example |
|------|---------|---------|
| Outer `describe` | component or module name | `describe('TransactionLoader', ...)` |
| Inner `describe` | method or function name | `describe('load', ...)` |
| `it` / `test` | reads as sentence | `it('throws FileNotFoundError when path is missing', ...)` |

Full sentence when combined: `TransactionLoader > load > throws FileNotFoundError when path is missing`

---

## Mocking

### `vi.fn()` — mock a function

```typescript
it('calls the formatter with the raw record', () => {
  // Arrange
  const mockFormatter = vi.fn().mockReturnValue({ formatted: true });
  const loader = new TransactionLoader({ formatter: mockFormatter });

  // Act
  loader.load(rawRecord);

  // Assert
  expect(mockFormatter).toHaveBeenCalledOnce();
  expect(mockFormatter).toHaveBeenCalledWith(rawRecord);
});
```

### `vi.spyOn()` — spy on an existing method

```typescript
it('logs an error when processing fails', () => {
  const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

  component.process(invalidInput);

  expect(errorSpy).toHaveBeenCalledWith(expect.stringContaining('processing failed'));
  errorSpy.mockRestore();
});
```

### Module mocking

```typescript
vi.mock('../../../src/services/apiClient', () => ({
  fetchRecord: vi.fn().mockResolvedValue({ id: '1', amount: 100 }),
}));

import { fetchRecord } from '../../../src/services/apiClient';

it('loads a record from the API', async () => {
  const result = await loadRecord('1');
  expect(fetchRecord).toHaveBeenCalledWith('1');
  expect(result.amount).toBe(100);
});
```

---

## Error Path Testing

```typescript
it('throws RecordNotFoundError when record does not exist', () => {
  expect(() => service.find('missing-id')).toThrow(RecordNotFoundError);
  expect(() => service.find('missing-id')).toThrow('Record not found: id=missing-id');
});

it('rejects with NetworkError when API is unreachable', async () => {
  mockFetch.mockRejectedValue(new NetworkError('timeout'));
  await expect(service.fetchRemote('id')).rejects.toThrow(NetworkError);
});
```

---

## Parametrised Tests (`test.each`)

```typescript
it.each([
  ['hello', 'HELLO'],
  ['world', 'WORLD'],
  ['',      ''     ],
])('transform("%s") returns "%s"', (input, expected) => {
  expect(component.transform(input)).toBe(expected);
});

// Object form — preferred for readability
it.each([
  { path: '../etc/passwd', expectedError: 'path traversal' },
  { path: '/absolute',     expectedError: 'absolute path'  },
])('load rejects unsafe path "$path"', ({ path, expectedError }) => {
  expect(() => loader.load(path)).toThrow(expectedError);
});
```

---

## Async Tests

```typescript
it('fetches a record successfully', async () => {
  // Arrange
  mockApiClient.get.mockResolvedValue({ id: '1', amount: 100 });

  // Act
  const result = await service.fetchRecord('1');

  // Assert
  expect(result.amount).toBe(100);
});

it('throws on API timeout', async () => {
  mockApiClient.get.mockRejectedValue(new Error('Request timed out'));
  await expect(service.fetchRecord('1')).rejects.toThrow('Request timed out');
});
```

---

## React Component Testing

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TransactionList } from '../../../src/components/TransactionList';

describe('TransactionList', () => {
  it('renders all transactions', () => {
    // Arrange
    const transactions = [
      { id: '1', amount: 100, label: 'Coffee' },
      { id: '2', amount: 250, label: 'Lunch'  },
    ];

    // Act
    render(<TransactionList transactions={transactions} />);

    // Assert
    expect(screen.getByText('Coffee')).toBeInTheDocument();
    expect(screen.getByText('Lunch')).toBeInTheDocument();
  });

  it('calls onDelete with the correct id when delete button is clicked', async () => {
    // Arrange
    const onDelete = vi.fn();
    const transactions = [{ id: '1', amount: 100, label: 'Coffee' }];
    render(<TransactionList transactions={transactions} onDelete={onDelete} />);

    // Act
    await userEvent.click(screen.getByRole('button', { name: /delete/i }));

    // Assert
    expect(onDelete).toHaveBeenCalledWith('1');
  });

  it('displays empty state when no transactions provided', () => {
    render(<TransactionList transactions={[]} />);
    expect(screen.getByText('No transactions')).toBeInTheDocument();
  });
});
```

Rules:
- Query by role or label text, not by CSS class or test ID unless unavoidable
- `userEvent` over `fireEvent` — simulates real browser interactions
- Never test implementation details (internal state, private methods)
- Test what the user sees and does, not how the component is built

---

## TypeScript Specific

```typescript
// Type assertions in tests — use satisfies or as, not any
const result = component.process(input) satisfies ProcessedRecord;

// Typed mock return values
const mockService = {
  fetch: vi.fn<[string], Promise<Record>>().mockResolvedValue(testRecord),
};

// Never use any in test files — use unknown with narrowing or explicit types
const rawResponse: unknown = await apiClient.get('/endpoint');
expect(rawResponse).toMatchObject({ status: 'ok' });
```

---

## vitest Configuration Reference

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',         // or 'jsdom' for DOM/React tests
    include: ['tests/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      thresholds: { lines: 80, branches: 75 },
    },
  },
});
```
