# C# Tooling (.NET 8+)

---

## Standard Toolchain

| Tool | Purpose | Config |
|------|---------|--------|
| `dotnet build` | Compilation | `*.csproj` |
| Roslyn analyzers | Static analysis (built-in) | `*.csproj` + `.editorconfig` |
| `dotnet format` | Formatting | `.editorconfig` |
| xUnit | Test runner | `*.csproj` (test project) |
| `coverlet` | Coverage | `*.csproj` (test project) |

---

## .csproj (baseline)

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <WarningsAsErrors />
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
  </PropertyGroup>
</Project>
```

Test project additions:
```xml
<ItemGroup>
  <PackageReference Include="xunit" Version="2.*" />
  <PackageReference Include="xunit.runner.visualstudio" Version="2.*" />
  <PackageReference Include="Moq" Version="4.*" />
  <PackageReference Include="coverlet.collector" Version="6.*" />
</ItemGroup>
```

---

## .editorconfig (formatting baseline)

```ini
root = true

[*.cs]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

# Naming rules enforced by Roslyn
dotnet_naming_rule.private_fields_should_be_camel_case.severity = warning
dotnet_naming_rule.private_fields_should_be_camel_case.symbols = private_fields
dotnet_naming_rule.private_fields_should_be_camel_case.style = camel_case_underscore_style

dotnet_naming_symbols.private_fields.applicable_kinds = field
dotnet_naming_symbols.private_fields.applicable_accessibilities = private

dotnet_naming_style.camel_case_underscore_style.required_prefix = _
dotnet_naming_style.camel_case_underscore_style.capitalization = camel_case
```

---

## Quality Gates

```bash
dotnet build --warningsaserrors                   # compile; all warnings are errors
dotnet format --verify-no-changes                 # formatting
dotnet test                                        # all tests pass
dotnet test --collect:"XPlat Code Coverage"       # with coverage
reportgenerator -reports:coverage.xml -targetdir:coveragereport
```

---

## Test Structure (xUnit)

```
src/
└── Transactions/
    ├── TransactionProcessor.cs
    └── ...
tests/
└── Transactions.Tests/
    ├── TransactionProcessorTests.cs
    └── ...
```

xUnit test example:
```csharp
public class TransactionProcessorTests
{
    [Fact]
    public async Task ProcessAsync_WithValidRecords_WritesResults()
    {
        // Arrange
        var reader = new Mock<IRecordReader>();
        reader.Setup(r => r.ReadAsync(It.IsAny<CancellationToken>()))
              .ReturnsAsync([mockRecord]);
        var writer = new Mock<IRecordWriter>();
        var processor = new TransactionProcessor(reader.Object, writer.Object);

        // Act
        await processor.ProcessAsync();

        // Assert
        writer.Verify(w => w.WriteAsync(
            It.Is<IReadOnlyList<TransactionRecord>>(l => l.Count == 1),
            It.IsAny<CancellationToken>()), Times.Once);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public void Constructor_WithInvalidAmount_ThrowsArgumentException(decimal amount)
    {
        Assert.Throws<ArgumentOutOfRangeException>(
            () => new TransactionRecord("id", amount));
    }
}
```
