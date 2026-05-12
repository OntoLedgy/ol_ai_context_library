# Go Patterns

This skill emphasises data-pipeline patterns. Concurrency in Go is a first-class
construction material; learn these shapes and you can build most ETL/streaming
workloads from them.

---

## Functional Options (construction with many optional fields)

```go
type Pipeline struct {
    sourcePath string
    batchSize  int
    maxRetries int
}

type Option func(*Pipeline)

func WithBatchSize(n int) Option {
    return func(p *Pipeline) { p.batchSize = n }
}

func WithMaxRetries(n int) Option {
    return func(p *Pipeline) { p.maxRetries = n }
}

func NewPipeline(sourcePath string, opts ...Option) *Pipeline {
    p := &Pipeline{
        sourcePath: sourcePath,
        batchSize:  100,    // defaults
        maxRetries: 3,
    }
    for _, opt := range opts {
        opt(p)
    }
    return p
}

// Usage
p := NewPipeline("data/input.csv",
    WithBatchSize(500),
    WithMaxRetries(5),
)
```

Use when construction has many optional parameters. Adds new options without breaking
callers, unlike a config struct with growing fields.

---

## Newtype-Style Type Safety

Go has no real newtype, but a named type with the same underlying type prevents
accidental mixing.

```go
type TransactionID string
type AccountID string

// Compiler rejects passing AccountID where TransactionID is expected
func findTransaction(id TransactionID) (*Record, error) { ... }

// Conversion is explicit
var raw string = "tx-1"
txID := TransactionID(raw)
```

---

## Pipeline via Channels

The canonical Go ETL shape: each stage is a goroutine that reads from one channel and
writes to the next. Stages are composable and backpressure is automatic.

```go
// Stage 1: produce
func source(ctx context.Context, path string) (<-chan Record, <-chan error) {
    out := make(chan Record)
    errc := make(chan error, 1)
    go func() {
        defer close(out)
        defer close(errc)
        f, err := os.Open(path)
        if err != nil {
            errc <- fmt.Errorf("opening %s: %w", path, err)
            return
        }
        defer f.Close()
        scanner := bufio.NewScanner(f)
        for scanner.Scan() {
            rec, err := parseLine(scanner.Bytes())
            if err != nil {
                errc <- fmt.Errorf("parse: %w", err)
                return
            }
            select {
            case out <- rec:
            case <-ctx.Done():
                errc <- ctx.Err()
                return
            }
        }
    }()
    return out, errc
}

// Stage 2: transform
func transform(ctx context.Context, in <-chan Record) <-chan Processed {
    out := make(chan Processed)
    go func() {
        defer close(out)
        for rec := range in {
            select {
            case out <- process(rec):
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

// Stage 3: sink
func sink(ctx context.Context, in <-chan Processed) error {
    for p := range in {
        if err := write(ctx, p); err != nil {
            return fmt.Errorf("writing %s: %w", p.ID, err)
        }
    }
    return nil
}
```

Rules:
- **Sender closes the channel, never the receiver.** Closing twice panics.
- Every blocking send/receive has a `<-ctx.Done()` companion in a `select` — otherwise a cancelled pipeline leaks goroutines.
- Use buffered channels only when you have a measured reason; default to unbuffered for natural backpressure.

---

## Fan-Out / Fan-In

Parallelise a CPU-bound or I/O-bound stage across N workers, then merge results.

```go
// Fan-out: N workers each reading from the same input channel
func fanOut(ctx context.Context, in <-chan Record, n int) []<-chan Processed {
    outs := make([]<-chan Processed, n)
    for i := 0; i < n; i++ {
        outs[i] = transform(ctx, in)   // each worker is a transform stage
    }
    return outs
}

// Fan-in: merge N output channels into one
func fanIn(ctx context.Context, ins ...<-chan Processed) <-chan Processed {
    out := make(chan Processed)
    var wg sync.WaitGroup
    wg.Add(len(ins))
    for _, ch := range ins {
        go func(c <-chan Processed) {
            defer wg.Done()
            for v := range c {
                select {
                case out <- v:
                case <-ctx.Done():
                    return
                }
            }
        }(ch)
    }
    go func() {
        wg.Wait()
        close(out)
    }()
    return out
}
```

---

## Worker Pool (bounded concurrency)

When you have N units of work and want at most W in flight at once.

```go
import "golang.org/x/sync/errgroup"

func processAll(ctx context.Context, records []Record, workers int) error {
    g, ctx := errgroup.WithContext(ctx)
    sem := make(chan struct{}, workers)

    for _, rec := range records {
        rec := rec   // capture
        select {
        case sem <- struct{}{}:
        case <-ctx.Done():
            return ctx.Err()
        }
        g.Go(func() error {
            defer func() { <-sem }()
            return process(ctx, rec)
        })
    }
    return g.Wait()
}
```

`errgroup` propagates the first error and cancels the shared context — every other
worker observing `ctx.Done()` exits cleanly.

---

## Context Cancellation

```go
// Add a deadline
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()    // always defer cancel — leaks the goroutine that fires the timer otherwise

// Cancel manually
ctx, cancel := context.WithCancel(ctx)
defer cancel()
// ...later
cancel()

// Always check in long loops
for {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case rec := <-in:
        if err := process(ctx, rec); err != nil {
            return err
        }
    }
}
```

---

## Errgroup vs sync.WaitGroup

| Use | When |
|-----|------|
| `errgroup.Group` | Goroutines can fail; you want first error and shared cancellation |
| `sync.WaitGroup` | Goroutines cannot fail (or all errors are independent); just wait for completion |

`errgroup` is almost always the right choice for data pipelines.

---

## Resource Cleanup with defer

```go
func loadFile(path string) ([]byte, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, fmt.Errorf("opening %s: %w", path, err)
    }
    defer f.Close()    // runs on return, even on panic

    return io.ReadAll(f)
}
```

For resources where `Close` returns an error you care about (e.g. flushing a writer),
assign it to a named return:

```go
func writeFile(path string, data []byte) (err error) {
    f, ferr := os.Create(path)
    if ferr != nil {
        return fmt.Errorf("creating %s: %w", path, ferr)
    }
    defer func() {
        if cerr := f.Close(); cerr != nil && err == nil {
            err = fmt.Errorf("closing %s: %w", path, cerr)
        }
    }()
    _, err = f.Write(data)
    return err
}
```

---

## Table-Driven Tests

The idiomatic Go testing pattern. Every test case in one table; one loop runs them all.

```go
func TestParseRecord(t *testing.T) {
    cases := []struct {
        name    string
        input   string
        want    Record
        wantErr error
    }{
        {
            name:  "valid record",
            input: `{"id":"tx-1","amount":100.0,"currency":"USD"}`,
            want:  Record{ID: "tx-1", Amount: 100.0, Currency: "USD"},
        },
        {
            name:    "missing id",
            input:   `{"amount":100.0,"currency":"USD"}`,
            wantErr: ErrMissingID,
        },
        {
            name:    "negative amount",
            input:   `{"id":"tx-1","amount":-1.0,"currency":"USD"}`,
            wantErr: ErrInvalidAmount,
        },
    }
    for _, tc := range cases {
        tc := tc                       // capture
        t.Run(tc.name, func(t *testing.T) {
            t.Parallel()
            got, err := ParseRecord([]byte(tc.input))
            if tc.wantErr != nil {
                if !errors.Is(err, tc.wantErr) {
                    t.Fatalf("err = %v, want %v", err, tc.wantErr)
                }
                return
            }
            if err != nil {
                t.Fatalf("unexpected error: %v", err)
            }
            if got != tc.want {
                t.Errorf("got %+v, want %+v", got, tc.want)
            }
        })
    }
}
```

Capture loop variables with `tc := tc` until Go 1.22+ (where per-iteration scoping is
default) — the duplicate line is harmless and explicit.

---

## Stream-Friendly I/O

Don't load whole files into memory.

```go
import (
    "bufio"
    "encoding/json"
    "os"
)

func streamRecords(ctx context.Context, path string, out chan<- Record) error {
    f, err := os.Open(path)
    if err != nil {
        return fmt.Errorf("opening %s: %w", path, err)
    }
    defer f.Close()

    scanner := bufio.NewScanner(f)
    scanner.Buffer(make([]byte, 0, 64*1024), 1024*1024)   // grow up to 1MB lines
    for scanner.Scan() {
        var rec Record
        if err := json.Unmarshal(scanner.Bytes(), &rec); err != nil {
            return fmt.Errorf("decoding line: %w", err)
        }
        select {
        case out <- rec:
        case <-ctx.Done():
            return ctx.Err()
        }
    }
    return scanner.Err()
}
```

---

## Interfaces at the Consumer

```go
// pipeline package: declares what it needs
package pipeline

type Source interface {
    Read(ctx context.Context) (<-chan Record, error)
}

type Sink interface {
    Write(ctx context.Context, records <-chan Processed) error
}

func Run(ctx context.Context, s Source, k Sink) error { ... }
```

```go
// reader package: provides a concrete implementation, knows nothing about pipeline
package reader

type CSV struct{ path string }
func NewCSV(path string) *CSV { return &CSV{path: path} }
func (c *CSV) Read(ctx context.Context) (<-chan Record, error) { ... }
```

`reader.CSV` satisfies `pipeline.Source` without saying so anywhere. The benefit:
implementations have no dependency on the consumer's interface, and tests can stub by
declaring a local interface.

---

## When NOT to Reach for a Goroutine

- Sequential work that runs in milliseconds — adding a goroutine adds scheduling overhead and complicates error handling.
- Anywhere you'd need a mutex *and* a channel to coordinate — usually means the design needs simplifying first.
- Inside a hot inner loop — channels are not free; profile before parallelising.

Default to sequential; reach for goroutines when there is a real concurrency need
(I/O overlap, CPU parallelism, independent streams).
