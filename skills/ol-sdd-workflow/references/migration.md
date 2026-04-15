# Migration Guide — Legacy Spec Locations → `documentation/`

How to migrate a project that has spec/steering/sprint artifacts in legacy locations (`.spec-workflow/` from the upstream spec-workflow-mcp, or `.claude/` from earlier ol-sdd-workflow versions) to the current canonical layout under `documentation/`.

## Canonical layout (current)

```
your-repo/
└── documentation/
    ├── workflow-config.md
    ├── steering/
    │   ├── product.md
    │   ├── tech.md
    │   └── structure.md
    ├── releases/
    │   └── {release-name}/
    │       ├── features.md
    │       └── epic-map.md
    ├── specs/
    │   └── {feature-name}/
    │       ├── requirements.md
    │       ├── design.md
    │       ├── tasks.md
    │       └── ticket-map.md
    └── sprints/
        └── sprint-{N}-kickoff.md
```

## Legacy layouts the migration handles

### Source A — upstream spec-workflow-mcp (`.spec-workflow/`)

```
your-repo/
└── .spec-workflow/
    ├── approvals/          (approval records — history, can be archived)
    ├── archive/            (completed specs)
    ├── specs/              (active specs, same internal shape)
    ├── steering/           (steering docs)
    ├── templates/          (vendor templates — do NOT copy; we have our own)
    ├── user-templates/     (user-custom templates — archive)
    └── config.example.toml (config — translate to documentation/workflow-config.md)
```

### Source B — earlier ol-sdd-workflow (`.claude/`)

```
your-repo/
└── .claude/
    ├── workflow-config.md
    ├── steering/
    ├── specs/
    ├── releases/           (only if the project used Phase 0.5)
    ├── sprints/
    └── bugs/               (legacy bug specs; optional)
```

## Invocation

```
You: "use ol-sdd-workflow to migrate legacy spec locations to documentation/"
```

or explicitly:

```
You: "migrate .spec-workflow/ to documentation/"
You: "migrate .claude/ specs to documentation/"
```

## Migration steps

The orchestrator runs these steps, surfacing each plan for user approval before touching any files.

### Step 1 — Detect source

Scan the repo root for any of:
- `.spec-workflow/` directory → Source A
- `.claude/steering/` or `.claude/specs/` → Source B
- Both → run Source A first, then Source B

If neither is present, report "no legacy layout detected" and exit.

If `documentation/` already exists with content, ask the user whether to merge (keep existing, add new from legacy) or abort.

### Step 2 — Map and preview

Produce a migration plan showing every move:

```
Migration Plan:
  .spec-workflow/steering/product.md       →  documentation/steering/product.md
  .spec-workflow/steering/tech.md          →  documentation/steering/tech.md
  .spec-workflow/specs/licence-ext/        →  documentation/specs/licence-ext/
  .spec-workflow/archive/                  →  documentation/archive/
  .spec-workflow/approvals/                →  documentation/archive/approvals/  (archived)
  .spec-workflow/templates/                →  [skipped — use prompts/coding/templates/]
  .spec-workflow/user-templates/           →  documentation/archive/user-templates/
  .spec-workflow/config.example.toml       →  documentation/workflow-config.md  (translated)

  .claude/steering/                        →  documentation/steering/  (merge with above)
  .claude/specs/                           →  documentation/specs/     (merge with above)
  .claude/sprints/                         →  documentation/sprints/
  .claude/releases/                        →  documentation/releases/
  .claude/bugs/                            →  documentation/bugs/      (if used)
  .claude/workflow-config.md               →  documentation/workflow-config.md  (merge)

Files unchanged: 3
Files moved: 42
Files translated: 1 (config)
Files skipped (vendor templates): 5
```

**Gate: user approves the plan before any files are moved.**

### Step 3 — Dry-run check

Before moving anything:
- Verify every source file is readable and non-empty
- Verify no destination file would be silently overwritten. If a collision exists (both legacy and current layouts have the same spec), stop and ask: "both `.claude/specs/foo/tasks.md` and `documentation/specs/foo/tasks.md` exist — which do you want to keep? Or should I rename the legacy one to `-legacy` and keep both?"
- Verify git working tree is clean (so the migration is a single reviewable commit)

If the working tree has uncommitted changes, ask the user to commit or stash first — migrations should always be isolated commits for reviewability.

### Step 4 — Execute with `git mv`

Use `git mv` (not `mv`) so git tracks the rename rather than seeing it as delete-then-add. This preserves file history for every migrated file.

```
git mv .spec-workflow/steering/product.md documentation/steering/product.md
git mv .spec-workflow/specs/licence-ext documentation/specs/licence-ext
# ... etc
```

For whole-directory moves, move the directory; git detects individual file renames automatically.

### Step 5 — Translate configuration

If `.spec-workflow/config.example.toml` exists, translate to `documentation/workflow-config.md`:

```toml
# legacy config.example.toml
[confluence]
space = "TBMLI"
parent_page_id = 6500000000

[jira]
project = "TI"
board = 100
```

becomes:

```markdown
# Workflow Config

confluence_space: TBMLI
confluence_parent_page: 6500000000
jira_project: TI
jira_board: 100
```

If both a legacy `.claude/workflow-config.md` and a `.spec-workflow/config.example.toml` exist, merge: prefer `.claude/` values (more recent format), fill gaps from the TOML.

### Step 6 — Archive history

Legacy approval records, user-templates, and any other history should not be deleted — move them under `documentation/archive/{source-name}/` so they remain in git history and are discoverable if someone needs to trace a decision.

### Step 7 — Update references

Some files may contain hardcoded `.claude/` or `.spec-workflow/` path references in their text (not just their location). After moving files, grep for these paths inside the moved files and update:

```
grep -l '.claude/\|.spec-workflow/' documentation/ --recursive
```

Common cases:
- tasks.md files referencing `.claude/specs/{feature}/` in `_Leverage:` paths
- sprint kickoff docs referencing `.claude/steering/` or `.claude/specs/`
- steering docs referencing `.claude/` paths in examples

Update each to the `documentation/` equivalent. Present diffs for approval before committing.

### Step 8 — Remove empty legacy directories

After everything is moved, the legacy directories should be empty. Remove them:

```
rmdir .spec-workflow/templates .spec-workflow/steering .spec-workflow/specs .spec-workflow  2>/dev/null || true
rmdir .claude/steering .claude/specs .claude/releases .claude/sprints .claude  2>/dev/null || true
```

`rmdir` fails on non-empty dirs — this is intentional, surfacing anything overlooked.

**Do NOT remove** `.claude/` at the user's home directory level — only at repo root.

### Step 9 — Commit

Single commit per migration source:

```
refactor(docs): migrate .spec-workflow/ to documentation/

- steering, specs, archive moved under documentation/
- approvals archived to documentation/archive/approvals/
- config.example.toml translated to documentation/workflow-config.md
- internal path references updated

Legacy .spec-workflow/ directory removed.
```

Use `git mv` in the commit so rename history is preserved. Do not squash file moves into a feat commit — keep the migration reviewable as its own refactor.

### Step 10 — Update downstream systems

Post-migration tasks (not automated by the skill — prompt the user):

- [ ] Update any CI scripts that reference `.claude/` or `.spec-workflow/` paths
- [ ] Update any editor/IDE config that excluded `.claude/` from search
- [ ] Update `.gitignore` if it referenced legacy paths
- [ ] Re-publish affected Confluence pages if URLs have changed
- [ ] Notify team in Slack / standup that spec locations have moved

## Collision handling policy

| Situation | Action |
|-----------|--------|
| Same spec in both legacy and new | Stop, ask user which version to keep |
| Same spec in `.spec-workflow/` and `.claude/` | Prefer `.claude/` (more recent format); archive `.spec-workflow/` version |
| Legacy spec references a JIRA epic that doesn't exist | Keep the spec, flag to user; do not create the epic |
| Legacy spec lacks the `_Skill:` annotations required by current tasks.md | Keep as-is; flag that the spec will need routing annotations before `backlog-manager` can publish it |
| Legacy steering doc conflicts with current one | Present a diff and ask user which to keep per-section |

## Reversibility

Because every move uses `git mv` and is in a single commit, reverting the migration is:

```
git revert {migration-commit-sha}
```

or, if the user wants to undo during the migration itself:

```
git restore --staged --worktree .
```

(before committing)

This is why Step 3 requires a clean tree — so revert is surgical.

## What this migration does NOT do

- Does not change JIRA tickets (those are already in JIRA by key; the spec's new path is updated in ticket descriptions when `backlog-manager` is next invoked)
- Does not change Confluence pages (their URLs are content-based, not path-based)
- Does not re-publish the impl logs
- Does not upgrade legacy specs to add new fields (`_Skill:`, `_Estimate:`) — it preserves content verbatim. If a legacy spec is missing these, `feature-spec-author` in refine mode can add them, but that's a separate action.
- Does not migrate implementation logs that lived in the repo (those should have been JIRA comments from the start; if a legacy `.claude/logs/` directory exists, archive it and flag for manual review)

## After migration

Run the workflow's normal state detection (`references/workflow-state.md` probes). All probes should succeed against the new `documentation/` layout. The orchestrator should report:

> "Steering present, {N} features specced, {M} in backlog, sprint {K} active — ready to continue."

If any probe fails after migration, surface the gap to the user — don't silently re-migrate.
