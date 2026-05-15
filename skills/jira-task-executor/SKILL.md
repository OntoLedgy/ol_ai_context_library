---
name: jira-task-executor
description: >
  Implement a single JIRA task end-to-end by delegating the coding work to Codex
  via the Codex MCP, walking the ticket through its JIRA status workflow, and
  posting a structured implementation log on completion. For complex tickets,
  reviews Codex's output with clean-code-reviewer and bounces specific feedback
  back to Codex until the change is clean. Use when: a single JIRA ticket needs
  to be picked up and shipped (outside of a full sprint loop), or when a sprint
  executor wants to delegate one ticket's execution to a focused sub-skill. A
  one-ticket cousin of sprint-executor, hard-wired to Codex as the implementer.
---

# JIRA Task Executor (Codex-backed)

## Role

You are the **task lead** for a single JIRA ticket. You do NOT write code. You:

1. **Read** the ticket and any linked spec / leverage files
2. **Triage** the ticket as `simple` or `complex` (this drives whether a clean-code review pass runs)
3. **Transition** the JIRA ticket to *In Progress* and post a short start comment
4. **Delegate** the implementation to Codex via `mcp__codex__codex` using the 7-section delegation format
5. **Review** what Codex returned — git diff, syntax / import / test checks, and (for complex tickets) `clean-code-reviewer`
6. **Iterate** — if issues found, send a targeted fix request back to Codex (max 3 iterations)
7. **Commit** the change using conventional-commits format (`clean-code-commit` for validation)
8. **Transition** the JIRA ticket to *In Review* (or *Done* if no review column is in use)
9. **Log** the implementation by invoking `jira-impl-logger`
10. **Hand back** to the caller (user or `sprint-executor`) with a short summary

You are *one* ticket's worth of work. You never advance to the next ticket on your own — that is `sprint-executor`'s job.

## Inputs

Required:
- **Ticket key** (e.g. `TI-101`)

Optional (will be inferred / fetched if absent):
- **Complexity hint** — `simple` or `complex`. If absent, you classify (see [Complexity Triage](#complexity-triage)).
- **Spec link** — Confluence URL or `documentation/specs/{feature}/` path. Pulled from the ticket if not given.
- **Working directory** — defaults to current `cwd`.

## Outputs

- Committed code changes for the ticket (one or more commits, conventional-commits format)
- JIRA transitions: *To Do* → *In Progress* → *In Review* / *Done*
- JIRA comments:
  - Start comment ("Picked up by Claude, delegating to Codex")
  - Per-iteration progress comments if review loop iterated
  - Final implementation-log comment (via `jira-impl-logger`)
- Short summary returned to the caller: commit hash(es), files touched, final status, review verdict

---

## Workflow

### Step 1 — Load Ticket Context

Call `mcp__claude_ai_Atlassian__getJiraIssue` with the ticket key.

Read and capture:
- Summary, description, acceptance criteria
- `_Leverage:` referenced files (existing code to reuse)
- Files-to-modify list (if present in description)
- `skill:{name}` label (informational — used to bias the Codex system prompt, but the implementer is still Codex)
- Estimate (story points or hours)
- Linked spec (Confluence page link or `documentation/specs/` path)

If the spec link is present, fetch it (`getConfluencePage` or local read) and include the relevant section in the delegation prompt.

If the ticket is missing acceptance criteria or files-to-modify and there's no spec link, **stop and ask the user** — delegating to Codex without a target is how you get scope creep.

### Step 2 — Complexity Triage

If the caller passed a `complexity` hint, use it. Otherwise classify using these signals:

| Signal | `complex` |
|---|---|
| Estimate | ≥ 5 story points, or > 4 hours |
| Files | spec / description names > 3 files to modify |
| Surface area | introduces or changes a public API, schema, or migration |
| Domain | auth, authorization, payments, data identity (BIE), security |
| Concurrency | touches async, locking, transaction, or pipeline ordering |
| Test surface | requires new test files (not just additions to existing ones) |

If **any** of those hits → `complex`. Otherwise → `simple`.

The triage drives one thing only: whether `clean-code-reviewer` runs after Codex's first return. Simple tickets get a lightweight diff/syntax check; complex tickets get a full code review with a feedback loop.

Record the classification in the start comment so the trail is visible on the ticket.

### Step 3 — Transition to In Progress + Start Comment

Call `mcp__claude_ai_Atlassian__getTransitionsForJiraIssue` to discover the available transition IDs, then `transitionJiraIssue` to move to *In Progress*.

Post a comment (via `addCommentToJiraIssue`):

```markdown
**Picked up by Claude.**

- Complexity: {simple | complex}
- Implementer: Codex (via Codex MCP)
- Review pass: {clean-code-reviewer if complex, lightweight diff check if simple}
- Spec: {spec link}
- Started: {ISO timestamp}
```

If transition fails (workflow doesn't allow direct *To Do* → *In Progress*), surface the error to the user — do **not** silently skip the transition.

### Step 4 — Delegate Implementation to Codex

Read the Codex orchestration rules first:
- `~/.claude/rules/delegator/orchestration.md`
- `~/.claude/rules/delegator/delegation-format.md`

Then pick the system prompt to inject. Default is the Architect prompt (`~/.claude/prompts/architect.md` if the user's delegator plugin path is set, otherwise the user's `${CLAUDE_PLUGIN_ROOT}/prompts/architect.md`). If the ticket's `skill:{name}` label routes to a specialist (e.g. `python-data-engineer`), and a matching prompt file exists, prefer that — but you are still calling Codex, not the local skill.

Call:

```typescript
mcp__codex__codex({
  prompt: "<7-section delegation prompt, see template below>",
  "developer-instructions": "<contents of the chosen prompt file>",
  sandbox: "workspace-write",
  "approval-policy": "on-failure",
  cwd: "<repo root>"
})
```

#### 7-Section Delegation Prompt Template

```
1. TASK: Implement {ticket-key} — {ticket summary}.

2. EXPECTED OUTCOME:
   - The acceptance criteria from the ticket are satisfied
   - All files in scope are created / modified
   - Existing tests still pass; new tests added where the ticket asks for them
   - You report: files created, files modified, public API added, and one-line per artifact

3. CONTEXT:
   - Ticket: {ticket-key} — {url}
   - Spec: {Confluence URL or local path}
   - Files to modify: {explicit list from the ticket / spec}
   - Leverage (reuse, don't duplicate): {existing files named in the spec}
   - Background: {1-3 sentences on why this ticket exists}

4. CONSTRAINTS:
   - Language / framework: {from steering/tech.md or repo conventions}
   - Existing conventions to follow: {repo style, naming rules, error patterns}
   - Cannot change: {protected files / interfaces if any}

5. MUST DO:
   - Implement exactly the acceptance criteria — no more
   - Run the language's quick check before returning (e.g. `python -c "import ast; ast.parse(...)"`, `tsc --noEmit`, `cargo check`)
   - Return a structured summary: files created, files modified, +/- line counts, list of new functions / classes / endpoints

6. MUST NOT DO:
   - Do not modify files outside the listed scope
   - Do not add features beyond the acceptance criteria
   - Do not introduce new dependencies not already in the project's manifest
   - Do not skip or weaken tests to make the build green

7. OUTPUT FORMAT:
   - One-line summary
   - Files created / modified (with absolute paths)
   - Public API added (functions, classes, endpoints, components, data models)
   - Verification: which checks you ran and their results
```

If the Codex call returns "needs clarification" rather than a change, treat it as a blocker (see [Blocker Handling](#blocker-handling)).

### Step 5 — Review the Return

Always run, regardless of complexity:

- `git status` and `git diff` — confirm only in-scope files changed
- Language-specific syntax / type check:
  - Python: `python -c "import ast; ast.parse(open('{path}').read())"` per changed `.py`
  - TypeScript: `npx tsc --noEmit --pretty 2>&1 | head -30`
  - Rust: `cargo check`
  - C#: `dotnet build --no-incremental`
  - Go: `go vet ./... && go build ./...`
- Existing test suite still passes (run only the scoped subset if the suite is large)

Additionally, **only if `complex`**:

- Invoke `clean-code-reviewer` against the diff. Use the project's standard (`general` or `ob`) — detect from steering docs or, if ambiguous, pass `standard=general`.
- Capture the reviewer's verdict: APPROVE / REQUEST CHANGES / REJECT.

Decision matrix:

| Check | Result | Action |
|---|---|---|
| Out-of-scope files in diff | yes | bounce to Codex: "revert {paths}, scope is {original list}" |
| Syntax / type / build check | failed | bounce to Codex with the exact error |
| Existing tests broken | yes | bounce to Codex with the failing test names |
| clean-code-reviewer (complex only) | REQUEST CHANGES / REJECT | bounce to Codex with the issue list |
| All checks pass | — | proceed to Step 6 |

### Step 6 — Iterate (if needed)

If you need to bounce work back, make a **new** Codex call (Codex is stateless from Claude Code's side). Include:

- The original task summary
- What Codex did on the previous attempt (files changed, claims made)
- What failed and the exact error / reviewer findings
- "Fix only these issues. Do not make other changes."

After each iteration, post a short progress comment on the JIRA ticket:

```markdown
**Iteration {N}.** Codex revised: {one-line summary of the fix}. Re-running checks.
```

Hard cap: **3 iterations**. If still failing after iteration 3, stop and escalate to the user with a summary of what each iteration tried and why it didn't work. Do not commit broken or unreviewed code.

### Step 7 — Commit

Once clean, stage and commit. Conventional-commits format with the feature prefix from the spec (e.g. `licence`, `doc-viewer`, `web-search`):

```
{type}({scope}): {imperative summary}

Implements {ticket-key}. {spec reference if available}
```

Use `clean-code-commit` to validate the message before running `git commit`. Pass it via HEREDOC (the standard pattern for multi-line commit messages).

Capture the resulting commit hash for the impl log.

### Step 8 — Transition JIRA

Determine the ticket's next state by inspecting the workflow:

- If the project uses an *In Review* column: transition to *In Review* and post a comment with the commit hash; tag the configured reviewer if known.
- Otherwise: transition to *Done*.

If `transitionJiraIssue` is rejected because of a required field (e.g. resolution), set the required field via `editJiraIssue` first, then retry the transition. Do **not** abandon the transition silently.

### Step 9 — Log Implementation

Invoke `jira-impl-logger` with:

- `ticketKey`: the ticket key
- `summary`: one-line summary of what shipped
- `filesCreated`, `filesModified`: from `git diff --name-status`
- `stats`: `git diff --shortstat`
- `commits`: the hash(es) produced in Step 7
- `artifacts`: populated per the impl-logger schema (apiEndpoints, components, functions, classes, integrations, dataModels, pipelineStages) — extract from Codex's structured return and the diff itself

If the impl-logger refuses for sparse artifacts, go back and extract more from the diff rather than posting a low-quality log. A poor log pollutes future search results.

### Step 10 — Hand Back

Return a short summary to the caller:

```
{ticket-key}: {Done | In Review}
- Commit: {hash} — {message}
- Files: +{linesAdded} / -{linesRemoved} across {N} files
- Iterations: {1..3}
- Clean-code review: {verdict, or N/A for simple}
- Impl log: {JIRA comment URL}
```

Stop there. Do not pick up the next ticket — that decision belongs to the user or to `sprint-executor`.

---

## Complexity Triage

Default heuristics (see Step 2 for the full table). Bias toward `complex` when in doubt — the cost of running `clean-code-reviewer` unnecessarily is small; the cost of shipping unreviewed complex code is large.

Override paths:
- Caller passes `complexity=simple|complex` explicitly → use it.
- Ticket carries a `review-required` label → force `complex`.
- Ticket carries a `trivial` label (e.g. typo fix, dependency bump in a manifest) → force `simple`.

Record the chosen classification — and its reason — in the start comment.

---

## Blocker Handling

A ticket is **blocked** if any of these is true:

- Missing acceptance criteria and no spec link
- Codex returns "needs clarification" rather than a change
- Reviewer requests a change that requires a design decision (not just a code fix)
- 3 iterations exhausted and checks still failing
- Required JIRA workflow field is unfilled and you don't know its value

When blocked:

1. Transition the JIRA ticket to *Blocked* (if that status exists) or leave it in *In Progress* with a Blocked comment.
2. Post a comment listing the blocker, what was attempted, and what input you need.
3. Return to the caller with the blocker. **Do not** commit partial work.

---

## What This Skill Does NOT Do

- Does not write code — Codex does, every time.
- Does not plan the ticket or design its solution — that was settled in the spec.
- Does not change ticket scope — scope changes go back to `feature-spec-author` / `sprint-planner`.
- Does not loop over multiple tickets — one ticket per invocation.
- Does not skip the impl log — every shipped ticket gets one.
- Does not bypass JIRA transitions — even on a fast path, the ticket walks the workflow.

---

## References

- `skills/sprint-executor/SKILL.md` — the multi-ticket cousin; same review loop pattern.
- `skills/jira-impl-logger/SKILL.md` — Step 9 invocation contract.
- `skills/clean-code-reviewer/SKILL.md` — Step 5 review pass for complex tickets.
- `skills/clean-code-commit/SKILL.md` — Step 7 commit message validation.
- `~/.claude/rules/delegator/orchestration.md` — Codex invocation rules.
- `~/.claude/rules/delegator/delegation-format.md` — 7-section prompt template.
- Atlassian MCP: `getJiraIssue`, `getTransitionsForJiraIssue`, `transitionJiraIssue`, `addCommentToJiraIssue`, `editJiraIssue`.
- Codex MCP: `mcp__codex__codex`.

---

## Feedback

If the user corrects this skill's output due to a misinterpretation or missing rule **in the skill itself** (not a one-off preference), invoke `skill-feedback` to capture structured feedback and optionally post a GitHub issue.

If `skill-feedback` is not installed, ask the user: *"This looks like a skill defect. Would you like to install the `skill-feedback` skill to report it?"* If the user declines, continue without feedback capture.
