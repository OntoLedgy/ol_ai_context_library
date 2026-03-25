# Violation Report Template

Use this template for all `clean-code-reviewer` output.

---

```markdown
## Clean Code Review — [target_path]

**Language:** [python | javascript | csharp | rust]
**Mode:** [full | functions | classes | naming | errors | smells]
**Files reviewed:** [N]
**Total violations:** [N] (HIGH: N, MEDIUM: N, LOW: N)
**Severity threshold applied:** [low | medium | high | none]

---

### Violations

| # | File | Line | Rule | Severity | Description | Suggested Fix |
|---|------|------|------|----------|-------------|---------------|
| 1 | | | | | | |

---

### Summary by Category

| Category | HIGH | MEDIUM | LOW | Total |
|----------|------|--------|-----|-------|
| Functions | | | | |
| Classes | | | | |
| Naming | | | | |
| Error Handling | | | | |
| Smells | | | | |
| **Total** | | | | |

---

### Key Issues (HIGH severity only)

1. [Most important issue — one sentence]
2. ...

---

### Verdict

**[APPROVE / REQUEST CHANGES / REJECT]**

Criteria:
- APPROVE: no HIGH violations; MEDIUM violations are minor or isolated
- REQUEST CHANGES: HIGH violations present but code is functional and salvageable
- REJECT: pervasive violations; code requires structural redesign before clean coding fixes

[1–2 sentence overall assessment. Be specific: name the files and patterns that drove the verdict.]

---

### Recommended Next Step

[Choose the most appropriate]:

**For code-level violations only (naming, function size, smells):**
> Pass this report to `clean-code-refactor` with `mode=[most critical mode]`.

**For structural violations (wrong class responsibilities, missing abstractions, wrong dependency direction):**
> Pass this report to `software-architect` Review Mode to design the target structure,
> then implement via `[language]-data-engineer` Implement Mode using the architect's design as spec.

**For both:**
> 1. `software-architect` Review Mode → target architecture design
> 2. `[language]-data-engineer` Implement Mode → structural changes per architect's design
> 3. `clean-code-reviewer` → re-scan to confirm structural violations resolved
> 4. `clean-code-refactor` → fix remaining code-level violations
```
