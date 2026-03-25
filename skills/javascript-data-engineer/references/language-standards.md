# JavaScript / TypeScript Language Standards

---

## Naming

| Symbol | Convention | Example |
|--------|-----------|---------|
| Variables / functions | `camelCase` | `loadRecords()`, `transactionCount` |
| Classes / interfaces / types | `PascalCase` | `RecordProcessor`, `TransactionSchema` |
| Constants (module-level) | `UPPER_SNAKE_CASE` | `MAX_BATCH_SIZE = 500` |
| Private class fields | `#field` (native private) | `#validator` |
| Files | `kebab-case` | `record-processor.ts`, `transaction-schema.ts` |
| Directories | `kebab-case` | `data-models/`, `pipeline-stages/` |
| Enum members | `PascalCase` | `ProcessingStatus.Complete` |

No `I` prefix on interfaces (`RecordReader` not `IRecordReader`).
No `_` prefix for private if using `#` native private fields.

---

## Type System

```typescript
// Always strict — tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}

// No any — use unknown with narrowing
function parseRecord(raw: unknown): TransactionRecord {
  if (!isTransactionRecord(raw)) {
    throw new TypeError(`Expected TransactionRecord, got: ${JSON.stringify(raw)}`);
  }
  return raw;
}

// Readonly properties
interface TransactionRecord {
  readonly id: string;
  readonly amount: number;
  readonly currency: string;
}

// Discriminated unions for states
type ProcessResult =
  | { status: 'success'; record: ProcessedRecord }
  | { status: 'failure'; reason: string };
```

---

## Functions

- Arrow functions for callbacks and short utilities
- Named `function` declarations for top-level exported functions (better stack traces)
- Explicit return types on public functions
- Default parameters over `undefined` checks:
  ```typescript
  function loadBatch(path: string, batchSize = 100): Promise<Record[]> { ... }
  ```
- Destructuring for object parameters when 3+ args:
  ```typescript
  function process({ records, batchSize, onError }: ProcessOptions): void { ... }
  ```

---

## Classes

- Use classes for stateful services with injected dependencies
- Prefer `readonly` on all injected dependencies
- Constructor injection only — no setter injection
- `abstract` classes over deeply nested inheritance
- Interfaces (structural typing) over `implements` chains

```typescript
class TransactionProcessor {
  constructor(
    private readonly reader: RecordReader,
    private readonly writer: RecordWriter,
  ) {}

  async process(): Promise<void> {
    const records = await this.reader.read();
    const results = records.map(this.transform);
    await this.writer.write(results);
  }
}
```

---

## Modules

- ESM (`import`/`export`) everywhere — no `require()`
- One primary export per file; co-locate closely related items
- Barrel files (`index.ts`) for public API surfaces only — not for every directory
- No circular imports — if A imports B and B imports A, extract a shared C

---

## Error Handling

```typescript
// Custom typed errors
class ValidationError extends Error {
  constructor(
    message: string,
    public readonly field: string,
    public readonly received: unknown,
  ) {
    super(message);
    this.name = 'ValidationError';
    Object.setPrototypeOf(this, ValidationError.prototype); // needed in some TS configs
  }
}

// Always re-throw or handle
try {
  await processRecord(record);
} catch (error) {
  if (error instanceof ValidationError) {
    logger.warn({ field: error.field }, error.message);
    return { status: 'skipped', reason: error.message };
  }
  throw error; // unknown errors always propagate
}
```

---

## Async Patterns

```typescript
// Prefer async/await over .then() chains
async function loadAllRecords(paths: string[]): Promise<Record[]> {
  const batches = await Promise.all(paths.map(loadFromPath));
  return batches.flat();
}

// Sequential when order matters or rate-limiting applies
async function processSequentially(records: Record[]): Promise<void> {
  for (const record of records) {
    await processRecord(record);
  }
}

// Never mix .then() and await in the same function
// Never forget to await — use ESLint @typescript-eslint/no-floating-promises
```
