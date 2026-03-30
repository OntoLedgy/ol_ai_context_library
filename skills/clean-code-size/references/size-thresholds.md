# Clean Code Size Thresholds

Use these thresholds as the default triage gates for `clean-code-size`.

These are soft limits. A file over the limit is a review candidate, not an automatic
failure. The real question is whether the file mixes multiple responsibilities that
should become separate components.

## Default Thresholds

| Language | Extensions | Default Threshold | Source | Notes |
|----------|------------|-------------------|--------|-------|
| Python | `.py` | 500 non-blank lines | `skills/clean-code-reviewer/references/languages/python.md` | Matches the Python module soft limit |
| JavaScript / TypeScript | `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs` | 300 non-blank lines | `skills/clean-code-reviewer/references/languages/javascript.md` | Matches the file soft limit |
| C# | `.cs` | 250 non-blank lines | Derived from the C# "one primary type per file" rule plus the 200-line class limit | Treat as a heuristic; inspect type boundaries before recommending a split |
| Rust | `.rs` | 250 non-blank lines | Derived from the 200-line `impl` guidance in the Rust review reference | Treat as a heuristic; check whether the file contains multiple responsibilities or just one large type |
| Unknown / mixed | any other supported file | 300 non-blank lines | Skill heuristic | Use only when language-specific guidance is unavailable |

## Interpretation Rules

- Use non-blank line count as the primary size signal.
- Use total line count as secondary context only.
- Large test files can be exempt if they are intentionally declarative and structurally
  consistent.
- Generated code, schema dumps, registries, and long constant maps are usually exempt.
- When a file is only slightly over the threshold, inspect responsibility count before
  recommending a split.
- When a file is far over the threshold, assume decomposition is likely unless the file is
  intentionally data-only.

## What to Do After a File Trips the Threshold

1. Read the file fully.
2. Identify responsibility clusters.
3. Decide whether the issue is:
   - an in-file cleanup for `clean-code-refactor`, or
   - a structural split requiring `software-architect` guidance.
4. For structural splits, propose a target module/component breakdown before any code
   changes are made.
