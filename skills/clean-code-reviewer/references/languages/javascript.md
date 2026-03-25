# Clean Code Reviewer — JavaScript / TypeScript

Language-specific rules for applying clean coding standards to JavaScript/TypeScript code.
Read alongside the general standards in `prompts/coding/standards/clean_coding/`.
Default assumption: TypeScript with `strict: true`.

---

## Naming Violations

| Violation | Example | Rule |
|-----------|---------|------|
| Non-camelCase function/variable | `process_record`, `record_count` | Use `camelCase` in JS/TS |
| Non-PascalCase class/interface/type | `transactionProcessor`, `iRecordReader` | Use `PascalCase`; no `I` prefix on interfaces |
| `I` prefix on interface | `IRecordReader` | Drop the `I`: `RecordReader` |
| Abbreviation | `txn`, `cfg`, `res`, `req` | Reveal intent: `transaction`, `configuration`, `response`, `request` |
| Non-verb function | `const validation = () =>` | Functions are verbs: `validateRecord` |
| Generic callback names | `data`, `item`, `x` in `.map()/.filter()` | Name reveals what the element is: `transaction`, `record` |

---

## Function Violations

| Violation | TypeScript-Specific Signal |
|-----------|--------------------------|
| > 20 lines | Flag; check for multiple concerns |
| > 3 parameters | Introduce an options object type or interface |
| Missing return type annotation | Public functions must have explicit return types |
| `any` type | Use `unknown` and narrow; or a specific type |
| `async` function without `await` | Either remove `async` or add the missing `await` |
| Floating promise (no `await`, no `.catch`) | Always `await` or handle rejection — `@typescript-eslint/no-floating-promises` |
| Flag parameter | `process(record, isDryRun)` | Two functions: `processRecord()`, `dryRunRecord()` |

---

## Class Violations

| Violation | TypeScript-Specific Signal |
|-----------|--------------------------|
| Injecting concrete class instead of interface | `constructor(private reader: CsvReader)` | Depend on `RecordReader` interface |
| Mutable public property | `public count = 0` | Expose via getter; mutate via method |
| Missing `readonly` on injected deps | `private reader: RecordReader` | Should be `private readonly reader: RecordReader` |
| > 200 lines | Likely violating SRP |
| Methods that don't use `this` | Extract to module-level function |

---

## Error Handling Violations

| Violation | Example | Rule |
|-----------|---------|------|
| `throw "string"` | `throw "not found"` | Always throw an `Error` object or subclass |
| Empty `catch` block | `catch (e) {}` | Handle, log, or re-throw |
| `Promise` without rejection handling | `fetchData()` without `.catch()` or `try/catch` | All promises must be handled |
| Returning `null` / `undefined` as error signal | `return null` on failure | Throw or use `Result<T, E>` |
| Catching then returning `null` | `catch (e) { return null; }` | Signal failure explicitly |
| `.then()` and `await` mixed in one function | — | Use one style consistently per function |

---

## Smell Violations

| Smell | TypeScript-Specific Signal |
|-------|--------------------------|
| Magic number/string | `if (status === 3)`, `type === "TXN"` | Extract as `const` or `enum` |
| Type assertion abuse | `value as TransactionRecord` without guard | Add type guard function |
| `// @ts-ignore` or `// @ts-expect-error` | — | Fix the underlying type issue |
| Barrel file re-exporting everything | `export * from './internal'` | Only export the public API |
| `any[]` parameter | `process(items: any[])` | Type the array: `TransactionRecord[]` |
| `console.log` left in | — | Remove before merge; use structured logger |

---

## Size Reference (TypeScript)

| Unit | Max | Note |
|------|-----|------|
| Function body | 20 lines | Excluding signature |
| Class | 200 lines | Excluding blank lines and type declarations |
| File | 300 lines | Over this, look for module splits |
| Parameters | 3 | More → introduce an options object interface |
