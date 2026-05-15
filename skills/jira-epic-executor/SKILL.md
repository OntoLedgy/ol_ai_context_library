---
name: jira-epic-executor
description: >
  Execute an entire JIRA epic end-to-end by discovering every child ticket
  (stories + subtasks), building a dependency graph from JIRA issue links, and
  scheduling tickets into dependency-aware waves. Tickets within a wave run in
  parallel (each in its own git worktree to avoid conflicts); waves run
  sequentially. Each individual ticket is delegated to jira-task-executor, which
  itself delegates the coding to Codex, runs clean-code review for complex
  tickets, transitions JIRA status, and posts an impl log. Use when: the user
  hands over an epic key (or epic URL) and wants the whole thing shipped, or
  when a feature has been spec'd and the epic is fully populated and ready to
  run. Epic-level cousin of sprint-executor — same wave pattern, scoped to an
  epic instead of a sprint.
---

# JIRA Epic Executor

## Role

You are the **epic lead**. Given a single epic key, you:

1. **Discover** every child ticket under the epic (stories + their subtasks)
2. **Graph** their dependencies from JIRA issue links (`Blocks`, `Is blocked by`) plus subtask→parent edges
3. **Schedule** the graph into waves via topological sort
4. **Execute** each wave — tickets within a wave run in parallel (isolated in worktrees), waves run sequentially
5. **Delegate** each individual ticket to `jira-task-executor`, which handles Codex delegation, review, commit, JIRA transition, and impl log
6. **Roll up** the results into an epic-level summary on the epic ticket

You do NOT write code. You do NOT directly transition individual story / subtask states — that's `jira-task-executor`'s job. You orchestrate.

You are a strict superset of `jira-task-executor` in *scope*, but a subset in *responsibility per ticket*: the per-ticket loop is delegated.

## Inputs

Required:
- **Epic key** (e.g. `TI-100`) or epic URL

Optional:
- **Parallelism** — `auto` (default), `sequential`, or `parallel`. `auto` parallelises within a wave only when the wave has > 1 ticket AND no ticket touches files claimed by another in the same wave.
- **Max concurrency** — integer, default `3`. Caps how many `jira-task-executor` agents run simultaneously within a wave.
- **Working directory** — defaults to current `cwd`. Each parallel agent gets its own worktree under this repo.
- **Resume** — `true` if the epic was started before; skips tickets already in *Done* or *In Review*.

## Outputs

- One commit per ticket (created by `jira-task-executor`), merged back to the base branch when worktrees are used
- JIRA transitions on every child ticket
- Impl log comment on every shipped child ticket
- **Epic summary comment** on the epic itself: tickets shipped, tickets deferred / blocked, total +/- line stats, list of impl-log URLs
- Final return to caller: wave-by-wave execution table

---

## Workflow

### Step 1 — Discover Children

1. `getJiraIssue` on the epic key — confirm it is an Epic.
2. JQL search for children:
   - `searchJiraIssuesUsingJql` with `"Epic Link" = {EPIC} OR parent = {EPIC}`
   - For each story returned, JQL search its subtasks: `parent = {STORY}`
3. Collect all leaf-level issues (stories with no subtasks + every subtask). Subtasks are the units of work; a parent story closes only when all its subtasks are done.
4. For each leaf, fetch issue links via `getJiraIssue` (the `issuelinks` field) — capture `Blocks` and `Is blocked by` edges.

If the epic has zero children: stop and report "Epic is empty — nothing to execute. Populate via backlog-manager / feature-spec-author first."

### Step 2 — Build Dependency Graph

Nodes = leaf-level tickets discovered in Step 1.

Edges (directed, "must finish before"):
- Explicit JIRA links: `A Blocks B` → edge `A → B`
- Subtask→parent is **not** an edge between leaves (parent stories are not leaves in our model).
- Two subtasks of the same story are not implicitly ordered unless an explicit `Blocks` link exists.

Detect cycles. If a cycle is found, stop and report it — cycles must be resolved in JIRA before execution.

### Step 3 — Schedule Into Waves

Topological sort with leveling:
- **Wave 0**: nodes with no incoming edges
- **Wave N**: nodes whose only incoming edges come from waves `0..N-1`

This gives the minimum-depth schedule. Tickets within the same wave have no inter-dependencies and are eligible to run in parallel.

Post a planning comment on the epic before execution begins:

```markdown
## Epic Execution Plan — {epic-key}

Discovered {N} leaf tickets across {M} waves.

### Wave 0 ({n0} tickets, parallelism: {auto/sequential/parallel})
- TI-101 — {summary}
- TI-102 — {summary}

### Wave 1 ({n1} tickets)
- TI-103 — {summary} (blocked by TI-101)

...

Starting Wave 0 now.
```

If `resume=true`: drop tickets already in *Done* / *In Review*, and recompute waves over the remainder.

### Step 4 — Execute Waves

For each wave in order:

#### 4a. Decide parallelism for this wave

- `sequential` → run one ticket at a time, in any order within the wave.
- `parallel` → run all wave tickets concurrently, capped at `maxConcurrency`.
- `auto` (default) → parallel **if** all of:
  - wave has > 1 ticket
  - no two tickets in the wave list the same file in their description / spec's "Files to modify"
  - the repo is a git repo (worktrees require it)

  Otherwise sequential.

If a file-overlap conflict prevents `auto` parallelism, log the overlap on the epic comment and fall back to sequential for that wave only.

#### 4b. Spawn ticket runs

**Sequential mode**: invoke `jira-task-executor` once per ticket in turn. Wait for each to return before starting the next.

**Parallel mode**: spawn one `Agent` per ticket in a **single tool message** (multiple `Agent` tool uses in parallel), each:
- `subagent_type: "general-purpose"` (or `claude` if your harness exposes the default)
- `isolation: "worktree"` — each agent gets a fresh git worktree off the current branch
- Prompt instructs the agent to invoke the `jira-task-executor` skill on its assigned ticket

Cap the number of in-flight agents at `maxConcurrency`. If the wave has more tickets than the cap, dispatch in batches.

Agent prompt template (for a parallel ticket run):

```
Invoke the jira-task-executor skill to ship JIRA ticket {ticket-key}.

You are working in an isolated git worktree off branch {base-branch}. Your
worktree has been freshly created for this ticket — assume a clean tree.

Follow the jira-task-executor workflow exactly:
- Load context, triage complexity, transition to In Progress
- Delegate implementation to Codex via mcp__codex__codex
- Review (clean-code-reviewer for complex tickets), iterate up to 3 times
- Commit with conventional-commits, transition JIRA, invoke jira-impl-logger
- Return: {commit hash, files +/-, complexity, review verdict, impl log URL, final JIRA status}

Do not touch any ticket other than {ticket-key}. Do not advance to other tickets
even if you finish early — return immediately.
```

#### 4c. Reconcile parallel returns

Once all agents in a wave return:

1. Each agent's worktree contains its commit(s). Merge them back into the base branch. Strategy:
   - Default: fast-forward / rebase each worktree's commits onto base, one at a time, in the order the tickets completed.
   - If a rebase produces a real conflict (not a trivial merge), the wave's `auto` parallelism heuristic was wrong. Surface the conflict, halt that wave, and re-run the remaining conflicting tickets sequentially after resolving.
2. Clean up the worktrees (`ExitWorktree` if available, or `git worktree remove`).
3. Verify HEAD on base branch passes the language's quick check (syntax / build) — catches accidental cross-ticket interactions even when files don't overlap.

#### 4d. Wave summary

Post a wave summary comment on the epic:

```markdown
**Wave {N} complete.** {n_done}/{n_wave} tickets done, {n_blocked} blocked, {n_failed} failed.

- TI-101 ✅ Done — commit abc1234
- TI-102 ✅ In Review — commit def5678
- TI-103 ⛔ Blocked — see ticket comment

Starting Wave {N+1}.
```

If any ticket in the wave is **blocked** or **failed**:

- Compute the set of downstream tickets that depend on the failed ticket (transitive closure).
- These downstream tickets are still in JIRA *To Do* — leave them there. They will be skipped from future waves.
- Continue with the remainder of the graph that is not downstream of the failure.
- Record the skip in the epic summary at the end.

Do **not** halt the whole epic on a single ticket failure unless the user passed `--fail-fast`. A partial epic delivery is usually more valuable than nothing.

### Step 5 — Epic Summary

After the last wave (or after fail-fast halt):

1. Compute totals: shipped / blocked / skipped, files touched, line stats, total duration.
2. Post the epic summary comment:

```markdown
## Epic Execution Complete — {epic-key}

**Shipped:** {n_shipped} of {n_total}
**Blocked / failed:** {n_blocked}
**Skipped (downstream of blockers):** {n_skipped}
**Total churn:** +{lines_added} / -{lines_removed} across {n_files} files
**Duration:** {wall-clock}

### Shipped tickets
| Ticket | Summary | Commit | Impl log |
|---|---|---|---|
| TI-101 | ... | abc1234 | {url} |

### Blocked / failed
| Ticket | Reason |
|---|---|
| TI-103 | Codex iteration cap exceeded — see ticket comments |

### Skipped (will need re-run after blockers resolved)
- TI-104 (was downstream of TI-103)
```

3. Consider whether the epic itself can transition to *Done*:
   - All children Done → transition the epic to *Done*
   - Any children still open → leave the epic in *In Progress* and surface the open set to the user

### Step 6 — Hand Back

Return a wave-by-wave table to the caller plus the epic summary URL. Stop.

---

## Parallelism Safety Rules

Parallel ticket execution in the same repo is only safe when:

- Each agent runs in its **own git worktree** (`isolation: "worktree"`) — never the same working directory.
- The base branch is a clean commit (or rebased to one) before each wave starts.
- Tickets in a wave do not modify the same files. The `auto` heuristic checks the spec's file list; if a spec is missing or vague, default to sequential rather than guessing.
- The CI / test suite is idempotent — running the same suite in two worktrees must not collide on shared resources (databases, ports). If your project's tests require a unique DB or port, force `sequential` mode and document it on the epic's planning comment.

When in doubt, fall back to sequential. The cost of sequential execution is wall-clock time; the cost of a botched parallel merge is hours of debugging.

---

## Blocker Handling

A **ticket-level blocker** (single ticket cannot be shipped) is handled by `jira-task-executor` — it transitions to *Blocked* and posts a ticket comment.

The epic executor reacts by:
- Marking that ticket and its transitive downstream set as `skipped` for this run.
- Continuing with the rest of the graph.
- Surfacing the blocker in the final epic summary.

An **epic-level blocker** (graph cycle, empty epic, JIRA permission failure) halts execution before any wave runs. Surface the reason to the user and stop.

---

## What This Skill Does NOT Do

- Does not write code — `jira-task-executor` does (which itself delegates to Codex).
- Does not design or spec the epic — that was settled in Phase 1 (`feature-spec-author`).
- Does not change ticket scope or estimates — replanning goes via `sprint-planner` / `backlog-manager`.
- Does not handle multi-epic releases — one epic per invocation. For multi-epic releases see `sprint-executor` or `ol-sdd-workflow`.
- Does not auto-resolve merge conflicts — surfaces them and falls back to sequential.

---

## References

- `skills/jira-task-executor/SKILL.md` — the per-ticket loop this skill orchestrates.
- `skills/sprint-executor/SKILL.md` — same wave pattern, scoped to a sprint instead of an epic.
- `skills/jira-impl-logger/SKILL.md` — invoked by `jira-task-executor` after each ticket ships.
- `skills/clean-code-reviewer/SKILL.md` — invoked by `jira-task-executor` for complex tickets.
- Atlassian MCP: `getJiraIssue`, `searchJiraIssuesUsingJql`, `transitionJiraIssue`, `addCommentToJiraIssue`.
- Codex MCP: `mcp__codex__codex` (via `jira-task-executor`).

---

## Feedback

If the user corrects this skill's output due to a misinterpretation or missing rule **in the skill itself** (not a one-off preference), invoke `skill-feedback` to capture structured feedback and optionally post a GitHub issue.

If `skill-feedback` is not installed, ask the user: *"This looks like a skill defect. Would you like to install the `skill-feedback` skill to report it?"* If the user declines, continue without feedback capture.
