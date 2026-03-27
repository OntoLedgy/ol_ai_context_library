# Clean Code Tests — C#

Language-specific testing patterns for C# (.NET 8+).
Read alongside `references/testing-philosophy.md` and `references/testing-standards.md`.

---

## Framework and Tooling

| Tool | Purpose |
|------|---------|
| `xUnit` | Preferred test framework — `[Fact]`, `[Theory]`, `IClassFixture` |
| `Moq` | Mocking library — `Mock<T>`, `.Setup()`, `.Verify()` |
| `FluentAssertions` | Readable assertions — `.Should().Be()` |
| `Microsoft.AspNetCore.Mvc.Testing` | Integration testing for ASP.NET Core |
| `Testcontainers` | Docker-based external services in integration tests |
| `dotnet test` | Test runner |

---

## File and Class Structure

```csharp
// tests/UnitTests/Module/ComponentNameTests.cs

using FluentAssertions;
using Moq;
using Xunit;

namespace MyProject.Tests.UnitTests.Module;

public class ComponentNameTests
{
    private readonly ComponentName _sut;
    private readonly Mock<IExternalService> _mockService;

    public ComponentNameTests()
    {
        _mockService = new Mock<IExternalService>();
        _sut = new ComponentName(_mockService.Object);
    }

    [Fact]
    public void Process_ValidInput_ReturnsExpectedOutput()
    {
        // Arrange
        var input = new InputData { Key = "value" };
        var expected = new OutputData { Processed = true, Key = "value" };

        // Act
        var result = _sut.Process(input);

        // Assert
        result.Should().BeEquivalentTo(expected);
    }

    [Fact]
    public void Process_NullInput_ThrowsArgumentNullException()
    {
        // Arrange & Act
        var act = () => _sut.Process(null!);

        // Assert
        act.Should().Throw<ArgumentNullException>()
            .WithMessage("*input*");
    }
}
```

Rules:
- Test class named `<ComponentName>Tests`
- Subject under test stored in `_sut` (System Under Test)
- Constructor for per-test setup; `IClassFixture<T>` for shared expensive setup
- `private readonly` fields for sut and mocks
- Namespace mirrors source: `MyProject.Tests.UnitTests.Module`

---

## Naming

| Unit | Pattern | Example |
|------|---------|---------|
| Test class | `<ComponentName>Tests` | `TransactionLoaderTests` |
| Test method | `<Method>_<StateUnderTest>_<ExpectedBehaviour>` | `Load_MissingFile_ThrowsFileNotFoundException` |
| Fixture class | `<Feature>Fixture` | `DatabaseFixture` |

---

## Fixtures and Shared Setup

### Per-test setup (constructor / `IAsyncLifetime`)

```csharp
public class TransactionLoaderTests
{
    private readonly TransactionLoader _sut;

    public TransactionLoaderTests()
    {
        // Runs before each test
        _sut = new TransactionLoader();
    }
}
```

### Shared expensive setup (`IClassFixture<T>`)

```csharp
public class DatabaseFixture : IAsyncLifetime
{
    public TestDatabase Database { get; private set; } = null!;

    public async Task InitializeAsync()
    {
        Database = await TestDatabase.CreateAsync();
    }

    public async Task DisposeAsync()
    {
        await Database.DisposeAsync();
    }
}

public class RepositoryIntegrationTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;

    public RepositoryIntegrationTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public async Task Save_ValidRecord_PersistsToDatabase()
    {
        // Arrange
        var repository = new TransactionRepository(_fixture.Database.ConnectionString);
        var record = new Transaction { Amount = 100m };

        // Act
        await repository.SaveAsync(record);

        // Assert
        var saved = await repository.FindAsync(record.Id);
        saved.Should().NotBeNull();
        saved!.Amount.Should().Be(100m);
    }
}
```

---

## Mocking with Moq

```csharp
[Fact]
public void Process_CallsFormatterOnce_WithRawRecord()
{
    // Arrange
    var mockFormatter = new Mock<IRecordFormatter>();
    mockFormatter
        .Setup(f => f.Format(It.IsAny<RawRecord>()))
        .Returns(new FormattedRecord { Label = "formatted" });

    var sut = new RecordProcessor(mockFormatter.Object);
    var rawRecord = new RawRecord { Data = "raw" };

    // Act
    sut.Process(rawRecord);

    // Assert
    mockFormatter.Verify(
        f => f.Format(It.Is<RawRecord>(r => r.Data == "raw")),
        Times.Once);
}
```

---

## Error Path Testing

```csharp
[Fact]
public void Load_MissingFilePath_ThrowsFileNotFoundException()
{
    // Arrange
    var invalidPath = "/nonexistent/file.csv";

    // Act
    var act = () => _sut.Load(invalidPath);

    // Assert
    act.Should().Throw<FileNotFoundException>()
        .WithMessage($"*{invalidPath}*");
}

[Fact]
public async Task FetchAsync_ApiUnavailable_ThrowsHttpRequestException()
{
    // Arrange
    _mockHttpClient
        .Setup(c => c.GetAsync(It.IsAny<string>(), It.IsAny<CancellationToken>()))
        .ThrowsAsync(new HttpRequestException("Connection refused"));

    // Act
    var act = async () => await _sut.FetchAsync("resource-id");

    // Assert
    await act.Should().ThrowAsync<HttpRequestException>()
        .WithMessage("*Connection refused*");
}
```

---

## Parametrised Tests (`[Theory]` + `[InlineData]`)

```csharp
[Theory]
[InlineData("hello", "HELLO")]
[InlineData("world", "WORLD")]
[InlineData("",      ""     )]
public void Transform_ReturnsUppercasedString(string input, string expected)
{
    var result = _sut.Transform(input);
    result.Should().Be(expected);
}

// MemberData for complex objects
public static IEnumerable<object[]> InvalidPaths =>
[
    ["../etc/passwd", "path traversal"],
    ["/absolute",     "absolute path" ],
];

[Theory]
[MemberData(nameof(InvalidPaths))]
public void Load_UnsafePath_ThrowsArgumentException(string path, string expectedFragment)
{
    var act = () => _sut.Load(path);
    act.Should().Throw<ArgumentException>()
        .WithMessage($"*{expectedFragment}*");
}
```

---

## Async Tests

```csharp
[Fact]
public async Task FetchRecordAsync_ValidId_ReturnsRecord()
{
    // Arrange
    var expectedRecord = new Transaction { Id = "1", Amount = 100m };
    _mockRepository
        .Setup(r => r.FindAsync("1", It.IsAny<CancellationToken>()))
        .ReturnsAsync(expectedRecord);

    // Act
    var result = await _sut.FetchRecordAsync("1");

    // Assert
    result.Should().NotBeNull();
    result!.Amount.Should().Be(100m);
}

[Fact]
public async Task FetchRecordAsync_CancellationRequested_ThrowsOperationCanceledException()
{
    // Arrange
    using var cts = new CancellationTokenSource();
    cts.Cancel();

    // Act
    var act = async () => await _sut.FetchRecordAsync("1", cts.Token);

    // Assert
    await act.Should().ThrowAsync<OperationCanceledException>();
}
```

Rules:
- All async test methods return `Task`, never `async void`
- Always pass and test `CancellationToken` for cancellable operations
- Never use `.Result` or `.Wait()` — always `await`

---

## Integration Tests

```csharp
[Trait("Category", "Integration")]
public class CsvPipelineIntegrationTests : IClassFixture<TempDirectoryFixture>
{
    private readonly TempDirectoryFixture _fixture;

    public CsvPipelineIntegrationTests(TempDirectoryFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public async Task RunPipeline_ValidCsvInput_ProducesExpectedOutput()
    {
        // Arrange
        var inputPath = Path.Combine(_fixture.InputDirectory, "transactions.csv");
        File.WriteAllText(inputPath, "id,amount\n1,100\n2,200");
        var outputPath = Path.Combine(_fixture.OutputDirectory, "result.json");

        // Act
        await Pipeline.RunAsync(inputPath, outputPath);

        // Assert
        var output = await File.ReadAllTextAsync(outputPath);
        output.Should().Contain("\"amount\":100");
        output.Should().Contain("\"amount\":200");
    }
}
```

---

## Anti-Patterns (C# Specific)

| Anti-pattern | Why |
|--------------|-----|
| `async void` test method | Exceptions are swallowed; always return `Task` |
| `.Result` or `.Wait()` | Can deadlock; always `await` |
| `new Mock<ConcreteClass>()` | Can't mock concrete types without virtual methods; use interfaces |
| Asserting `!= null` only | Weak; use `.Should().NotBeNull().And.BeEquivalentTo(expected)` |
| `Thread.Sleep` in tests | Flaky; use `Task.Delay` with cancellation or proper async awaiting |
