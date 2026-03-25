# Skill Architecture: Facet Diagram

A faceted classification of the skill library — each skill is uniquely addressed by a combination of facet values.

---

## Facet Taxonomy

```mermaid
mindmap
  root((SKILL FACETS))
    F1 Mode
      Design
      Implement
      Review
      Refactor
    F2 Role
      Architect
      Engineer
    F3 Scope
      Solution
      Ontology
      Pipeline
      UI
      BIE
    F4 Language
      Agnostic
      Python
      TypeScript/JS
      C-Sharp
      Rust
    F5 Topic · Review and Refactor mode only
      Functions
      Classes
      Naming
      Errors
      Smells
```

**Operation is derived, not a facet**: `Scope + Role` → Operation name.

| Scope | Architect | Engineer |
|---|---|---|
| Solution | Solution Architecture | Solution Implementation |
| Ontology | Ontology Design | Ontology Implementation |
| Pipeline | Pipeline Architecture | Pipeline Implementation |
| UI | UI Design | UI Implementation |
| BIE | BIE Design | BIE Implementation |

---

## Skills Placement Matrix

| Skill | Mode | Role | Scope | Language | → Operation |
|---|---|---|---|---|---|
| `software-architect` | Design | Architect | Solution | Agnostic | Solution Architecture |
| `bie-component-ontologist` | Design | Architect | BIE | Agnostic | BIE Design |
| `bclearer-pipeline-architect` | Design | Architect | Pipeline | Agnostic | Pipeline Architecture |
| `data-engineer` | Implement | Engineer | Solution | Agnostic | Solution Implementation |
| `python-data-engineer` | Implement | Engineer | Solution | Python | Solution Implementation |
| `javascript-data-engineer` | Implement | Engineer | Solution | TypeScript | Solution Implementation |
| `csharp-data-engineer` | Implement | Engineer | Solution | C# | Solution Implementation |
| `rust-data-engineer` | Implement | Engineer | Solution | Rust | Solution Implementation |
| `bie-data-engineer` | Implement | Engineer | BIE | Python | BIE Implementation |
| `bclearer-pipeline-engineer` | Implement | Engineer | Pipeline | Python | Pipeline Implementation |
| `clean-code-reviewer` | Review | Engineer | Solution | Multi | _(cross-cutting)_ |
| `clean-code-refactor` | Refactor | Engineer | Solution | Multi | _(cross-cutting)_ |

> `clean-code-reviewer` and `clean-code-refactor` are cross-cutting — they apply across all scopes. Assigned to Solution scope as the broadest default.

---

## Clean Coding Topics: Sub-Facet of Review / Refactor

Clean coding topics are a conditional facet — they only apply when **Mode = Review or Refactor**. They define *what* is being examined or fixed. In Implement mode, all topics apply holistically; in Review/Refactor they can be targeted.

### Topic Taxonomy

```mermaid
mindmap
  root((Topic))
    Functions
      Size under 20 lines
      Single responsibility
      0-3 arguments
      No flag arguments
      No side effects
      Consistent abstraction level
    Classes
      Single responsibility
      High cohesion
      Low coupling
      Size under 200 lines
      Dependency on abstractions
    Naming
      Reveals intent
      Noun for types · verb for methods
      No abbreviations
      No encoding
      Searchable
    Errors
      Exceptions not codes
      No null returns
      No null parameters
      Context in messages
    Smells
      No duplication
      No dead code
      No magic numbers
      No feature envy
      No large class
      No long parameter list
```

### Topic Priority Order (for full review)

When no topic is specified (`full` mode), apply in this order to minimise rework:

```
Functions → Classes → Naming → Errors → Smells
    ↑            ↑        ↑        ↑        ↑
  structure   structure  labels  safety  cleanup
  (rename     (split     (after  (after  (last —
  after)      after      rename) struct) depends
              rename)             fixed)  on all)
```

### Topics Are Cross-Cutting Across All Scopes

Topics apply to **any** engineer skill operating in Review or Refactor mode, regardless of scope:

```
                   TOPIC
                   ─────────────────────────────────────────────────
                   Functions  Classes  Naming  Errors  Smells
SCOPE              ─────────────────────────────────────────────────
Solution           ✓          ✓        ✓       ✓       ✓
BIE                ✓          ✓        ✓       ✓       ✓
Pipeline           ✓          ✓        ✓       ✓       ✓
Ontology           ✓          ✓        ✓       ✓       ✓
UI                 ✓          ✓        ✓       ✓       ✓
─────────────────────────────────────────────────────────────────────
```

The `clean-code-reviewer` and `clean-code-refactor` skills are the dedicated, composable implementations. Embedded review modes within architect/engineer skills are implicitly full-topic reviews scoped to their domain.

### Extended Canonical Address (with Topic)

When targeting a specific topic, the address extends to `[Role]:[Mode]:[Scope]:[Language]:[Topic]`:

| Canonical Address | Meaning |
|---|---|
| `engineer:review:solution:python:full` | clean-code-reviewer, all topics, Python |
| `engineer:review:solution:python:naming` | clean-code-reviewer, naming only |
| `engineer:review:solution:python:functions` | clean-code-reviewer, functions only |
| `engineer:refactor:solution:python:naming` | clean-code-refactor, fix naming |
| `engineer:refactor:solution:python:smells` | clean-code-refactor, fix smells |
| `engineer:review:pipeline:python:errors` | pipeline engineer reviewing error handling |

Topic defaults to `full` when omitted.

---

## Mode × Role: The Two-Axis Model

```
             ROLE
             ─────────────────────────────────────────
             Architect             Engineer
MODE ────────────────────────────────────────────────────
Design   │   PRIMARY               (upstream input)
         │   s-arch, bie-ont,
         │   bcl-arch
─────────────────────────────────────────────────────────
Implement│   (driven by design)    PRIMARY
         │                         d-eng, py-eng,
         │                         js/cs/rs-eng,
         │                         bie-eng, bcl-eng
─────────────────────────────────────────────────────────
Review   │   embedded in each      cc-reviewer
         │   Architect skill       + embedded in each
         │   (gap analysis)        Engineer skill
─────────────────────────────────────────────────────────
Refactor │   structural changes    cc-refactor
         │   (via new design)      (code-level only)
```

---

## Skills Space: Scope × Language Grid

```
              LANGUAGE AXIS
              ──────────────────────────────────────────────────────────
              Agnostic   Python   TypeScript   C#     Rust    Multi
              ──────────────────────────────────────────────────────────
S  Solution   data-eng   py-eng   js-eng       cs-eng rs-eng  cc-rev
C                                                              cc-ref
O  Ontology   ·          ·        ·            ·      ·       ·
P  Pipeline   bcl-arch†  bcl-eng  ·            ·      ·       ·
E  UI         ·          ·        ·            ·      ·       ·
   BIE        bie-ont†   bie-eng  ·            ·      ·       ·
──────────────────────────────────────────────────────────────────────
  † = Architect role (Design mode)
  · = gap (no skill exists for this combination)
```

---

## Inheritance Hierarchy

```mermaid
flowchart TD
    subgraph Architect["Role: Architect"]
        SA[software-architect\nSolution]
        BCO[bie-component-ontologist\nBIE]
        BCL_A[bclearer-pipeline-architect\nPipeline]
        SA -->|"extends"| BCL_A
    end

    subgraph Engineer["Role: Engineer"]
        DE[data-engineer\nSolution · Agnostic]
        PY[python-data-engineer\nSolution · Python]
        JS[javascript-data-engineer\nSolution · TypeScript]
        CS[csharp-data-engineer\nSolution · C#]
        RS[rust-data-engineer\nSolution · Rust]
        BIE_E[bie-data-engineer\nBIE · Python]
        BCL_E[bclearer-pipeline-engineer\nPipeline · Python]

        DE -->|"extends"| PY
        DE -->|"extends"| JS
        DE -->|"extends"| CS
        DE -->|"extends"| RS
        DE -->|"extends"| BIE_E
        PY -->|"extends"| BCL_E
    end

    subgraph Quality["Review + Refactor modes · cross-cutting"]
        CCR[clean-code-reviewer]
        CCRF[clean-code-refactor]
        CCR -->|"output feeds"| CCRF
    end

    SA -->|"design feeds"| DE
    BCL_A -->|"design feeds"| BCL_E
    BCO -->|"design feeds"| BIE_E
```

---

## Mode × Scope Lanes

```
MODE:      Design ───────────────► Implement ──────────► Review/Refactor

           ┌──────────────────┐    ┌───────────────┐    ╔══════════════╗
Solution   │ software-        │───►│ data-engineer │───►║ clean-code-  ║
           │ architect        │    │ (+ language   │    ║ reviewer     ║
           └──────────────────┘    │  variants)    │    ║ clean-code-  ║
                                   └───────────────┘    ║ refactor     ║
           ┌──────────────────┐    ┌───────────────┐    ╚══════════════╝
Ontology   │ ·                │    │ ·             │   ← scope exists,
           └──────────────────┘    └───────────────┘     skills pending

           ┌──────────────────┐    ┌───────────────┐
BIE        │ bie-component-   │───►│ bie-data-     │─────────↑
           │ ontologist       │    │ engineer      │   applies to
           └──────────────────┘    └───────────────┘   all scopes
           ┌──────────────────┐    ┌───────────────┐
Pipeline   │ bclearer-        │───►│ bclearer-     │
           │ pipeline-arch    │    │ pipeline-eng  │
           └──────────────────┘    └───────────────┘
           ┌──────────────────┐    ┌───────────────┐
UI         │ ·                │    │ ·             │   ← scope exists,
           └──────────────────┘    └───────────────┘     skills pending
```

---

## Structural Observations

### 1. Operation is Fully Derived
Removing Operation as a facet is correct — `Scope + Role` composes it unambiguously. No information is lost; the operation name is readable from any skill's facet address.

### 2. Scope Clarifies What Domain Conflated
The old "Domain" value "bclearer Pipeline" conflated scope (Pipeline) with platform (bclearer). The new model separates these: scope is Pipeline, platform specificity is captured in the skill name and references. This makes the grid extensible to other pipeline platforms.

### 3. UI Scope Is Present but Unpopulated
The UI scope is named in the taxonomy but has no skills yet. This makes the gap explicit and shows where the library needs to grow.

### 4. Identified Gaps

| Gap | Facet Coords | Implication |
|---|---|---|
| BIE × non-Python | Implement / Engineer / BIE / TypeScript, C#, Rust | BIE impl locked to Python |
| Pipeline × non-Python | Implement / Engineer / Pipeline / TypeScript, C#, Rust | Pipeline impl locked to Python |
| Ontology × all languages | * / * / Ontology / * | Ontology scope has no skills yet |
| UI × all | * / * / UI / * | No UI skills exist |
| Architect:Refactor | Refactor / Architect / * | No structural refactoring skill |
| Architect:Review (standalone) | Review / Architect / * | Architecture review is embedded, not composable |

---

## Canonical Skill Address

Format: `[Role]:[Mode]:[Scope]:[Language]`

| Canonical Address | Skill |
|---|---|
| `architect:design:solution:*` | software-architect |
| `architect:design:bie:*` | bie-component-ontologist |
| `architect:design:pipeline:*` | bclearer-pipeline-architect |
| `engineer:implement:solution:*` | data-engineer |
| `engineer:implement:solution:python` | python-data-engineer |
| `engineer:implement:solution:typescript` | javascript-data-engineer |
| `engineer:implement:solution:csharp` | csharp-data-engineer |
| `engineer:implement:solution:rust` | rust-data-engineer |
| `engineer:implement:bie:python` | bie-data-engineer |
| `engineer:implement:pipeline:python` | bclearer-pipeline-engineer |
| `engineer:review:solution:multi` | clean-code-reviewer |
| `engineer:refactor:solution:multi` | clean-code-refactor |
