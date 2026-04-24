# Skill Feedback Issue Template

Use this template when posting a GitHub issue via the `skill-feedback` skill.

---

## Title Format

```
skill({skill_name}): {imperative one-line summary}
```

Examples:
- `skill(clean-code-naming): reject plural class names when standard=general`
- `skill(feature-spec-author): include release epic key in task cross-references`
- `skill(ob-engineer): apply single-quote rule to f-strings`

---

## Labels

- `skill-feedback` (always)
- `skill:{skill_name}` (e.g., `skill:clean-code-naming`)

---

## Body

````markdown
## Skill Feedback Report

**Skill:** `{skill_name}`
**Skill file:** `skills/{skill_name}/SKILL.md` @ `{short_commit_hash}`
**Reporter:** {name_or_handle | "Anonymous skill user"}

---

### What happened

{1-3 sentences describing the skill's actual output or behaviour}

### What was expected

{1-3 sentences describing the correct output or behaviour}

### Root Cause Analysis

**File:** `{path_to_skill_file_or_reference}`
**Section:** {heading or rule name}

**Current text:**
> {quote the relevant section, or "Section does not exist (missing rule)"}

**Problem:** {explain why this text causes incorrect behaviour}

### Suggested Fix

{One of:}

**Option A — Amend existing text:**
Replace:
> {old text}

With:
> {new text}

**Option B — Add new rule:**
Add the following under `{section heading}`:
> {new rule text}

**Option C — Structural change:**
{Describe the structural change needed, e.g., "Add a new reference file for X",
"Split section Y into two sections"}

---

### Reproduction

**Input given to skill:**
```
{summarise the input parameters}
```

**Skill output (excerpt):**
```
{relevant excerpt of the skill's output}
```

**Expected output (excerpt):**
```
{what the output should have been}
```

---

### Impact

- **Severity:** {low | medium | high} — {rationale}
- **Frequency:** {one-off edge case | common scenario | always}
- **Affected users:** {who would hit this — e.g., "anyone using standard=ob with Python"}

---

*Posted via `skill-feedback` skill*
````
