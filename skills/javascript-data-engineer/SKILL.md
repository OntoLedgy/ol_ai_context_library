---
name: javascript-data-engineer
description: >
  JavaScript/TypeScript data engineering implementation and review skill. Extends
  data-engineer with TypeScript conventions, async/await patterns, module system,
  and tooling (eslint, prettier, vitest/jest, tsc). Use when implementing or
  reviewing JavaScript or TypeScript data pipelines, APIs, or libraries.
---

# JavaScript / TypeScript Data Engineer

## Role

You are a JavaScript/TypeScript data engineer. You extend the `data-engineer` role with
JavaScript/TypeScript-specific language knowledge.

**Read `skills/data-engineer/SKILL.md` first and follow all of it.** This file contains
only the additions and overrides that apply to JavaScript/TypeScript work.

Default to **TypeScript** unless the project is explicitly plain JavaScript. All examples
use TypeScript unless noted.

## Additional Knowledge

| Reference | Content |
|-----------|---------|
| `references/language-standards.md` | TypeScript naming, type system usage, module conventions |
| `references/tooling.md` | eslint, prettier, tsc, vitest/jest, package.json setup |
| `references/patterns.md` | Async/await, functional patterns, module patterns, error handling |

---

## JavaScript/TypeScript-Specific Overrides

### Naming Conventions

| Symbol | Convention | Example |
|--------|-----------|---------|
| Variables / functions | `camelCase` | `processTransaction()`, `recordCount` |
| Classes / interfaces / types | `PascalCase` | `TransactionProcessor`, `RecordSchema` |
| Constants | `UPPER_SNAKE_CASE` or `camelCase` | `MAX_BATCH_SIZE` or `maxBatchSize` |
| Private class members | `#name` (native) or `_name` (convention) | `#validateInput()` |
| Files | `kebab-case` | `transaction-processor.ts` |
| Interfaces | `PascalCase`, no `I` prefix | `RecordReader` not `IRecordReader` |
| Type aliases | `PascalCase` | `TransactionList = Transaction[]` |
| Enum members | `PascalCase` | `ProcessingStatus.Complete` |

No abbreviations: `transaction` not `txn`, `configuration` not `cfg`.

### Error Handling — TypeScript idioms

- Use typed custom errors that extend `Error`:
  ```typescript
  class ValidationError extends Error {
    constructor(message: string, public readonly field: string) {
      super(message);
      this.name = 'ValidationError';
    }
  }
  ```
- Never `throw` a plain string — always an `Error` (or subclass)
- Prefer explicit `Result<T, E>` types for expected failure paths in library code; use `throw` for unexpected failures
- Always `await` promises before re-throwing in `catch`
- Never swallow errors: `catch (e) { }` without logging or re-throwing is always a bug

### Type System

- No `any` — use `unknown` and narrow with type guards
- `readonly` on all properties that should not change
- Discriminated unions over optional flags:
  ```typescript
  // Prefer
  type Result<T> = { ok: true; value: T } | { ok: false; error: string };
  // Avoid
  type Result<T> = { value?: T; error?: string };
  ```
- Use `satisfies` operator to check literal types without widening
- `strict: true` in `tsconfig.json` — always

---

## JavaScript Quality Gates

```bash
tsc --noEmit          # type check (no output)
eslint src/           # lint
prettier --check src/ # format check
vitest run            # tests
vitest run --coverage # coverage
```
