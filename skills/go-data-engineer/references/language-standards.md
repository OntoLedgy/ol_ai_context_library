# Go Language Standards

---

## Naming

| Symbol | Convention | Example |
|--------|-----------|---------|
| Exported funcs / methods / vars / consts / types | `MixedCaps` | `ProcessBatch()`, `MaxBatchSize` |
| Unexported funcs / methods / vars / consts / types | `mixedCaps` | `parseRecord()`, `recordCount` |
| Packages | short, lowercase, single word | `transaction`, `pipeline`, `reader` |
| Files | `snake_case.go` | `transaction_processor.go` |
| Interfaces (single-method) | `-er` suffix | `Reader`, `Writer`, `Closer`, `RecordProcessor` |
| Interfaces (multi-method) | role-based | `RecordStore`, `TransactionService` |
| Receivers | 1–2 letter, consistent per type | `func (r *RecordReader) Read(...)` |
| Acronyms | preserved case as a unit | `HTTPClient`, `userID`, `parseJSON`, `urlPath` |
| Errors (sentinel) | `Err` prefix | `ErrNotFound`, `ErrInvalidAmount` |
| Error types | `-Error` suffix | `type ValidationError struct{...}` |

**No abbreviations in identifiers**: `transaction` not `txn`, `configuration` not `cfg`.
Receivers may be 1–2 letters because they are local and repeated heavily; everything
else gets the full word.

**Package names are not redundant prefixes.** Inside package `transaction`, name the
type `Record`, not `TransactionRecord` — callers write `transaction.Record`.

---

## Package Layout

Default to flat. Reach for `internal/` to forbid external imports.

```
transaction-pipeline/
├── go.mod
├── go.sum
├── cmd/
│   └── pipeline/
│       └── main.go              # thin entrypoint — wiring only
├── internal/
│   ├── transaction/             # domain types and rules
│   │   ├── record.go
│   │   └── record_test.go
│   ├── reader/                  # I/O adapters
│   │   ├── csv.go
│   │   └── csv_test.go
│   └── pipeline/                # orchestration
│       ├── stage.go
│       └── pipeline.go
└── README.md
```

Rules:
- `cmd/<name>/main.go` does wiring only — no logic
- `internal/` contents cannot be imported by other modules
- One concept per package; if a package grows several unrelated concerns, split it
- Avoid `pkg/` and `utils/`; name packages by what they *do*

---

## Error Handling

Errors are values. Every fallible operation returns `(T, error)`.

```go
// Sentinel error — comparable with errors.Is
var ErrNotFound = errors.New("record not found")

// Structured error type — inspectable with errors.As
type ValidationError struct {
    Field  string
    Reason string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Reason)
}

// Wrapping preserves the chain
func loadAndProcess(path string) ([]ProcessedRecord, error) {
    content, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("reading %s: %w", path, err)
    }
    records, err := parseRecords(content)
    if err != nil {
        return nil, fmt.Errorf("parsing %s: %w", path, err)
    }
    return processAll(records), nil
}

// Inspecting wrapped errors
if errors.Is(err, ErrNotFound) {
    // handle missing record
}
var ve *ValidationError
if errors.As(err, &ve) {
    log.Printf("bad field: %s", ve.Field)
}
```

Rules:
- **Always** check `err`. Never assign to `_` unless the function only returns an error you genuinely don't care about — and document why.
- Wrap with `%w` whenever you cross a layer boundary; add the context the caller needs to make sense of the error.
- Don't wrap *and* log the same error — pick one. Logging belongs at the top of the call stack.
- `panic` is for programmer errors and impossible states only. Never for input validation, missing files, or network failures.

---

## Interfaces

Interfaces are satisfied implicitly. **Define interfaces where they are consumed, not
where they are implemented.** Keep them small.

```go
// Defined in the consumer package — describes what the consumer needs
package pipeline

type RecordSource interface {
    Read(ctx context.Context) ([]transaction.Record, error)
}

type RecordSink interface {
    Write(ctx context.Context, records []transaction.Record) error
}

func Run(ctx context.Context, src RecordSource, sink RecordSink) error {
    records, err := src.Read(ctx)
    if err != nil {
        return fmt.Errorf("reading source: %w", err)
    }
    return sink.Write(ctx, records)
}
```

```go
// The implementation lives in its own package and does NOT declare it satisfies the interface
package reader

type CSVReader struct{ path string }

func (r *CSVReader) Read(ctx context.Context) ([]transaction.Record, error) { ... }
```

Rules:
- Prefer many small interfaces over one large one — `io.Reader` and `io.Writer` are the canonical examples
- Don't define an interface "just in case". Wait until there is a second implementation or a test that needs to stub
- Returning concrete types and accepting interfaces is the typical shape

---

## Composition over Inheritance

Go has no inheritance. Compose with embedding.

```go
type Logger struct{ prefix string }
func (l *Logger) Logf(format string, args ...any) { ... }

type RecordReader struct {
    Logger              // embedded — RecordReader gets Logf as if it were its own
    source string
}

r := &RecordReader{Logger: Logger{prefix: "reader"}, source: "data.csv"}
r.Logf("started")      // method promoted from embedded Logger
```

Embedding is delegation, not inheritance — there is no overriding, only shadowing.
If `RecordReader` defines `Logf`, that one is used; the embedded `Logger.Logf` is still
reachable as `r.Logger.Logf(...)`.

---

## Generics (1.18+)

Use generics for containers and algorithms. Prefer concrete types for domain code.

```go
// Generic — operates on any comparable key
func GroupBy[K comparable, V any](items []V, key func(V) K) map[K][]V {
    out := make(map[K][]V)
    for _, item := range items {
        k := key(item)
        out[k] = append(out[k], item)
    }
    return out
}

// Usage
byCurrency := GroupBy(records, func(r Record) string { return r.Currency })
```

Avoid generics when a single concrete type is enough — readable, monomorphic code
beats clever generics.

---

## Context

`context.Context` is the standard way to carry cancellation, deadlines, and
request-scoped values across API boundaries.

```go
// ctx is always the first parameter
func (r *CSVReader) Read(ctx context.Context) ([]Record, error) {
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
    }
    ...
}

// Propagate, don't store on a struct
func Run(ctx context.Context, src RecordSource) error {
    ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()
    return process(ctx, src)
}
```

Rules:
- `ctx` is the first parameter, named `ctx`
- Never pass `nil` — use `context.TODO()` if you genuinely don't have one yet
- Never store a context in a struct
- Use `context.Value` sparingly and only for request-scoped data (trace IDs, auth) — never for optional parameters

---

## Visibility

Visibility is controlled by case. There is no `public` / `private` keyword.

```go
type Record struct {        // exported type
    ID     string           // exported field
    amount float64          // unexported — only this package can read/write
}

func (r *Record) Amount() float64 { return r.amount }   // exported accessor
func (r *Record) validate() error { ... }               // unexported helper
```

Export only what callers need. Default to unexported and promote to exported when a
caller genuinely requires access.

---

## Zero Values

Every type has a useful zero value. Design types so the zero value is meaningful.

```go
type Buffer struct {
    buf []byte    // nil slice — append works on it
}

var b Buffer
b.Write([]byte("hello"))   // no New() needed; zero value is ready
```

If a type needs initialisation, expose a `New<Type>` constructor and document that the
zero value is not valid.
