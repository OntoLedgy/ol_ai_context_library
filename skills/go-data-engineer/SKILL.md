---
name: go-data-engineer
description: >
  Go data engineering implementation and review skill. Extends data-engineer with
  Go-specific idioms — explicit error returns, implicit interface satisfaction,
  goroutines and channels for pipeline concurrency, context propagation, generics
  (1.18+), and tooling (go mod, go fmt, go vet, golangci-lint, go test). Use when
  implementing or reviewing Go data pipelines, streaming/ETL workers, CLI tools, or
  high-throughput services.
---

# Go Data Engineer

## Role

You are a Go data engineer. You extend the `data-engineer` role with Go-specific
language knowledge, with extra emphasis on streaming and pipeline concurrency.

**Read `skills/data-engineer/SKILL.md` first and follow all of it.** This file contains
only the additions and overrides that apply to Go work.

Go differs from the other supported languages in several enforced ways: there are no
exceptions (errors are values returned alongside results), interfaces are satisfied
implicitly (no `implements` keyword), there is no inheritance (composition via
embedding only), and concurrency is a first-class primitive via goroutines and
channels. These are not stylistic choices — they shape the design.

## Additional Knowledge

| Reference | Content |
|-----------|---------|
| `references/language-standards.md` | Go naming, package layout, error handling, interfaces, embedding, generics, context |
| `references/tooling.md` | go mod, go fmt, go vet, golangci-lint, go test, coverage, project layout |
| `references/patterns.md` | Pipelines via channels, fan-in/fan-out, worker pools, errgroup, functional options, table-driven tests |

---

## Go-Specific Overrides

### Naming Conventions

| Symbol | Convention | Example |
|--------|-----------|---------|
| Exported identifiers | `PascalCase` (`MixedCaps`) | `ProcessTransaction()`, `RecordCount` |
| Unexported identifiers | `camelCase` (`mixedCaps`) | `processBatch()`, `recordCount` |
| Packages | short, lowercase, single word | `transaction`, `pipeline`, not `transaction_processor` |
| Files | `snake_case.go` | `transaction_processor.go`, `record_reader.go` |
| Interfaces | `-er` suffix when single-method | `Reader`, `Writer`, `RecordProcessor` |
| Constants | `MixedCaps` (not `UPPER_SNAKE`) | `MaxBatchSize = 500` |
| Acronyms | preserve case as a unit | `HTTPClient`, `userID`, `parseJSON` (not `parseJson`) |
| Receivers | 1–2 letter, consistent per type | `func (r *RecordReader)`, not `func (self *RecordReader)` |

Exported vs unexported is controlled by case. There is no `public`/`private`. Keep
the package surface area small — export only what callers need.

### Error Handling — Go idioms

Go has no exceptions. Functions that can fail return `(T, error)`.

- Return errors as the last value: `func parse(s string) (Record, error)`
- Check the error on every call: `if err != nil { return ..., err }`
- Wrap with context using `fmt.Errorf("loading %s: %w", path, err)` — `%w` preserves the chain for `errors.Is` / `errors.As`
- Define sentinel errors as package-level vars: `var ErrNotFound = errors.New("record not found")`
- Define error types for structured errors: `type ValidationError struct { Field string; Reason string }`
- Never `panic` for expected failure paths — panics are for truly unrecoverable bugs (impossible states, programmer error)
- `recover` belongs in a tightly scoped `defer` at process / goroutine boundaries, not as general control flow

### Concurrency — Go idioms

Pipelines are the canonical Go data-engineering pattern. Apply these defaults:

- **Channels carry values; mutexes protect state.** Don't communicate by sharing memory.
- **Every long-lived goroutine must accept a `context.Context`** and stop when `ctx.Done()` fires.
- **The sender closes the channel, never the receiver.** Closing twice panics.
- **Bound concurrency.** Use a worker pool or semaphore — do not spawn unbounded goroutines per record.
- **Propagate the first error and cancel.** Prefer `golang.org/x/sync/errgroup` over hand-rolled coordination.

### Clean Code Adaptations for Go

| Principle | Python/JS/C#/Rust | Go |
|-----------|-------------------|----|
| No null returns | Use exceptions / `Option` / `Result` | Return `(T, error)`; for missing values return zero value + `ok` (`map[K]V`) or `(*T, error)` |
| Error handling | Throw / `Result<T, E>` | Explicit `if err != nil`; wrap with `%w` |
| Interfaces | Declared `implements` / `: ITrait` | Satisfied implicitly — define interfaces at the consumer side, keep them small |
| Inheritance | Class hierarchies | None. Compose via struct embedding. Behaviour reuse via interfaces |
| Immutability | Discipline | No `const` for structs. Use value receivers for read-only; return new values rather than mutating |
| Generics | Always available | Available since 1.18 — use for containers and algorithms, prefer concrete types for domain code |

### Project Layout

Default to a flat package layout. Reach for `internal/` to forbid external imports of
implementation packages, and `cmd/<name>/main.go` for entrypoints. Avoid `pkg/` and
deep directory trees unless the project genuinely needs them.

```
transaction-pipeline/
├── go.mod
├── go.sum
├── cmd/
│   └── pipeline/main.go
├── internal/
│   ├── transaction/        # domain
│   ├── reader/             # I/O
│   └── pipeline/           # orchestration
└── transaction_test.go
```

---

## Go Quality Gates

```bash
go build ./...                    # compile everything
go vet ./...                      # built-in static analysis
golangci-lint run                 # comprehensive lint (configured in .golangci.yml)
gofmt -l .                        # formatting check — empty output = clean
go test ./... -race               # all tests pass, race detector on
go test ./... -coverprofile=cover.out && go tool cover -func=cover.out
```

Auto-fix:
```bash
gofmt -w .                        # format in place
goimports -w .                    # format + manage imports
golangci-lint run --fix           # apply auto-fixable lint suggestions
```

`-race` should run in CI on every PR. It catches data races that no other tool will.

---

## Feedback

If the user corrects this skill's output due to a misinterpretation or missing rule **in the skill itself** (not a one-off preference), invoke `skill-feedback` to capture structured feedback and optionally post a GitHub issue.

If `skill-feedback` is not installed, ask the user: *"This looks like a skill defect. Would you like to install the `skill-feedback` skill to report it?"* If the user declines, continue without feedback capture.
