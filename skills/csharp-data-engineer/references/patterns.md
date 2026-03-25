# C# Patterns

---

## Result Pattern (typed error handling)

For expected, recoverable failures in library/domain code:

```csharp
public readonly record struct Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public string? Error { get; }

    private Result(bool isSuccess, T? value, string? error)
    {
        IsSuccess = isSuccess;
        Value = value;
        Error = error;
    }

    public static Result<T> Success(T value) => new(true, value, null);
    public static Result<T> Failure(string error) => new(false, default, error);
}

// Usage
Result<TransactionRecord> result = ParseRecord(raw);
if (!result.IsSuccess)
{
    _logger.LogWarning("Skipping invalid record: {Error}", result.Error);
    return;
}
ProcessRecord(result.Value!);
```

Use `throw` for unexpected conditions. Use `Result<T>` when callers must explicitly handle failure.

---

## Dependency Injection (Microsoft.Extensions.DI)

```csharp
// Registration in Program.cs / Startup
services.AddScoped<IRecordReader, CsvRecordReader>();
services.AddScoped<IRecordWriter, DatabaseRecordWriter>();
services.AddScoped<TransactionProcessor>();

// Constructor injection (primary constructor style, .NET 8+)
public class TransactionProcessor(
    IRecordReader reader,
    IRecordWriter writer,
    ILogger<TransactionProcessor> logger)
{
    public async Task ProcessAsync(CancellationToken cancellationToken = default)
    {
        logger.LogInformation("Starting processing");
        var records = await reader.ReadAsync(cancellationToken);
        await writer.WriteAsync(records, cancellationToken);
    }
}
```

---

## Options Pattern (configuration)

```csharp
public sealed class PipelineOptions
{
    public const string SectionName = "Pipeline";

    [Required]
    public required string SourcePath { get; init; }

    [Range(1, 10_000)]
    public int BatchSize { get; init; } = 100;
}

// Registration
services.AddOptions<PipelineOptions>()
    .BindConfiguration(PipelineOptions.SectionName)
    .ValidateDataAnnotations()
    .ValidateOnStart();

// Consumption
public class Processor(IOptions<PipelineOptions> options) { ... }
```

---

## IDisposable and using

```csharp
// Always implement IDisposable for classes managing unmanaged resources
public sealed class DatabaseConnection : IDisposable
{
    private readonly SqlConnection _connection;
    private bool _disposed;

    public void Dispose()
    {
        if (!_disposed)
        {
            _connection.Dispose();
            _disposed = true;
        }
    }
}

// Callers always use 'using'
using var connection = new DatabaseConnection(connectionString);
await connection.ExecuteAsync(query, cancellationToken);
// connection.Dispose() called automatically
```

---

## LINQ — functional data transforms

```csharp
// Chain transforms — materialise at the boundary
var summary = transactions
    .Where(t => t.Status == TransactionStatus.Complete)
    .GroupBy(t => t.Currency)
    .Select(g => new CurrencySummary(
        Currency: g.Key,
        Total: g.Sum(t => t.Amount),
        Count: g.Count()))
    .OrderByDescending(s => s.Total)
    .ToList();  // materialise — no deferred execution after this boundary

// Avoid side effects in LINQ chains (Select/Where should be pure)
```

---

## Async Streams for large datasets

```csharp
public async IAsyncEnumerable<IReadOnlyList<T>> ReadInBatchesAsync<T>(
    int batchSize,
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
{
    var batch = new List<T>(batchSize);
    await foreach (var item in GetAllItemsAsync(cancellationToken))
    {
        batch.Add(item);
        if (batch.Count >= batchSize)
        {
            yield return batch.AsReadOnly();
            batch = new List<T>(batchSize);
        }
    }
    if (batch.Count > 0)
        yield return batch.AsReadOnly();
}
```
