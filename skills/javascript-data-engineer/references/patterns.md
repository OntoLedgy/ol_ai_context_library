# JavaScript / TypeScript Patterns

---

## Async / Await

```typescript
// Parallel independent operations
const [users, transactions] = await Promise.all([
  fetchUsers(),
  fetchTransactions(),
]);

// Sequential (order matters or rate limiting)
for (const record of records) {
  await processRecord(record);
}

// Concurrent with limit (use p-limit or similar)
import pLimit from 'p-limit';
const limit = pLimit(5);
await Promise.all(records.map(r => limit(() => processRecord(r))));

// Error handling in parallel — allSettled when partial failure is acceptable
const results = await Promise.allSettled(records.map(processRecord));
const succeeded = results
  .filter((r): r is PromiseFulfilledResult<ProcessedRecord> => r.status === 'fulfilled')
  .map(r => r.value);
```

---

## Result Type (typed error handling)

```typescript
type Result<T, E = string> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function parseRecord(raw: unknown): Result<TransactionRecord> {
  if (!isTransactionRecord(raw)) {
    return { ok: false, error: `Invalid record: ${JSON.stringify(raw)}` };
  }
  return { ok: true, value: raw };
}

// Usage
const result = parseRecord(input);
if (!result.ok) {
  logger.warn(result.error);
  return;
}
const record = result.value;
```

Use `Result` for expected, recoverable failures in library code. Use `throw` for unexpected conditions.

---

## Dependency Injection

```typescript
// Define interfaces (not implementations) as dependencies
interface RecordReader { read(): Promise<Record[]>; }
interface RecordWriter { write(records: Record[]): Promise<void>; }

class Pipeline {
  constructor(
    private readonly reader: RecordReader,
    private readonly writer: RecordWriter,
  ) {}

  async run(): Promise<void> {
    const records = await this.reader.read();
    await this.writer.write(records);
  }
}

// In production
const pipeline = new Pipeline(new CsvReader(path), new DbWriter(conn));
// In tests
const pipeline = new Pipeline(mockReader, mockWriter);
```

---

## Functional Patterns

```typescript
// Map / filter / reduce with type safety
const totals: number[] = records.map(r => r.amount);
const valid = records.filter(r => r.amount > 0);
const total = records.reduce((sum, r) => sum + r.amount, 0);

// Type-safe groupBy (no lodash needed in modern JS)
function groupBy<T>(items: T[], key: (item: T) => string): Record<string, T[]> {
  return items.reduce<Record<string, T[]>>((acc, item) => {
    const k = key(item);
    (acc[k] ??= []).push(item);
    return acc;
  }, {});
}

// Immutable updates
const updated = { ...record, amount: record.amount * 1.1 };
const withNewItem = [...records, newRecord];
```

---

## Module Pattern

```typescript
// Public API — explicit exports from index.ts
// src/transactions/index.ts
export type { TransactionRecord } from './types.js';
export { TransactionProcessor } from './processor.js';
// Do NOT re-export internal implementation details

// Barrel file only at package boundary — not for every folder
```

---

## Type Guards

```typescript
function isTransactionRecord(value: unknown): value is TransactionRecord {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value && typeof value.id === 'string' &&
    'amount' in value && typeof value.amount === 'number'
  );
}
```
