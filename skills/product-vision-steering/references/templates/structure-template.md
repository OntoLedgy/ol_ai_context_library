# Project Structure

> **How to use this document.** Steering doc — describes WHERE things live and HOW they are named.
> Read by every engineer (human and AI) before placing or naming a new file. If a convention here
> conflicts with an in-repo pattern, the in-repo pattern wins for already-placed code; this document
> wins for new code. Update this doc when the convention changes — don't let drift accumulate.

| | |
|---|---|
| **Project** | [name] |
| **Last reviewed** | [YYYY-MM-DD] |
| **Approved by** | [name(s)] |
| **Confluence page** | [URL, set on first publish] |

## Directory Organisation

```
[Describe the actual directory tree. Annotate purpose per top-level entry. Keep it current — an
out-of-date tree is misleading.]

project-root/
├── src/                    # [Purpose]
├── tests/                  # [Purpose]
├── documentation/          # [Repo-side specs and steering docs]
│   ├── steering/           # product.md, tech.md, structure.md
│   ├── releases/           # Per-release plans
│   └── specs/              # Per-feature specs (requirements/design/tasks)
├── scripts/                # [Build / utility scripts]
└── [other top-level dirs]
```

## Naming Conventions

### Files
| Kind | Convention | Example |
|---|---|---|
| Components / modules | [PascalCase / snake_case / kebab-case] | [example] |
| Services / handlers | [convention] | [example] |
| Utilities / helpers | [convention] | [example] |
| Test files | [convention] | [example] |

### Code Symbols
| Kind | Convention | Example |
|---|---|---|
| Classes / types | [PascalCase / CamelCase] | [example] |
| Functions / methods | [camelCase / snake_case] | [example] |
| Constants | [UPPER_SNAKE_CASE] | [example] |
| Variables | [camelCase / snake_case] | [example] |
| Private / internal | [leading underscore? package-private?] | [example] |

## Test File Placement

[Test placement is a frequent source of inconsistency. Be explicit.]

- **Unit tests**: [colocated next to source / mirrored under `tests/` / etc.]
- **Integration tests**: [location, naming convention]
- **End-to-end tests**: [location, naming convention — note OAS-23 standardised the e2e + thin-slice
  convention; reference its prompt if applicable]
- **Fixtures and test data**: [location]
- **Snapshots / golden files**: [location]

## Import Patterns

### Import Order
1. Standard library / language built-ins
2. Third-party external dependencies
3. Internal project modules (absolute imports)
4. Relative imports within the same module
5. Style / asset imports

### Module / Package Organisation
[Describe the canonical import style for this project — absolute from project root, relative within
a module, namespace packages, etc.]

## Code Structure Patterns

### Module / Class Organisation
```
1. Module docstring (purpose)
2. Imports
3. Constants and configuration
4. Type / interface definitions
5. Main implementation
6. Helper / private functions
7. Exported public API
```

### Function / Method Organisation
```
- Input validation first (fail fast at the boundary)
- Core logic
- Single clear return point where practical
- Errors raised, not silently swallowed
```

### File Organisation Principles
- One primary class / module per file
- Related helpers may co-exist if they only serve the primary
- Public API at the top or bottom — be consistent within the project
- Internal helpers prefixed or marked clearly

## Skill-to-Directory Routing (if applicable)

[When the project is built with OL-SDD engineer skills, declare which skill writes code where. Helps
both sprint-executor's routing and human reviewers' expectations.]

| Skill | Writes to | Notes |
|---|---|---|
| `data-engineer` | [path] | [convention] |
| `ui-engineer` | [path] | [convention] |
| `bie-data-engineer` | [path] | [convention] |
| `agent-engineer` | [path] | [convention] |

## Documentation Surface Map

[Where each kind of documentation lives. Avoids duplication between repo, Confluence, and JIRA.]

| Artifact | Surface | Path / URL pattern |
|---|---|---|
| Steering docs | Repo + Confluence | `documentation/steering/` ↔ Confluence parent page |
| Release plans | Repo + Confluence | `documentation/releases/{release}/` |
| Feature specs | Repo + Confluence | `documentation/specs/{feature}/` |
| Backlog tickets | JIRA | `{PROJECT-KEY}` |
| Implementation logs | JIRA comments | `impl-logged` label on each ticket |
| ADR / decision records | [repo or Confluence] | [path] |
| API reference | [generated / handwritten] | [path or URL] |

## Code Organisation Principles
1. **Single responsibility** — each file has one clear purpose
2. **Modularity** — code is organised into reusable modules
3. **Testability** — structure makes testing straightforward
4. **Consistency** — follow established patterns before introducing new ones

## Module Boundaries
[Define how parts of the project interact and where the firewall lines are.]

- **Public API vs internal**: [what is exposed]
- **Stable vs experimental**: [where experimental code lives]
- **Platform-specific isolation**: [if applicable]
- **Dependency direction**: [which modules may depend on which — call out the forbidden directions]

## Code Size Guidelines

| Limit | Target | Hard ceiling |
|---|---|---|
| File length | [lines] | [lines] |
| Function / method length | [lines] | [lines] |
| Class / module complexity | [metric, e.g. cyclomatic] | [ceiling] |
| Nesting depth | [levels] | [levels] |

Override conditions: [when a function genuinely needs to exceed the ceiling — usually never. Document
the rare exceptions.]

## UI / Frontend Structure (if applicable)
[Delete if not relevant.]

```
src/
└── [ui-or-frontend-dir]/
    ├── components/        # [Atomic / Feature-Sliced / etc.]
    ├── pages-or-routes/   # [Naming convention]
    ├── state/             # [State management modules]
    └── styles/            # [CSS / theme]
```

## Documentation Standards
- All public APIs must have documentation
- Inline comments only where the WHY is non-obvious
- README at each major module boundary
- Follow the language's idiomatic documentation conventions
