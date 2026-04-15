---
name: product-vision-steering
description: >
  Produce and maintain the three steering documents that provide persistent project
  context: product.md (vision, users, objectives), tech.md (stack, patterns, tooling),
  and structure.md (directory layout, naming conventions). Use when: setting up a new
  project from scratch, onboarding an existing codebase into the ol-sdd-workflow,
  refreshing steering docs when the project's direction or stack changes, or when a
  feature spec author needs upstream context that is missing. Produces filled-in
  templates committed to documentation/steering/ and published to Confluence. Phase 0 of
  the ol-sdd-workflow orchestrator.
---

# Product Vision & Steering

## Role

You produce the three steering documents that every downstream spec, backlog item, and implementation relies on for context. These are the project's long-lived "constitution" — they change rarely and intentionally.

You are invoked by the `ol-sdd-workflow` orchestrator at Phase 0, or directly by the user when steering needs to be set up or refreshed.

## Deliverables

| File | Template | Purpose |
|------|----------|---------|
| `documentation/steering/product.md` | `prompts/coding/templates/product-template.md` | Product vision: purpose, users, key features, objectives, metrics, principles |
| `documentation/steering/tech.md` | `prompts/coding/templates/tech-template.md` | Technology stack: languages, frameworks, libraries, tooling, deployment |
| `documentation/steering/structure.md` | `prompts/coding/templates/structure-template.md` | Project structure: directory organisation, naming conventions, module boundaries |

Each file is also published as a Confluence page under the project's parent page.

## Workflow

### Step 1 — Detect Existing State

Check for:
- `documentation/steering/` directory and each of the three files
- If any exist, read them and treat them as the baseline to refine (not replace)
- Identify codebase type from manifest files: `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `Pipfile`, etc.

### Step 2 — Analyse the Project

Scan the codebase for:
- Primary language(s) and version
- Frameworks and major dependencies
- Directory structure and apparent architectural style
- Naming conventions (snake_case vs PascalCase vs camelCase)
- Testing framework and layout
- CI/CD configuration

Do not fabricate details you can't verify — flag unknowns for the user.

### Step 3 — Gather Product Context

Ask the user (skip questions you can answer from an existing README or docs):
- What problem does this product solve?
- Who are the primary users / consumers?
- What are the top 3–5 features that deliver value?
- What are the business or project objectives?
- What does success look like in 6 months? (metrics, milestones)
- Any known principles, constraints, or non-negotiables?

### Step 4 — Fill the Three Templates

Populate each template. Keep it concrete and specific to this project — no boilerplate filler.

For `tech.md`, draw from `software-architect/references/technology-stack.md` if the project is on the bclearer/OL stack. Otherwise document the actual stack.

For `structure.md`, document what is there now (not an aspirational rewrite). If the structure has known problems, note them in a dedicated section but don't change it.

### Step 5 — Present for Approval

Present all three filled documents to the user. Ask for approval per document — it's acceptable to approve them together, but give the user the chance to refine each.

### Step 6 — Commit and Publish

On approval:
1. Write the three files to `documentation/steering/`
2. Publish each as a Confluence page under the project's parent page (use Atlassian MCP tools; ask for space key and parent page ID if not configured)
3. Update `documentation/workflow-config.md` with confluence/jira config if provided
4. Return to the caller (orchestrator or user) with links to committed files and Confluence pages

---

## When to Refresh Steering

Steering docs should be stable. Refresh when:
- The product pivots (new users, new primary problem)
- The tech stack changes materially (new primary language, new framework)
- The project structure is deliberately reorganised
- Onboarding a new team member reveals that current steering is misleading

Minor drift (a new library added, a refactor) does not warrant a steering refresh — handle it in feature specs.

## What This Skill Does NOT Do

- Does not design features (that's `feature-spec-author`)
- Does not make architecture decisions at feature-level (that's `software-architect`)
- Does not produce ontology models (that's `ontologist` / `ob-ontologist`)
- Does not define a phased development roadmap — that belongs in the project's Confluence landing page or as a follow-up to steering

## References

- `prompts/coding/templates/product-template.md` — product vision template
- `prompts/coding/templates/tech-template.md` — technology stack template
- `prompts/coding/templates/structure-template.md` — project structure template
- `skills/software-architect/references/technology-stack.md` — bclearer/OL platform libraries reference
- `skills/software-architect/references/confluence-pages.md` — Confluence page conventions
