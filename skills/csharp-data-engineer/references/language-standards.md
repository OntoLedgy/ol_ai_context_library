# C# Language Standards (.NET 8+)

---

## Naming

| Symbol | Convention | Example |
|--------|-----------|---------|
| Classes / structs / records | `PascalCase` | `TransactionProcessor`, `RecordBatch` |
| Interfaces | `I` + `PascalCase` | `IRecordReader`, `ITransactionWriter` |
| Methods | `PascalCase` (verb) | `ProcessBatch()`, `LoadRecordsAsync()` |
| Properties | `PascalCase` (noun) | `TransactionCount`, `SourcePath` |
| Private fields | `_camelCase` | `_reader`, `_batchSize` |
| Local variables / params | `camelCase` | `transactionRecord`, `cancellationToken` |
| Constants | `PascalCase` | `MaxBatchSize`, `DefaultTimeout` |
| Enums / enum members | `PascalCase` | `ProcessingStatus.Complete` |
| Async methods | suffix `Async` | `LoadAsync()`, `WriteRecordsAsync()` |
| Generic type params | `T`, `TKey`, `TValue`, or descriptive `TRecord` | |
| Files | `PascalCase.cs`, one type per file | `TransactionProcessor.cs` |

---

## Types — modern C# patterns

### Records (value objects)

```csharp
// Immutable value object
public record TransactionRecord(
    string Id,
    decimal Amount,
    string Currency);

// With validation
public record TransactionRecord
{
    public string Id { get; init; }
    public decimal Amount { get; init; }

    public TransactionRecord(string id, decimal amount)
    {
        ArgumentException.ThrowIfNullOrEmpty(id);
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(amount);
        Id = id;
        Amount = amount;
    }
}
```

### Nullable reference types

```csharp
// Enable in every project
#nullable enable

// All reference type properties are non-nullable by default
public class ProcessingResult
{
    public required string RecordId { get; init; }    // required = must be set
    public string? FailureReason { get; init; }        // nullable = intentionally optional
}
```

### Primary constructors (.NET 8+)

```csharp
public class TransactionProcessor(
    IRecordReader reader,
    IRecordWriter writer)
{
    public async Task ProcessAsync(CancellationToken cancellationToken = default)
    {
        var records = await reader.ReadAsync(cancellationToken);
        await writer.WriteAsync(records, cancellationToken);
    }
}
```

---

## Interfaces and Dependency Inversion

```csharp
public interface IRecordReader
{
    Task<IReadOnlyList<TransactionRecord>> ReadAsync(
        CancellationToken cancellationToken = default);
}

public interface IRecordWriter
{
    Task WriteAsync(
        IReadOnlyList<TransactionRecord> records,
        CancellationToken cancellationToken = default);
}
```

- `I` prefix on all interfaces
- Always use interfaces for injected dependencies — never concrete classes
- `IReadOnlyList<T>` over `List<T>` for return types (callers cannot modify internal state)

---

## Error Handling

```csharp
// Typed exception with context
public sealed class RecordValidationException : Exception
{
    public string RecordId { get; }
    public string FieldName { get; }

    public RecordValidationException(string recordId, string fieldName, string message)
        : base(message)
    {
        RecordId = recordId;
        FieldName = fieldName;
    }
}

// Null guards (.NET 6+)
public void Process(string filePath)
{
    ArgumentNullException.ThrowIfNull(filePath);
    ArgumentException.ThrowIfNullOrEmpty(filePath);
    ...
}

// Never catch Exception without context
catch (Exception ex) when (ex is not OperationCanceledException)
{
    _logger.LogError(ex, "Unexpected error processing record {RecordId}", recordId);
    throw;
}
```

---

## LINQ

```csharp
// Prefer method syntax for clarity with complex chains
var highValueTransactions = transactions
    .Where(t => t.Amount > 1000m)
    .OrderByDescending(t => t.Amount)
    .Take(100)
    .ToList();

// Use query syntax only when joins make it clearer
// Materialise with .ToList() / .ToArray() before leaving a method to avoid deferred execution surprises
```

---

## Async Streams

```csharp
// IAsyncEnumerable for lazy sequences
public async IAsyncEnumerable<TransactionRecord> ReadBatchesAsync(
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
{
    await foreach (var line in ReadLinesAsync(cancellationToken))
    {
        yield return ParseRecord(line);
    }
}

// Consumption
await foreach (var record in reader.ReadBatchesAsync(cancellationToken))
{
    await ProcessRecord(record, cancellationToken);
}
```
