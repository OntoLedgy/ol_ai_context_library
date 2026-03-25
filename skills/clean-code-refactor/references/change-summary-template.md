# Change Summary Template

Use this template for all `clean-code-refactor` output.

---

```markdown
## Clean Code Refactor — [target_path]

**Language:** [python | javascript | csharp | rust]
**Mode:** [full | functions | classes | naming | errors | smells]
**Apply mode:** [propose | apply]
**Files modified:** [N]
**Violations fixed:** [N] (HIGH: N, MEDIUM: N, LOW: N)
**Violations flagged (out of scope):** [N]

---

### Changes

[Repeat for each fix:]

#### [filename:line] [Category]: [short description]

**Rule:** [The specific clean coding rule being fixed]
**Severity:** [HIGH | MEDIUM | LOW]

**Before:**
```[language]
[original code]
```

**After:**
```[language]
[refactored code]
```

**Rationale:** [One sentence — why this change makes the code better]

---

### Flagged (structural — not fixed)

| # | File | Line | Violation | Why Not Fixed | Recommended Next Step |
|---|------|------|-----------|--------------|----------------------|
| 1 | | | | Requires module split | `software-architect` Review Mode → `[language]-data-engineer` Implement Mode |

---

### Verification

Run these commands to confirm nothing was broken:

[Python:]
```bash
ruff check src/
mypy src/
pytest
```

[JavaScript/TypeScript:]
```bash
tsc --noEmit
eslint src/
vitest run
```

[C#:]
```bash
dotnet build --warningsaserrors
dotnet test
```

[Rust:]
```bash
cargo clippy -- -D warnings
cargo test
```

---

### What Was NOT Changed

[List anything in scope that was deliberately left unchanged, and why. This prevents
reviewers from assuming it was missed.]

Example:
- `legacy_transform()` in `processor.py` — naming violation present but function is
  called from 12 external modules; rename requires coordinated change outside this scope
```
