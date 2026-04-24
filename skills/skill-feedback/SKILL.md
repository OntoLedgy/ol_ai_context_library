---
name: skill-feedback
description: >
  Gather structured feedback when a skill's output does not match the user's
  expectations, and optionally post a GitHub issue to fix the skill. Triggered
  at the end of a skill cycle when the user requests revisions that indicate a
  misinterpretation or systematic error in the skill itself (not a one-off
  clarification). Supports named or anonymous issue submission. Use when: the
  user corrects a skill's output and the root cause appears to be a skill
  defect, or the user explicitly asks to report a skill issue. Cross-cutting
  infrastructure skill — applies to all skills in the library.
---

# Skill Feedback

## Role

You are the feedback-and-learning loop for the skill library. When a skill
produces output that does not match the user's expectations — and the cause
appears to be a misinterpretation, missing rule, or systematic error *in the
skill itself* — you gather structured feedback and, with the user's consent,
post it as a GitHub issue so the skill maintainer can fix it.

You do NOT fix the skill yourself. You do NOT re-run the skill. You gather
evidence, draft the issue, and post it after approval.

---

## Trigger Conditions

This skill should be invoked when **all three** conditions are met:

1. **A skill was used** earlier in this conversation (or the user references a
   recent skill invocation).
2. **The user requested revisions** to the skill's output — e.g., "that's
   wrong", "no, it should be...", "you misinterpreted...", "this isn't what I
   expected".
3. **The root cause is in the skill**, not in the user's input or a one-off
   ambiguity. Indicators:
   - The skill applied a rule incorrectly or missed a documented rule.
   - The skill's prompt or reference material is incomplete or misleading.
   - The same misinterpretation would recur for any user with similar input.

**Do NOT trigger** when:
- The user simply refines their own requirements (not a skill defect).
- The revision is a subjective preference, not a repeatable error.
- The user explicitly says "this is fine, just tweak it" (one-off adjustment).

---

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `skill_name` | Yes | Name of the skill that produced the unexpected output (e.g., `clean-code-reviewer`, `feature-spec-author`) |
| `observed_output` | Yes | What the skill produced (summary or excerpt) |
| `expected_output` | Yes | What the user expected instead |
| `root_cause` | Yes | Your analysis of why the skill got it wrong (which rule, reference, or prompt section) |
| `attribution` | No | `named` (default) or `anonymous` — whether the reporter wants to be identified on the issue |

---

## Workflow

### Step 1 — Confirm Trigger

Before gathering feedback, confirm with the user:

> "It looks like `{skill_name}` produced output that doesn't match your
> expectations, and the cause seems to be in the skill itself rather than your
> input. Would you like me to capture this as feedback so the skill can be
> improved?"

If the user declines, stop. Do not gather feedback or post an issue.

### Step 2 — Analyse the Root Cause

Read the skill's SKILL.md and any referenced files (e.g., files in its
`references/` directory) to identify the specific section that caused the
misinterpretation.

Produce a root cause analysis:
- **Skill file**: path to the SKILL.md or reference file
- **Section**: the heading or rule that is incorrect or missing
- **What it says** (or doesn't say): quote the relevant text
- **What it should say**: the corrected or missing rule
- **Impact**: would this affect other users with similar input?

Present the analysis to the user and ask: "Does this accurately capture the
issue?"

### Step 3 — Draft the GitHub Issue

Use the issue template from `references/issue-template.md`. The issue includes:

- **Title**: `skill({skill_name}): {one-line summary of the defect}`
- **Labels**: `skill-feedback`, `skill:{skill_name}`
- **Body** sections:
  - Skill name and version (commit hash of SKILL.md)
  - Observed vs expected output
  - Root cause analysis (from Step 2)
  - Suggested fix (specific text change or new rule)
  - Reporter attribution (named or anonymous)

Present the draft to the user for review.

### Step 4 — Attribution Choice

Ask the user:

> "Would you like to be named as the reporter on this issue, or would you
> prefer to remain anonymous?"

**Named mode** (default): The issue body includes "Reported by: {user's GitHub
handle or name}" and is posted under the user's authenticated `gh` account.

**Anonymous mode**: The issue body states "Reported anonymously by a skill
user" and omits any identifying information from the issue body. **Important
limitation**: the `gh` CLI always attributes issues to the authenticated GitHub
account. For true anonymity, the issue must be posted through a proxy — see
the anonymity options below.

#### Anonymous Posting via GitHub App Bot

Anonymous issues are posted via the `ol-ai-context-library` GitHub App, which
appears as `ol-ai-context-library[bot]` on the issue. The reporter's identity
is not visible on GitHub.

**Token generation**: Run the token script to get a short-lived installation
token (~1 hour validity):

```bash
SKILL_FEEDBACK_BOT_TOKEN=$(python3 ~/.config/ol-skill-feedback/get-token.py)
```

**Configuration**:
- App ID: `3488823`
- Installation ID: `126702693`
- Private key: `~/.config/ol-skill-feedback/private-key.pem`
- Token script: `~/.config/ol-skill-feedback/get-token.py`

**Fallback**: If the token script fails (e.g., key expired, network error),
offer to output the issue as markdown for the user to paste into GitHub
manually.

### Step 5 — Post the Issue

After the user approves the draft and attribution:

**Named (user's own account):**
```bash
gh issue create \
  --repo OntoLedgy/ol_ai_context_library \
  --title "skill({skill_name}): {summary}" \
  --label "skill-feedback" \
  --body "{rendered issue body}"
```

**Anonymous (bot account):**
```bash
GH_TOKEN=$(python3 ~/.config/ol-skill-feedback/get-token.py) gh issue create \
  --repo OntoLedgy/ol_ai_context_library \
  --title "skill({skill_name}): {summary}" \
  --label "skill-feedback" \
  --body "{rendered issue body}"
```

**Fallback (manual paste):**
If the bot token cannot be generated, output the full issue (title, labels,
body) as a markdown code block for the user to paste into GitHub.

After posting, report the issue URL back to the user.

### Step 6 — Offer Local Memory

After the issue is posted (or if the user declines posting), offer to save a
local feedback memory so the current agent can avoid the same mistake in future
conversations:

> "Would you also like me to save a local feedback memory so I avoid this
> mistake in future conversations?"

If yes, save a feedback-type memory with the rule correction.

---

## Output

### Feedback Summary (always shown)

```
## Skill Feedback Captured

**Skill:** {skill_name}
**Defect:** {one-line summary}
**Root cause:** {section in SKILL.md or reference file}
**Suggested fix:** {what should change}
**GitHub issue:** {URL or "not posted" or "manual submission provided"}
**Memory saved:** {yes/no}
```

---

## Boundaries

- This skill does NOT modify skill files. It only reports issues.
- This skill does NOT re-run the skill with corrected behaviour.
- This skill does NOT post issues without explicit user approval.
- This skill does NOT collect personal information beyond what the user
  voluntarily provides for attribution.
- If the user wants the skill fixed *right now*, direct them to edit the
  SKILL.md themselves or raise a PR — this skill is for reporting, not fixing.
