# Clean Code Refactor — JavaScript / TypeScript

Language-specific refactoring patterns for TypeScript/JavaScript.
Read alongside the general `clean-code-refactor` SKILL.md.

---

## Naming Fixes

| Violation | Before | After |
|-----------|--------|-------|
| Abbreviation | `const txn = ...`, `function procRec` | `const transaction = ...`, `function processRecord` |
| `I` prefix on interface | `interface IRecordReader` | `interface RecordReader` |
| Non-camelCase function | `function process_record()` | `function processRecord()` |
| Non-PascalCase class | `class transactionProcessor` | `class TransactionProcessor` |
| Generic callback name | `records.map(x => x.amount)` | `records.map(record => record.amount)` |

---

## Function Extraction (TypeScript)

```typescript
// Before
async function processData(
  records: unknown[],
  config: any,
  outputPath: string,
): Promise<void> {
  // 54 lines: validation, transformation, writing
  ...
}

// After
async function processData(
  records: unknown[],
  config: ProcessingConfig,
  outputPath: string,
): Promise<void> {
  const validated = validateRecords(records);
  const transformed = transformRecords(validated, config);
  await writeResults(transformed, outputPath);
}

function validateRecords(records: unknown[]): TransactionRecord[] { ... }

function transformRecords(
  records: TransactionRecord[],
  config: ProcessingConfig,
): ProcessedRecord[] { ... }

async function writeResults(
  records: ProcessedRecord[],
  outputPath: string,
): Promise<void> { ... }
```

---

## Argument Reduction (TypeScript)

```typescript
// Before
function createRecord(
  name: string,
  amount: number,
  currency: string,
  source: string,
  timestamp: Date,
): Record { ... }

// After — introduce options interface
interface CreateRecordOptions {
  readonly name: string;
  readonly amount: number;
  readonly currency: string;
  readonly source: string;
  readonly timestamp: Date;
}

function createRecord(options: CreateRecordOptions): Record { ... }
```

---

## Error Handling Fixes (TypeScript)

```typescript
// Before — returning null as error signal
function findRecord(id: string): TransactionRecord | null {
  const result = db.query(id);
  if (!result) return null;
  return result;
}

// After — throw typed error
function findRecord(id: string): TransactionRecord {
  const result = db.query(id);
  if (!result) {
    throw new RecordNotFoundError(`Record not found: id=${id}`);
  }
  return result;
}

// Before — throw string
throw 'record not found';

// After — throw Error subclass
class RecordNotFoundError extends Error {
  constructor(message: string, public readonly recordId: string) {
    super(message);
    this.name = 'RecordNotFoundError';
    Object.setPrototypeOf(this, RecordNotFoundError.prototype);
  }
}
throw new RecordNotFoundError(`Record not found`, id);

// Before — unhandled promise
fetchRecords();  // floating promise

// After — awaited
await fetchRecords();
// or if fire-and-forget is intentional:
void fetchRecords().catch(error => logger.error(error));
```

---

## `any` Removal (TypeScript)

```typescript
// Before
function process(data: any): any { ... }

// After — explicit types
function process(data: TransactionRecord): ProcessedRecord { ... }

// Before — unknown input
function process(data: any) {
  return data.amount * 2;
}

// After — use unknown with type guard
function process(data: unknown): number {
  if (!isTransactionRecord(data)) {
    throw new TypeError(`Expected TransactionRecord, got: ${JSON.stringify(data)}`);
  }
  return data.amount * 2;
}
```

---

## Smell Fixes (TypeScript)

```typescript
// Before — magic string/number
if (record.status === 'COMPLETE') { ... }
if (retryCount > 3) { ... }

// After — enum and constant
enum RecordStatus { Complete = 'COMPLETE', Pending = 'PENDING' }
const MAX_RETRY_COUNT = 3;

if (record.status === RecordStatus.Complete) { ... }
if (retryCount > MAX_RETRY_COUNT) { ... }

// Before — console.log left in
console.log('processing', record);

// After — remove or replace with structured logger
logger.debug({ record }, 'processing record');
```
