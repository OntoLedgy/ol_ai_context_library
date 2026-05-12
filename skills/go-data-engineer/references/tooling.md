# Go Tooling

---

## Standard Toolchain

| Tool | Purpose | Config |
|------|---------|--------|
| `go` | Build, test, module management | `go.mod` |
| `gofmt` / `goimports` | Formatting + import management | none — fixed style |
| `go vet` | Built-in static analysis | none |
| `golangci-lint` | Comprehensive lint aggregator | `.golangci.yml` |
| `go test` | Test runner (built-in) | none |
| `go test -cover` / `go tool cover` | Coverage | none |
| `go test -race` | Data race detector | none |
| `govulncheck` | Vulnerability scanner | none |

Pin the Go toolchain version in `go.mod` (`go 1.23`) so collaborators and CI use the same one.

---

## go.mod (baseline)

```
module github.com/ontoledgy/transaction-pipeline

go 1.23

require (
    github.com/google/uuid v1.6.0
    golang.org/x/sync v0.10.0
)

require (
    // indirect dependencies pinned by `go mod tidy`
)
```

Run `go mod tidy` after every change to imports — it removes unused deps and adds missing ones.

---

## .golangci.yml (baseline)

```yaml
run:
  timeout: 5m
  go: "1.23"

linters:
  disable-all: true
  enable:
    - errcheck         # unchecked errors
    - govet            # built-in analysis
    - ineffassign      # unused assignments
    - staticcheck      # comprehensive static analysis
    - unused           # dead code
    - gosimple         # simplifications
    - gofmt            # formatting
    - goimports        # import grouping
    - revive           # replacement for golint
    - misspell         # English spelling
    - errorlint        # correct %w / errors.Is / errors.As usage
    - bodyclose        # http response body close
    - contextcheck     # context propagation
    - nilerr           # returning nil error after err != nil
    - gocritic         # opinionated checks
    - prealloc         # slice prealloc when length is known

linters-settings:
  errcheck:
    check-blank: true
  revive:
    rules:
      - name: var-naming
      - name: exported

issues:
  exclude-use-default: false
```

---

## Project Structure

```
transaction-pipeline/
├── go.mod
├── go.sum
├── .golangci.yml
├── Makefile
├── cmd/
│   └── pipeline/
│       └── main.go
├── internal/
│   ├── transaction/
│   ├── reader/
│   └── pipeline/
└── README.md
```

`cmd/<name>/main.go` is a thin wiring layer:

```go
package main

import (
    "context"
    "log"
    "os"
    "os/signal"

    "github.com/ontoledgy/transaction-pipeline/internal/pipeline"
    "github.com/ontoledgy/transaction-pipeline/internal/reader"
)

func main() {
    ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
    defer stop()

    src := reader.NewCSV(os.Args[1])
    if err := pipeline.Run(ctx, src); err != nil {
        log.Fatalf("pipeline failed: %v", err)
    }
}
```

---

## Quality Gates

```bash
go build ./...                                            # compile everything
go vet ./...                                              # built-in static analysis
gofmt -l .                                                # empty output = formatted
golangci-lint run                                         # full lint
go test ./... -race -count=1                              # all tests, race on, no cache
go test ./... -coverprofile=cover.out                     # produce coverage profile
go tool cover -func=cover.out                             # coverage summary
go tool cover -html=cover.out -o cover.html               # browsable HTML report
govulncheck ./...                                         # known-vuln scan
```

Auto-fix:
```bash
gofmt -w .                          # format in place
goimports -w .                      # format + organise imports
golangci-lint run --fix             # apply auto-fixable lint suggestions
go mod tidy                         # prune/add module deps
```

`-race` should run in CI on every PR. It is the only practical way to catch
data races. `-count=1` disables the test cache when you want a true rerun.

---

## Test Structure

Tests live next to the code in `*_test.go`, package `xxx` (white-box) or `xxx_test`
(black-box, only sees exported API).

```go
package transaction

import (
    "errors"
    "testing"
)

func TestProcess_ValidRecord_ReturnsProcessed(t *testing.T) {
    record := Record{ID: "tx-1", Amount: 100.0, Currency: "USD"}

    got, err := Process(record)

    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if got.SourceID != "tx-1" {
        t.Errorf("SourceID = %q, want %q", got.SourceID, "tx-1")
    }
}

func TestProcess_NegativeAmount_ReturnsValidationError(t *testing.T) {
    record := Record{Amount: -1.0}

    _, err := Process(record)

    var ve *ValidationError
    if !errors.As(err, &ve) {
        t.Fatalf("got %T, want *ValidationError", err)
    }
    if ve.Field != "Amount" {
        t.Errorf("Field = %q, want %q", ve.Field, "Amount")
    }
}
```

Table-driven tests are the idiomatic Go pattern — see `patterns.md`.

Helpers:
- `t.Helper()` at the top of a helper makes failure lines point at the caller
- `t.Cleanup(fn)` for tear-down — preferred over `defer`
- `t.Parallel()` to mark a test as parallel-safe (combine with `-race`)
- `testing.TB` as a parameter type lets a helper accept both `*testing.T` and `*testing.B`

---

## Benchmarks

```go
func BenchmarkParseRecord(b *testing.B) {
    raw := []byte(`{"id":"tx-1","amount":100.0,"currency":"USD"}`)
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _, _ = ParseRecord(raw)
    }
}
```

Run with:
```bash
go test -bench=. -benchmem ./...
```

---

## Makefile (optional but useful)

```makefile
.PHONY: fmt lint test cover build

fmt:
	gofmt -w .
	goimports -w .

lint:
	go vet ./...
	golangci-lint run

test:
	go test ./... -race -count=1

cover:
	go test ./... -coverprofile=cover.out
	go tool cover -func=cover.out

build:
	go build ./...

ci: fmt lint test
```
