# Clean Code Refactor — C#

Language-specific refactoring patterns for C# (.NET 8+).
Read alongside the general `clean-code-refactor` SKILL.md.

---

## Naming Fixes

| Violation | Before | After |
|-----------|--------|-------|
| Non-PascalCase method | `processRecord()` | `ProcessRecord()` |
| Non-PascalCase property | `transactionCount` | `TransactionCount` |
| Field without `_` prefix | `private RecordReader reader` | `private readonly IRecordReader _reader` |
| Async without suffix | `public Task Load()` | `public Task LoadAsync()` |
| Missing `I` on interface | `interface RecordReader` | `interface IRecordReader` |
| Abbreviation | `txn`, `cfg`, `acct` | `transaction`, `configuration`, `account` |

---

## Method Extraction (C#)

```csharp
// Before — one method doing everything
public async Task ProcessDataAsync(
    IReadOnlyList<object> records,
    object config,
    string outputPath,
    CancellationToken cancellationToken = default)
{
    // 54 lines: validation, transformation, writing
    ...
}

// After
public async Task ProcessDataAsync(
    IReadOnlyList<TransactionRecord> records,
    ProcessingConfig config,
    string outputPath,
    CancellationToken cancellationToken = default)
{
    var validated = ValidateRecords(records);
    var transformed = TransformRecords(validated, config);
    await WriteResultsAsync(transformed, outputPath, cancellationToken);
}

private static IReadOnlyList<TransactionRecord> ValidateRecords(
    IReadOnlyList<TransactionRecord> records) { ... }

private static IReadOnlyList<ProcessedRecord> TransformRecords(
    IReadOnlyList<TransactionRecord> records,
    ProcessingConfig config) { ... }

private async Task WriteResultsAsync(
    IReadOnlyList<ProcessedRecord> records,
    string outputPath,
    CancellationToken cancellationToken) { ... }
```

---

## Parameter Reduction (C#)

```csharp
// Before
public Record CreateRecord(
    string name,
    decimal amount,
    string currency,
    string source,
    DateTime timestamp)

// After — introduce a record
public record CreateRecordRequest(
    string Name,
    decimal Amount,
    string Currency,
    string Source,
    DateTime Timestamp);

public Record CreateRecord(CreateRecordRequest request) { ... }
```

---

## Error Handling Fixes (C#)

```csharp
// Before — returning null
public TransactionRecord? FindRecord(string id)
{
    var result = _db.Query(id);
    return result ?? null;
}

// After — throw with context
public TransactionRecord FindRecord(string id)
{
    var result = _db.Query(id)
        ?? throw new RecordNotFoundException(id);
    return result;
}

public sealed class RecordNotFoundException : Exception
{
    public string RecordId { get; }
    public RecordNotFoundException(string recordId)
        : base($"Record not found: id={recordId}")
    {
        RecordId = recordId;
    }
}

// Before — catch all without filter
catch (Exception ex)
{
    _logger.LogError(ex, "Error");
}

// After — preserve cancellation
catch (Exception ex) when (ex is not OperationCanceledException)
{
    _logger.LogError(ex, "Error processing record {RecordId}", recordId);
    throw;
}

// Before — .Result / .Wait()
var records = LoadRecordsAsync().Result;

// After — await
var records = await LoadRecordsAsync(cancellationToken);
```

---

## Dependency Injection Fix (C#)

```csharp
// Before — depends on concrete type
public class TransactionProcessor
{
    private readonly CsvRecordReader _reader;
    public TransactionProcessor() { _reader = new CsvRecordReader(); }
}

// After — inject abstraction via primary constructor
public class TransactionProcessor(IRecordReader reader)
{
    private readonly IRecordReader _reader = reader;

    public async Task ProcessAsync(CancellationToken cancellationToken = default)
    {
        var records = await _reader.ReadAsync(cancellationToken);
        ...
    }
}
```

---

## Smell Fixes (C#)

```csharp
// Before — magic numbers/strings
if (retryCount > 3) Task.Delay(500);
if (status == "COMPLETE") ...

// After
private const int MaxRetryCount = 3;
private static readonly TimeSpan RetryDelay = TimeSpan.FromMilliseconds(500);

if (retryCount > MaxRetryCount) await Task.Delay(RetryDelay, cancellationToken);
if (status == ProcessingStatus.Complete.ToString()) ...
// or better:
if (processingStatus == ProcessingStatus.Complete) ...
```
