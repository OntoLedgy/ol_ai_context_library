# BORO Clean Coding Skills — Plan

## Context

BORO has a mature, internally documented clean coding approach used on bCLEARer projects. This is captured in the `BORO Coding` section of the SDS Confluence space. The goal is to build two specialised skills that embed these BORO-specific coding conventions:

- **`boro-software-architect`** — extends the existing `software-architect` skill with BORO coding conventions applied at the architectural design level (module naming, orchestration patterns, interface contracts, configuration layers)
- **`boro-software-engineer`** — extends the existing `python-data-engineer` skill with BORO Quick Style Guide as the implementation standard

These skills do NOT replace the existing skills. They sit above them in the inheritance hierarchy as BORO-flavoured specialisations.

**Sources (Confluence pages):**
- `6495863472` — BORO Clean Coding Quick Style Guide ← primary source
- `6495863609` — Clean Coding - Meaningful Names
- `6495863620` — Clean Coding - Readable Code Layout
- `6495862997` — bEng Coding - Discussions - Best Practices
- `6495863571` — bEng Coding Standards - Referencing Code

---

## Part 1: BORO Coding Principles

All principles extracted from the Confluence pages, organised by category.

### 1.1 Naming Conventions

| Rule | BORO Standard | Example |
|------|--------------|---------|
| Class names | CamelCase, **plural** | `class MyObjectTypes:` |
| Class file names | snake_case | `my_object_types.py` |
| Constant names | CAPITAL_CASE with underscores | `IDS_COLUMN_NAME = 'boro_ids'` |
| All other names | snake_case | `get_my_function_result()` |
| Function names | **"action" names** — verbs | `get_something()`, `export_data()` |
| File names | **"actor" names** aligned with public function | `data_exporter.py` → `export_data()` |
| Boolean functions | `is_` or `has_` prefix | `is_snapshot_valid()` |
| Private methods | **double underscore prefix** `__` | `def __process_line():` |
| String delimiter | **single quotes only** | `'example string'` |
| Forbidden names | No: `process`, `handle`, `data`, `item`, `tmp`, `res`, unclear abbreviations | |
| Forbidden single letters | Except `self`, `cls`, `__` | |
| File rename rule | If public function renamed → file **must** be renamed | |

**Deeper naming principles (from Meaningful Names page):**

- Use intention-revealing names — precision over brevity
- Avoid disinformation — don't imply wrong meaning
- Make meaningful distinctions — adjacent things must be distinguishable
- Use pronounceable, searchable names
- Avoid encodings (except interface/implementation distinction)
- Class names = nouns or noun phrases; avoid Manager, Processor, Data, Info
- Method names = verbs or verb phrases; accessors use `get_`/`set_`/`is_`
- No mental mapping, no slang, no culture-specific terms
- One word per concept — consistency across sibling methods and classes
- Prefer solution domain names (CS terminology) over problem domain names
- Use context to disambiguate without being gratuitously redundant

### 1.2 Code Layout

| Rule | BORO Standard |
|------|--------------|
| Line length | **20 chars** (BORO standard; PEP8 says 79 — BORO overrides this) |
| Between instructions | One empty line |
| After colon `:` (function/loop) | Do NOT leave next line empty |
| Variable assignments | Always in new line after backslash `\` |
| Function arguments | Each argument on its own line; no spaces around `=` in calls |
| Parameter name + value | On the same line (no break after `=`) |
| Type annotations | **Always specify** parameter types |
| Named parameters | **Always specify** argument name at call site; use `*` to enforce |
| Return type | **Always specified**, on new line before colon; `-> None` if nothing returned |
| For loops | `in` block goes on a new line |
| Class member sequence | constants → static attrs → object attrs → inner classes → getters/setters → methods |
| Indentation | 4 spaces; no TABs |
| Related attributes | No empty line between them; empty line between all other members |
| Paragraphs | Blocks of related statements separated by empty lines |

### 1.3 Function Design

| Rule | BORO Standard |
|------|--------------|
| Return | Only one item |
| Responsibility | One thing only — separation of concerns |
| Decomposition | Break into sub-functions as much as possible |
| Too many arguments | Create a class to pass them |
| Flag arguments | Forbidden |
| Private functions | Called only by the main function in the file; never externally |
| Exposing behaviour | If external code needs it → expose as a public method |

### 1.4 File / Module Structure

| Rule | BORO Standard |
|------|--------------|
| Per-file rule | One **public** (entry point) function + its private subfunctions |
| Exception | Facade/suite files may have multiple related public functions |
| Orchestrator pattern | When managing a sequence of processes → use `orchestrate_*()` function |
| Orchestrator file name | `[name]_orchestrator.py` |
| Orchestrator function name | `orchestrate_[name]()` |
| Nesting | Orchestrators can be nested |

### 1.5 Class Design

| Rule | BORO Standard |
|------|--------------|
| Instance methods | Use `self` |
| No `self`/`cls` usage | Declare as `@staticmethod` |
| Class-level methods | Use `@classmethod` (e.g., `bie_identity_type(cls)`) |

### 1.6 Constants and Strings

| Rule | BORO Standard |
|------|--------------|
| Hardcoded strings | **Never** — define as constants or enums |
| Constants location | Separate file(s) |
| Enums | Separate class |
| File/folder paths | Use `os.path.join()` and `os.sep`; use `Path()` constructor |

### 1.7 Error Handling

| Rule | BORO Standard |
|------|--------------|
| Catch specificity | **Only specific exceptions** — never bare `except:` or `except Exception:` |
| Traceback preservation | Use bare `raise` inside `except` |
| Unimplemented | `raise NotImplementedError` is allowed |

### 1.8 Library Usage

| Rule | BORO Standard |
|------|--------------|
| File/folder operations | Use `nf_common` `Files` and `Folders` classes |
| General functions | **Check `nf_common` first** before writing new ones |
| Import style | **Explicit only**: `from file import class/method/constant` |
| Wildcard imports | Forbidden: `from x import *` |
| Folder imports | Forbidden: `import folder_a.folder_b` |

### 1.9 Comments

| Rule | BORO Standard |
|------|--------------|
| General comments | Clean code must not need comments |
| Code self-documentation | Code should be clear and self-explanatory |
| Allowed comments | Development purposes only: `# TODO`, notes |

### 1.10 Loop Design

| Rule | BORO Standard |
|------|--------------|
| Loop body > 1 statement | Extract all loop content into a private function |
| Nested loops | Must NOT be visible — group into private functions |
| `for` loop `in` clause | Goes on a new line |

### 1.11 Best Practices

| Principle | Rule |
|-----------|------|
| YAGNI | Don't write code you don't need yet |
| DRY — Rule of Three | Third time you write the same code → extract to a helper |
| Fail Fast | Validate input; fail on invalid state as early as possible |
| API Design | Simple things should be simple; complex things should be possible |

---

## Part 2: Architectural Translation

BORO coding principles, when lifted to the architectural level, produce the following patterns. These are not documented on the Confluence site — they are derived from the coding conventions.

### 2.1 Actor-Action Module Architecture
**Source**: File naming convention (actor files + action functions); file rename rule

Every architectural component is named as an **actor** — what it IS (noun). Its primary public interface expresses its **action** — what it DOES (verb). Renaming the action renames the actor.

**Architectural implications:**
- No "utility" modules — every module is a purposeful actor
- Each component has one public API entry point by default
- Module identity is tied to its function; if its purpose changes, it must be redesigned
- Component naming: `[domain_noun]_[role].py` with `do_action()` as the public function

### 2.2 Orchestration as First-Class Architectural Concern
**Source**: Orchestrator pattern; nested orchestrators

Multi-step processes are managed by explicitly named orchestrators. Orchestrators compose other orchestrators, creating a visible pipeline hierarchy.

**Architectural implications:**
- Architecture must designate orchestration layers explicitly
- Clear separation between orchestration logic (what runs next) and execution logic (what is done)
- Orchestrators are visible in architecture diagrams — not implicit `main()` functions
- Orchestrator hierarchy maps directly to the solution's processing stages
- Canonical naming: `orchestrate_[stage_name]()` in `[stage_name]_orchestrator.py`

### 2.3 Constant/Enum Configuration Layer
**Source**: No hardcoded strings; constants in separate files; enums in separate classes

All domain vocabulary — type names, column names, status values, configuration keys — is separated from processing logic in a dedicated constants/enums layer.

**Architectural implications:**
- A constants/configuration layer is mandatory in every solution architecture
- Domain vocabulary is a first-class architectural concern
- Enums create self-documenting, type-safe APIs across component boundaries
- Changing domain vocabulary only touches the constants layer

### 2.4 Explicit Contract Architecture
**Source**: Mandatory type annotations; mandatory named parameters; return type declarations

All component interfaces are fully specified with types. Named parameters enforce clarity at call sites. No implicit duck-typing contracts across module boundaries.

**Architectural implications:**
- All public APIs carry full type contracts (parameters and return types)
- Component integration is verifiable without runtime testing
- `*` parameter enforces named-only calling at architectural boundaries
- API design: simple calls for common cases; all complex cases still possible

### 2.5 Fail-Fast Boundary Design
**Source**: Fail Fast principle; specific exception handling

Validation occurs at ingress points. Specific exception types are used at each layer. No silent failures.

**Architectural implications:**
- Validation is architecturally located at system boundaries (ingress adapters, entry points)
- Error propagation paths are designed, not ad hoc
- Exception types are domain-specific; each layer defines its own exception vocabulary
- Architecture designates which components are validation gates

### 2.6 Library-First Platform Design
**Source**: Check `nf_common` first; DRY rule

Every solution is designed against an inventory of available platform libraries. Custom code is only written when no platform function exists.

**Architectural implications:**
- Platform library inventory is an input to solution design, not an afterthought
- Architecture explicitly maps which platform library provides each cross-cutting function
- Custom components only appear when platform coverage is absent
- Platform dependencies are explicit in architecture documents

### 2.7 Minimal Surface Area
**Source**: YAGNI; one-public-function-per-file; no speculative abstractions

Architectural scope is strictly bounded by current requirements. Each component exposes the minimum interface needed.

**Architectural implications:**
- No speculative architectural components for hypothetical future requirements
- Feature scope is negotiated before design begins
- Component interfaces are minimal by default — extended only when proven necessary
- Over-engineering is an architectural defect, not a virtue

### 2.8 Decomposition Hierarchy
**Source**: Function decomposition into sub-functions; private functions hidden behind public interface

Architectural components have internal hierarchies. The public interface hides implementation complexity.

**Architectural implications:**
- Architecture is described at multiple levels: L1 orchestrators → L2 workers → L3 helpers
- Each level has its own actor-action naming
- Internal complexity is an implementation detail; only public interfaces appear in diagrams
- Nested orchestrators represent the decomposition hierarchy visually

---

## Part 3: Engineer Skills Translation

BORO coding principles, applied at the implementation level, define the `boro-software-engineer` standard.

### 3.1 BORO vs. `python-data-engineer` — Key Differences

| Dimension | `python-data-engineer` | BORO overrides / adds |
|-----------|----------------------|----------------------|
| Line length | PEP8 79 chars | **20 chars** |
| File structure | One responsibility per file | **One public function per file** |
| Private methods | `_single_underscore` | **`__double_underscore`** |
| Named parameters | Best practice | **Mandatory** — use `*` to enforce |
| Type annotations | Encouraged | **Mandatory** — all params + return types |
| Strings | No hardcoding | **Mandatory enum/constant pattern** |
| Import style | Clean imports | **Explicit only** — no folder imports, no `*` |
| Library reuse | General DRY | **Check `nf_common` first** |
| File naming | Descriptive | **Actor names** aligned with public function |
| Orchestration | General pattern | **`orchestrate_*()` in `*_orchestrator.py`** |
| Exception handling | Use exceptions | **Specific exceptions only** |
| Comments | Minimal | **None** — code must be self-documenting |

### 3.2 BORO Engineer Implementation Checklist

**Naming**
- [ ] Classes: CamelCase, plural
- [ ] Files: snake_case, actor name matching public function
- [ ] Functions: action verbs (`get_`, `export_`, `import_`, `orchestrate_`)
- [ ] Private functions: `__double_underscore`
- [ ] Constants: `CAPITAL_CASE`
- [ ] Booleans: `is_` or `has_` prefix
- [ ] No vague names: no `data`, `tmp`, `process`, `handle`, `res`

**Layout**
- [ ] Lines: ≤ 20 characters
- [ ] Function args: each on its own line
- [ ] Type annotations: all parameters declared
- [ ] Named parameters: enforced with `*`
- [ ] Return type: declared on new line before `:`
- [ ] Variable assignments: new line after `\`
- [ ] For loops: `in` block on new line
- [ ] One empty line between instructions

**Structure**
- [ ] One public function per file
- [ ] Orchestrators in `*_orchestrator.py` files
- [ ] Private functions: only called by the file's public function
- [ ] `@staticmethod` where no `self`/`cls` needed
- [ ] `@classmethod` for class-level identity methods

**Strings and constants**
- [ ] No hardcoded strings — all in constants/enums
- [ ] Paths use `os.path.join()` + `os.sep` or `Path()`
- [ ] String delimiter: single quotes

**Error handling**
- [ ] Specific exceptions only — named exception types
- [ ] Bare `raise` to preserve traceback
- [ ] No `except:` or `except Exception:`

**Libraries**
- [ ] `nf_common` checked before writing general functions
- [ ] Imports: `from file import name` only
- [ ] No `from x import *`
- [ ] No folder-level imports

**Comments**
- [ ] No comments unless `# TODO` / development note

---

## Part 4: Skill Architecture Placement

### New Skills in the Taxonomy

| Skill | Mode | Role | Scope | Language | Inherits From |
|-------|------|------|-------|----------|---------------|
| `boro-software-architect` | Design | Architect | Solution | Agnostic | `software-architect` |
| `boro-software-engineer` | Implement | Engineer | Solution | Python | `python-data-engineer` |

### Inheritance Position

```
software-architect
    └── boro-software-architect      ← adds BORO coding conventions to design output

data-engineer
    └── python-data-engineer
            └── boro-software-engineer   ← adds BORO Quick Style Guide as coding standard
```

### Canonical Facet Addresses

| Skill | Address |
|-------|---------|
| `boro-software-architect` | `architect:design:solution:agnostic:boro` |
| `boro-software-engineer` | `engineer:implement:solution:python:boro` |

---

## Part 5: Conflicts and Overlaps

### Conflicts with Existing Standards

| Dimension | Existing Standard | BORO Standard | Resolution |
|-----------|------------------|---------------|------------|
| Line length | PEP8 79 chars | **20 chars** | BORO wins — intentional and documented |
| Private methods | `_single_underscore` | `__double_underscore` | BORO wins — note: `__` triggers Python name mangling in classes |
| File structure | One responsibility per file | **One public function per file** | BORO is stricter — new skill enforces the BORO rule |
| Comments | Minimal | **None** (code self-documents) | Compatible — BORO is more absolute |
| Named params | Best practice | **Mandatory + `*` enforcement** | BORO is stricter |
| Type annotations | Encouraged | **Mandatory** | BORO is stricter |

### Compatible / Overlapping Rules

| Dimension | Status |
|-----------|--------|
| Functions do one thing | Compatible — BORO aligns with clean code |
| No flag arguments | Compatible — same rule |
| Single responsibility | Compatible — BORO is more granular (file-level) |
| Meaningful names | Compatible — BORO adds actor/action specifics |
| Use exceptions | Compatible — BORO adds the "specific only" constraint |
| YAGNI | Compatible — identical principle |
| DRY | Compatible — BORO uses "Rule of Three" as the trigger |

---

## Part 6: Files to Create

### `boro-software-architect`

```
skills/boro-software-architect/
├── SKILL.md
└── references/
    └── boro-coding-principles.md    ← architectural translations of BORO principles
```

**`SKILL.md` adds to `software-architect`:**
- Actor-action module naming in all component designs
- Explicit orchestration layer in every multi-step solution
- Mandatory constants/enum layer in architecture output
- Explicit type contracts on all component interfaces
- Fail-fast validation gates at system boundaries
- Platform library inventory check before designing custom components
- BORO naming conventions applied to architecture diagrams and specs

### `boro-software-engineer`

```
skills/boro-software-engineer/
├── SKILL.md
└── references/
    └── boro-quick-style-guide.md    ← BORO Quick Style Guide as actionable reference
```

**`SKILL.md` adds to `python-data-engineer`:**
- BORO Quick Style Guide as the coding standard (overrides PEP8 where they conflict)
- All rules in Section 3.2 checklist enforced in Implement and Review modes
- Conflict table (Section 5) included so the engineer knows which standard wins

---

## Part 7: Verification

After skills are created:
1. Read both `SKILL.md` files — confirm they are self-contained and actionable
2. Confirm inheritance is explicit (each skill names what it extends)
3. Confirm `references/` files contain all source principles
4. Update `SKILL-ARCHITECTURE.md` Skills Placement Matrix to add both new skills
5. Confirm conflicts with existing standards are documented within each skill (no silent overrides)
