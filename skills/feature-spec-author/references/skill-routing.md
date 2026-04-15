# Skill Routing Table

When writing a task in `tasks.md`, annotate it with the engineer skill that should implement it using `_Skill: {skill-name}_`. This same label drives JIRA routing (Phase 2) and sprint-executor delegation (Phase 4).

## Routing guide

| Task Type | Skill | Examples |
|-----------|-------|----------|
| Python data/business logic | `python-data-engineer` | API endpoints, services, parsers |
| Python + BORO/OL conventions | `ob-engineer` | BORO-style modules, interop services |
| SQLAlchemy model + Alembic migration | `python-data-engineer` | Schema changes |
| FastAPI endpoint / router | `python-data-engineer` | REST API |
| Pydantic schema | `python-data-engineer` | Request/response models |
| bclearer pipeline stage | `bclearer-pipeline-engineer` | Stage runners, orchestration |
| BIE domain object, enum, identity | `bie-data-engineer` | BIE components |
| Agent (tool, orchestration, skill) | `agent-engineer` | ol_ai_services agents |
| React / TypeScript UI component | `ui-engineer` | Pages, components, hooks |
| Raw TS/JS (non-UI) | `javascript-data-engineer` | Node utilities, API clients |
| C# library / service | `csharp-data-engineer` | .NET code |
| Rust library / CLI / engine | `rust-data-engineer` | Performance-critical code |
| Clean code review only | `clean-code-reviewer` | Quality check before merge |
| Code smells / function size / naming | `clean-code-refactor` | Refactor-only tasks |
| Test-only task | `clean-code-tests` | Test coverage additions |
| Architecture-only change | `software-architect` (refactor) | Structural redesign with no new features |
| Ontology modelling | `ob-ontologist` / `bie-component-ontologist` | Domain analysis, BORO classification |
| Commit-only task | `clean-code-commit` | Validating commit messages |

## Rules

1. **One skill per task.** If a task needs two skills, split it.
2. **Prefer the most specific skill.** `ob-engineer` over `python-data-engineer` when BORO conventions apply.
3. **Language always matches.** Don't route Python code to `ui-engineer`.
4. **UI tasks default to `ui-engineer`** (extends `javascript-data-engineer`) unless framework-agnostic.
5. **Unknown routing?** Default to the generic `data-engineer` and flag for review.

## JIRA label convention

The `_Skill: python-data-engineer_` annotation becomes JIRA label `skill:python-data-engineer` on the ticket, so engineers and automation can filter.

## Related

- `skills/SKILL-ARCHITECTURE.md` for the full skill taxonomy (role × mode × scope × language).
