# Clean Code Reviewer — C#

Language-specific rules for applying clean coding standards to C# code (.NET 8+).
Read alongside the general standards in `prompts/coding/standards/clean_coding/`.

---

## Naming Violations

| Violation | Example | Rule |
|-----------|---------|------|
| Non-PascalCase method | `processRecord()` | Methods are `PascalCase`: `ProcessRecord()` |
| Non-PascalCase property | `transactionCount` | Properties are `PascalCase`: `TransactionCount` |
| Private field without `_` prefix | `private Reader reader` | Use `_camelCase`: `private readonly RecordReader _reader` |
| Async method without `Async` suffix | `public Task Load()` | Must be `LoadAsync()` |
| Missing `I` prefix on interface | `public interface RecordReader` | Must be `IRecordReader` |
| Abbreviation | `txn`, `cfg`, `acct` | Reveal intent: `transaction`, `configuration`, `account` |
| Non-verb method | `public void Validation()` | Methods are verbs: `ValidateRecord()` |

---

## Function / Method Violations

| Violation | C#-Specific Signal |
|-----------|-------------------|
| > 20 lines | Flag; extract helper methods |
| > 3 parameters | Introduce a record or options class |
| `async void` (non-event-handler) | Always `async Task`; `async void` swallows exceptions |
| `.Result` or `.Wait()` on a Task | Deadlock risk; always `await` |
| Missing `CancellationToken` parameter on async method | All async I/O methods should accept `CancellationToken` |
| `ConfigureAwait(false)` absent in library code | Library code should avoid capturing context |
| Flag parameter | `Process(record, isDryRun)` | Two methods: `Process()`, `DryRun()` |

---

## Class Violations

| Violation | C#-Specific Signal |
|-----------|-------------------|
| Constructor injecting concrete type | `public Processor(CsvReader reader)` | Inject `IRecordReader` |
| Non-readonly injected field | `private IRecordReader _reader` | Must be `private readonly IRecordReader _reader` |
| Missing `sealed` on leaf class | Unsealed concrete classes invite unintended subclassing | Mark `sealed` unless designed for extension |
| Missing nullable annotation | `#nullable enable` not present | Enable nullable reference types project-wide |
| `required` property without validation | `public required string Path { get; init; }` without guard | Add `ArgumentException.ThrowIfNullOrEmpty` or data annotation |
| > 200 lines | Likely violating SRP |

---

## Error Handling Violations

| Violation | Example | Rule |
|-----------|---------|------|
| `catch (Exception ex)` without filter | Catches everything including `OperationCanceledException` | Use `when (ex is not OperationCanceledException)` |
| Empty `catch` block | `catch (Exception) {}` | Handle, log, or re-throw |
| Exception swallowed with `return null` | `catch (Exception) { return null; }` | Throw or return `Result<T>` |
| No context in exception message | `throw new Exception("Error")` | Include what was being attempted and the relevant value |
| Missing null guard | Public method accepting reference type without `ArgumentNullException.ThrowIfNull` | Guard at boundary |
| `return null` where non-nullable expected | With `#nullable enable`, this is a compiler warning | Fix the type or throw |

---

## Smell Violations

| Smell | C#-Specific Signal |
|-------|-------------------|
| Magic number | `if (count > 47)`, `Task.Delay(300)` | Extract as `const int` or `static readonly` |
| LINQ side effects | `records.Where(r => { log(r); return true; })` | No side effects in LINQ predicates |
| `.ToList()` inside a loop | `foreach (var r in GetRecords().ToList())` repeated | Materialise once outside the loop |
| Using `dynamic` | — | Replace with a proper type |
| `#pragma warning disable` | — | Fix the underlying issue |
| `string` for IDs/types instead of records/enums | `string status = "COMPLETE"` | Use `enum ProcessingStatus` |

---

## Size Reference (C#)

| Unit | Max | Note |
|------|-----|------|
| Method body | 20 lines | Excluding signature and braces |
| Class | 200 lines | Excluding blank lines |
| File | One primary type | One class/record/interface per file |
| Parameters | 3 | More → introduce a `record` or options class |
