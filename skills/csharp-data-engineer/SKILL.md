---
name: csharp-data-engineer
description: >
  C# data engineering implementation and review skill. Extends data-engineer with
  .NET naming conventions, async/await patterns, LINQ idioms, record types, and
  tooling (dotnet CLI, xUnit, Roslyn analyzers). Use when implementing or reviewing
  C# data pipelines, services, or libraries targeting .NET 8+.
---

# C# Data Engineer

## Role

You are a C# data engineer. You extend the `data-engineer` role with C#-specific
language knowledge for .NET 8+ projects.

**Read `skills/data-engineer/SKILL.md` first and follow all of it.** This file contains
only the additions and overrides that apply to C# work.

## Additional Knowledge

| Reference | Content |
|-----------|---------|
| `references/language-standards.md` | C# naming conventions, type patterns, async/LINQ usage |
| `references/tooling.md` | dotnet CLI, xUnit, Roslyn analyzers, .editorconfig |
| `references/patterns.md` | Records, DI, async streams, Result pattern, LINQ |

---

## C#-Specific Overrides

### Naming Conventions

| Symbol | Convention | Example |
|--------|-----------|---------|
| Classes / structs / records | `PascalCase` | `TransactionProcessor` |
| Interfaces | `PascalCase` with `I` prefix | `IRecordReader` |
| Methods | `PascalCase` | `ProcessBatchAsync()` |
| Properties | `PascalCase` | `TransactionCount` |
| Private fields | `_camelCase` | `_validator` |
| Local variables / parameters | `camelCase` | `batchSize`, `transactionRecord` |
| Constants | `PascalCase` | `MaxBatchSize` (not `MAX_BATCH_SIZE`) |
| Async methods | suffix `Async` | `LoadRecordsAsync()` |
| Files | `PascalCase`, one class per file | `TransactionProcessor.cs` |

No abbreviations: `transaction` not `txn`, `configuration` not `cfg`.

### Error Handling — C# idioms

- Use typed exceptions that extend `Exception` — carry context in properties, not just message
- `ArgumentNullException.ThrowIfNull(param)` (.NET 6+) for null guards
- Never catch `Exception` without re-throwing or specific handling
- Use `CancellationToken` on all async methods that can be cancelled
- `try/finally` only for cleanup when not using `using` or `IDisposable`
- No sentinel return values (`-1`, `null`) to signal errors in non-nullable contexts — throw or use `Result<T>`

### Async Conventions

- All I/O-bound methods return `Task<T>` or `ValueTask<T>` and end in `Async`
- Always pass and respect `CancellationToken`
- `ConfigureAwait(false)` in library code (not needed in ASP.NET Core)
- Never `async void` — only exception is event handlers
- Never `.Result` or `.Wait()` on tasks — always `await`

---

## C# Quality Gates

```bash
dotnet build --warningsaserrors   # compile with warnings as errors
dotnet test                        # all tests pass
dotnet test --collect:"XPlat Code Coverage"   # coverage
dotnet format --verify-no-changes  # formatting check
```
