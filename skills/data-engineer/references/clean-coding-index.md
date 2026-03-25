# Clean Coding Standards Index

All clean coding standards are sourced from `prompts/coding/standards/clean_coding/`. This index maps each concern to the authoritative document.

---

## Standard Documents

| Concern | Document | Key Rules |
|---------|----------|-----------|
| **Functions** | `clean_coding/functions.md` | < 20 lines, one thing, 0–3 args, no flag args, no side effects |
| **Classes** | `clean_coding/classes.md` | SRP, high cohesion, < 200 lines, depend on abstractions |
| **Naming** | `clean_coding/meaningful_names.md` | Reveal intent, no abbreviations, noun/verb conventions, searchable |
| **Error Handling** | `clean_coding/error_handling.md` | Exceptions not codes, no null returns, context in exceptions |
| **Comments** | `clean_coding/comments.md` | No redundant comments, no commented-out code, TODOs with owners |
| **Formatting** | `clean_coding/formatting.md` | Vertical separation, horizontal alignment, consistent style |
| **Objects & Data Structures** | `clean_coding/objects_and_data_structures.md` | Encapsulation, Law of Demeter, data/object asymmetry |
| **Boundaries** | `clean_coding/boundaries.md` | Third-party wrapping, learning tests, interface isolation |
| **Concurrency** | `clean_coding/concurrency.md` | Thread safety, single responsibility for concurrency, avoid shared data |
| **Emergence** | `clean_coding/emergence.md` | Run all tests, no duplication, expressive code, minimal abstractions |
| **Systems** | `clean_coding/systems.md` | Separate construction from use, dependency injection, AOP |
| **Smells & Heuristics** | `clean_coding/smells_and_heuristics.md` | Full smell catalogue: comments, environment, functions, general, names, tests |
| **Summary** | `clean_coding/clean_coding_standards.md` | One-page quick reference across all standards |
| **Full Reference** | `clean_coding/clean_coding_full_details.md` | Complete detail for all standards |

---

## Loading Order for Reviews

When reviewing code, apply standards in this priority order (highest impact first):

1. **Correctness** — does the code produce the right result? (not a clean coding check, but check first)
2. **Functions** — size, single responsibility, argument count
3. **Classes** — SRP, cohesion, dependency direction
4. **Naming** — intent-revealing names across all symbols
5. **Error handling** — exception patterns, null usage
6. **Smells & Heuristics** — duplication, dead code, magic numbers
7. **Comments** — redundancy, TODOs
8. **Formatting** — consistency
9. **Boundaries / Systems** — only for cross-component work
10. **Concurrency** — only when concurrency is present

---

## Loading Order for Refactoring

When refactoring, apply in this order to minimise rework:

1. **Naming** first — rename symbols before restructuring; renaming after restructuring is twice the work
2. **Functions** — extract methods to get functions below 20 lines and doing one thing
3. **Classes** — split classes after functions are clean; SRP violations are clearer once functions are right
4. **Error handling** — convert sentinel returns and null patterns
5. **Smells** — remove duplication, dead code, magic numbers last (they become visible once structure is clean)

---

## Deviation from Standards

This skill applies clean coding standards as written in the documents above. When working in a bclearer-specific context (e.g. `bclearer_orchestration_services` or `bclearer_interop_services`), the **bclearer code style** (`bie-data-engineer/references/code-style.md`) takes precedence for formatting and naming conventions — it is a stricter, project-specific instantiation of these general standards.

For general Python projects without a bclearer constraint, apply the standards as documented here.
