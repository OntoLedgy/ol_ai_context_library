# JavaScript / TypeScript Tooling

---

## Standard Toolchain

| Tool | Purpose | Config |
|------|---------|--------|
| `tsc` | Type checking | `tsconfig.json` |
| `eslint` | Linting | `eslint.config.ts` (flat config) |
| `prettier` | Formatting | `.prettierrc` |
| `vitest` | Test runner (preferred) | `vitest.config.ts` |
| `jest` | Test runner (legacy / React) | `jest.config.ts` |
| `@vitest/coverage-v8` | Coverage | via `vitest.config.ts` |

---

## tsconfig.json (strict baseline)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

---

## eslint.config.ts (flat config)

```typescript
import typescript from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';

export default [
  {
    files: ['src/**/*.ts'],
    plugins: { '@typescript-eslint': typescript },
    languageOptions: { parser: tsParser },
    rules: {
      ...typescript.configs['strict-type-checked'].rules,
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/no-explicit-any': 'error',
    },
  },
];
```

---

## .prettierrc

```json
{
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "semi": true
}
```

---

## vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: false,
    coverage: {
      provider: 'v8',
      thresholds: { lines: 80, functions: 80 },
      include: ['src/**'],
      exclude: ['src/**/*.d.ts'],
    },
  },
});
```

---

## Quality Gates

```bash
tsc --noEmit              # type check
eslint src/               # lint
prettier --check src/     # format check
vitest run                # tests
vitest run --coverage     # with coverage
```

Auto-fix:
```bash
eslint --fix src/
prettier --write src/
```

---

## Test Structure

```
src/
└── transaction-processor.ts
tests/
├── unit/
│   └── transaction-processor.test.ts
└── integration/
    └── pipeline.test.ts
```

Vitest test example:
```typescript
import { describe, it, expect, vi } from 'vitest';
import { TransactionProcessor } from '../src/transaction-processor';

describe('TransactionProcessor', () => {
  it('processes valid records and writes results', async () => {
    const reader = { read: vi.fn().mockResolvedValue([mockRecord]) };
    const writer = { write: vi.fn().mockResolvedValue(undefined) };
    const processor = new TransactionProcessor(reader, writer);

    await processor.process();

    expect(writer.write).toHaveBeenCalledWith([expectedResult]);
  });
});
```
