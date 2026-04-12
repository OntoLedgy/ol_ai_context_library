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
      Analysis
      Review
      Refactor
    F2 Role
      Architect
      Engineer
      Ontologist
    F3 Scope
      Solution
      Ontology
      Pipeline
      Agent
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
    F6 Standard · Review and Refactor mode only
      general
      ob
```

**Operation is derived, not a facet**: `Scope + Role` → Operation name.

| Scope | Architect | Engineer | Ontologist |
|---|---|---|---|
| Solution | Solution Architecture | Solution Implementation | Solution Ontology |
| Ontology | Ontology Design | Ontology Implementation | Ontology Analysis (OB) |
| Pipeline | Pipeline Architecture | Pipeline Implementation | — |
| Agent | Agent Architecture | Agent Implementation | — |
| UI | UI Design | UI Implementation | — |
| BIE | BIE Design | BIE Implementation | BIE Component Ontology |

---

## Skills Placement Matrix

| Skill | Mode | Role | Scope | Language | → Operation |
|---|---|---|---|---|---|
| `software-architect` | Design | Architect | Solution | Agnostic | Solution Architecture |
| `bclearer-pipeline-architect` | Design | Architect | Pipeline | Agnostic | Pipeline Architecture |
| `ob-architect` | Design | Architect | Ontology | Agnostic | Ontology Architecture |
| `ontologist` | Analysis | Ontologist | Solution | Agnostic | Ontological Analysis |
| `ob-ontologist` | Analysis | Ontologist | Ontology | Agnostic | BORO Ontological Analysis |
| `bie-component-ontologist` | Analysis | Ontologist | BIE | Agnostic | BIE Component Ontology |
| `data-engineer` | Implement | Engineer | Solution | Agnostic | Solution Implementation |
| `python-data-engineer` | Implement | Engineer | Solution | Python | Solution Implementation |
| `javascript-data-engineer` | Implement | Engineer | Solution | TypeScript | Solution Implementation |
| `csharp-data-engineer` | Implement | Engineer | Solution | C# | Solution Implementation |
| `rust-data-engineer` | Implement | Engineer | Solution | Rust | Solution Implementation |
| `bie-data-engineer` | Implement | Engineer | BIE | Python | BIE Implementation |
| `ob-engineer` | Implement | Engineer | Ontology | Python | Ontology Implementation |
| `bclearer-pipeline-engineer` | Implement | Engineer | Pipeline | Python | Pipeline Implementation |
| `agent-architect` | Design | Architect | Agent | Agnostic | Agent Architecture |
| `agent-engineer` | Implement | Engineer | Agent | Python | Agent Implementation |
| `ui-architect` | Design | Architect | UI | Agnostic | UI Design |
| `ui-engineer` | Implement | Engineer | UI | TypeScript | UI Implementation |
| `clean-code-reviewer` | Review | Engineer | Solution | Multi | _(cross-cutting)_ |
| `clean-code-refactor` | Refactor | Engineer | Solution | Multi | _(cross-cutting)_ |
| `clean-code-naming` | Review/Fix/Suggest | Engineer | Solution | Multi | _(cross-cutting)_ |
| `clean-code-tests` | Generate/Review/Coverage | Engineer | Solution | Multi | _(cross-cutting)_ |
| `clean-code-commit` | Validate/Generate | Engineer | Solution | Agnostic | _(cross-cutting)_ |

> All clean-code skills are cross-cutting — they apply across all scopes. `clean-code-reviewer`, `clean-code-refactor`, `clean-code-naming`, and `clean-code-tests` support `standard: general | ob`. `clean-code-commit` does not use the standard facet.
>
> `boro-ontologist` is a **platform-independent BORO methodology dependency skill**. It sits beneath the primary facet grid and is loaded by `ob-ontologist` when deeper BORO foundations, patterns, or re-engineering references are required. It is intended for reuse by future BORO-native model skills such as BNOP (Python) and later language-specific variants.

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

### Standard Facet (F6): `general` | `ob`

**Standard** is a second conditional facet — it applies to all clean-code skills except `clean-code-commit`. It controls *which convention set* the skill enforces.

| Value | Convention Set | Source |
|-------|---------------|--------|
| `general` | Clean Code (Robert C. Martin) | `prompts/coding/standards/clean_coding/` |
| `ob` (Python) | BORO Quick Style Guide + Clean Code base | `ob-engineer/references/boro-quick-style-guide.md` |
| `ob` (Rust) | BORO Quick Style Guide (Rust) + Clean Code base | `ob-engineer/references/boro-quick-style-guide-rust.md` |

When `standard=ob`, the skill loads the language-appropriate OB overrides on top of the general set. Where they conflict, OB wins (see conflict table in `boro-skills-plan.md` Part 5). Rules not covered by OB fall back to `general`. The Rust guide includes additional Rust-specific sections (ownership, types, iterators, concurrency) derived from the same BORO design philosophy.

Standard defaults to `general` when omitted.

### Extended Canonical Address (with Topic and Standard)

Full address format: `[Role]:[Mode]:[Scope]:[Language]:[Topic]:[Standard]`

| Canonical Address | Meaning |
|---|---|
| `engineer:review:solution:python:full` | clean-code-reviewer, all topics, general standard |
| `engineer:review:solution:python:full:ob` | clean-code-reviewer, all topics, OB conventions |
| `engineer:review:solution:python:naming` | clean-code-reviewer, naming only, general |
| `engineer:review:solution:python:naming:ob` | clean-code-reviewer, naming only, OB conventions |
| `engineer:refactor:solution:python:naming:ob` | clean-code-refactor, fix naming, OB conventions |
| `engineer:refactor:solution:python:smells` | clean-code-refactor, fix smells, general |
| `engineer:review:pipeline:python:errors:ob` | pipeline engineer reviewing error handling, OB style |

Both Topic and Standard default to `full` / `general` when omitted.

---

## Mode × Role: The Two-Axis Model

```
             ROLE
             ──────────────────────────────────────────────────────────────────
             Architect             Engineer              Ontologist
MODE ────────────────────────────────────────────────────────────────────────────
Design   │   PRIMARY               (upstream input)      (upstream input)
         │   s-arch,
         │   bcl-arch, ob-arch
─────────────────────────────────────────────────────────────────────────────────
Analysis │   (downstream consumer) (downstream consumer) PRIMARY
         │                                               ontologist, ob-ont,
         │                                               bie-comp-ont
─────────────────────────────────────────────────────────────────────────────────
Implement│   (driven by design)    PRIMARY               (model feeds engineer)
         │                         d-eng, py-eng,
         │                         js/cs/rs-eng,
         │                         bie-eng, bcl-eng
─────────────────────────────────────────────────────────────────────────────────
Review   │   embedded in each      cc-reviewer            embedded in each
         │   Architect skill       + embedded in each     Ontologist skill
         │   (gap analysis)        Engineer skill         (model validation)
─────────────────────────────────────────────────────────────────────────────────
Refactor │   structural changes    cc-refactor            (via new analysis)
         │   (via new design)      (code-level only)
```

---

## Skills Space: Scope × Language Grid

```
              LANGUAGE AXIS
              ──────────────────────────────────────────────────────────
              Agnostic       Python   TypeScript   C#     Rust    Multi
              ──────────────────────────────────────────────────────────
S  Solution   data-eng       py-eng   js-eng       cs-eng rs-eng  cc-rev
C             ontologist‡                                          cc-ref
O  Ontology   ob-arch†       ob-eng   ·            ·      ·       ·
P             ob-ontologist‡
E  Pipeline   bcl-arch†      bcl-eng  ·            ·      ·       ·
   Agent      agent-arch†    agent-eng ·           ·      ·       ·
   UI         ui-arch†       ·        ui-eng       ·      ·       ·
   BIE        bie-comp-ont‡  bie-eng  ·            ·      ·       ·
──────────────────────────────────────────────────────────────────────
  † = Architect role (Design mode)
  ‡ = Ontologist role (Analysis mode)
  · = gap (no skill exists for this combination)
  Note: bcl-eng inherits from ob-eng (bclearer is an OB-specific framework)
  Note: bie-comp-ont inherits from ob-ontologist (BIE is an OB/BORO framework)
```

---

## Inheritance Hierarchy

```mermaid
flowchart TD
    subgraph Architect["Role: Architect"]
        SA[software-architect\nSolution]
        BCL_A[bclearer-pipeline-architect\nPipeline]
        OB_A[ob-architect\nOntology]
        SA -->|"extends"| BCL_A
        SA -->|"extends"| OB_A
        SA -->|"extends"| UI_A[ui-architect\nUI]
        OB_A -->|"extends"| AGT_A[agent-architect\nAgent]
    end

    subgraph Ontologist["Role: Ontologist"]
        ONT[ontologist\nSolution · Agnostic]
        OB_ONT[ob-ontologist\nOntology · Agnostic]
        BCO[bie-component-ontologist\nBIE · Agnostic]
        ONT -->|"extends"| OB_ONT
        OB_ONT -->|"extends"| BCO
    end

    BORO_CORE[boro-ontologist\nBORO method · platform-independent]

    subgraph Engineer["Role: Engineer"]
        DE[data-engineer\nSolution · Agnostic]
        PY[python-data-engineer\nSolution · Python]
        JS[javascript-data-engineer\nSolution · TypeScript]
        CS[csharp-data-engineer\nSolution · C#]
        RS[rust-data-engineer\nSolution · Rust]
        BIE_E[bie-data-engineer\nBIE · Python]
        OB_E[ob-engineer\nOntology · Python]
        BCL_E[bclearer-pipeline-engineer\nPipeline · Python]
        AGT_E[agent-engineer\nAgent · Python]

        DE -->|"extends"| PY
        DE -->|"extends"| JS
        DE -->|"extends"| CS
        DE -->|"extends"| RS
        DE -->|"extends"| BIE_E
        JS -->|"extends"| UI_E[ui-engineer\nUI · TypeScript]
        PY -->|"extends"| OB_E
        OB_E -->|"extends"| BCL_E
        OB_E -->|"extends"| AGT_E
    end

    subgraph Quality["Review + Refactor modes · cross-cutting"]
        CCR[clean-code-reviewer]
        CCRF[clean-code-refactor]
        CCR -->|"output feeds"| CCRF
    end

    SA -->|"design feeds"| DE
    BCL_A -->|"design feeds"| BCL_E
    OB_A -->|"design feeds"| OB_E
    AGT_A -->|"design feeds"| AGT_E
    UI_A -->|"design feeds"| UI_E
    BORO_CORE -.->|"loads when needed"| OB_ONT
    OB_ONT -->|"model feeds"| OB_E
    BCO -->|"model feeds"| BIE_E
```

---

## Mode × Scope Lanes

```
MODE:      Design ──► Analysis ──────────► Implement ──────────► Review/Refactor

           ┌────────────┐                  ┌───────────────┐    ╔══════════════╗
Solution   │ software-  │                  │ data-engineer │───►║ clean-code-  ║
           │ architect  │─────────────────►│ (+ language   │    ║ reviewer     ║
           └────────────┘  ┌────────────┐  │  variants)    │    ║ clean-code-  ║
                           │ ontologist │  └───────────────┘    ║ refactor     ║
                           └─────┬──────┘                       ╚══════════════╝
                                 │extends                              ↑
           ┌────────────┐  ┌─────▼──────┐  ┌───────────────┐   applies to
Ontology   │ ob-        │  │ ob-        │  │ ob-engineer   │   all scopes
           │ architect  │  │ ontologist │─►│ (BORO/Ontlgy) │
           └────────────┘  └─────┬──────┘  └───────┬───────┘
                  │              │extends          │extends
                  │        ┌─────▼──────┐  ┌───────▼───────┐
BIE               │        │ bie-comp-  │  │ bie-data-     │
                  │        │ ontologist │─►│ engineer      │
                  │        └────────────┘  └───────────────┘
                  │
           ┌──────▼─────┐                  ┌───────────────┐
Pipeline   │ bclearer-  │────────────────►│ bclearer-     │
           │ pipe-arch  │                  │ pipeline-eng  │
           └────────────┘                  │ (inherits     │
                                           │  ob-engineer) │
                                           └───────────────┘

           ┌────────────┐                  ┌───────────────┐
Agent      │ agent-     │────────────────►│ agent-        │
           │ architect  │                  │ engineer      │
           └────────────┘                  │ (inherits     │
                                           │  ob-engineer) │
                                           └───────────────┘
UI         ┌────────────┐                  ┌───────────────┐
           │ ui-        │────────────────►│ ui-engineer   │
           │ architect  │                  │ (TypeScript)  │
           └────────────┘                  └───────────────┘
```

---

## Structural Observations

### 1. Operation is Fully Derived
Removing Operation as a facet is correct — `Scope + Role` composes it unambiguously. No information is lost; the operation name is readable from any skill's facet address.

### 2. Scope Clarifies What Domain Conflated
The old "Domain" value "bclearer Pipeline" conflated scope (Pipeline) with platform (bclearer). The new model separates these: scope is Pipeline, platform specificity is captured in the skill name and references. This makes the grid extensible to other pipeline platforms.

### 3. UI Scope Is Present but Unpopulated
The UI scope is named in the taxonomy but has no skills yet. This makes the gap explicit and shows where the library needs to grow.

### 4. Planned Inheritance Migration (`bie-data-engineer`)

`bie-data-engineer` currently inherits from `python-data-engineer`. It will eventually inherit from `ob-engineer` (BIE is an OB-specific framework, like bclearer). This change is **deferred** until `ob-engineer` is built and validated in production. `bie-data-engineer` is battle-hardened; its inheritance chain will not be touched until Phase 7 of the skills plan.

The inheritance diagram above reflects the **current** state. When Phase 7 completes, `BIE_E` will move from `DE → BIE_E` to `OB_E → BIE_E`.

### 5. Identified Gaps

| Gap | Facet Coords | Implication |
|---|---|---|
| BIE × non-Python | Implement / Engineer / BIE / TypeScript, C#, Rust | BIE impl locked to Python |
| Pipeline × non-Python | Implement / Engineer / Pipeline / TypeScript, C#, Rust | Pipeline impl locked to Python |
| Agent × non-Python | Implement / Engineer / Agent / TypeScript, C#, Rust | Agent impl locked to Python (ol_ai_services is Python) |
| Ontology × non-Python | Implement / Engineer / Ontology / TypeScript, C#, Rust | `ob-engineer` (Python) exists; other languages still gaps |
| UI × non-TypeScript | Implement / Engineer / UI / Python, C#, Rust | `ui-engineer` (TypeScript) exists; other UI languages still gaps |
| UI × Architect (non-Agnostic) | Design / Architect / UI / Python, C# | `ui-architect` is agnostic; no platform-specific UI architect variants |
| Architect:Refactor | Refactor / Architect / * | No structural refactoring skill |
| Architect:Review (standalone) | Review / Architect / * | Architecture review is embedded, not composable |
| Pipeline × Ontologist | Analysis / Ontologist / Pipeline / * | No pipeline ontologist (pipeline domains analysed via ob-ontologist) |
| Agent × Ontologist | Analysis / Ontologist / Agent / * | No agent ontologist (agent domains analysed via ob-ontologist) |

### 6. BORO Methodology Is Reusable Below the Facet Grid

`boro-ontologist` is intentionally **not** a second canonical ontology-role entry beside
`ob-ontologist`. Instead, it is the reusable BORO methodology layer that `ob-ontologist`
loads when deeper BORO references are needed. This keeps the public skill taxonomy clean
while allowing the same BORO source material to be reused later by BNOP (Python) and
future language-specific BORO-native model skills.

---

## Canonical Skill Address

Format: `[Role]:[Mode]:[Scope]:[Language]`

| Canonical Address | Skill |
|---|---|
| `architect:design:solution:*` | software-architect |
| `architect:design:pipeline:*` | bclearer-pipeline-architect |
| `architect:design:ontology:*` | ob-architect |
| `ontologist:analysis:solution:*` | ontologist |
| `ontologist:analysis:ontology:*` | ob-ontologist |
| `ontologist:analysis:bie:*` | bie-component-ontologist |
| `engineer:implement:solution:*` | data-engineer |
| `engineer:implement:solution:python` | python-data-engineer |
| `engineer:implement:solution:typescript` | javascript-data-engineer |
| `engineer:implement:solution:csharp` | csharp-data-engineer |
| `engineer:implement:solution:rust` | rust-data-engineer |
| `engineer:implement:bie:python` | bie-data-engineer |
| `engineer:implement:ontology:python` | ob-engineer |
| `engineer:implement:pipeline:python` | bclearer-pipeline-engineer |
| `architect:design:agent:*` | agent-architect |
| `engineer:implement:agent:python` | agent-engineer |
| `architect:design:ui:agnostic` | ui-architect |
| `engineer:implement:ui:typescript` | ui-engineer |
| `engineer:review:solution:multi` | clean-code-reviewer |
| `engineer:refactor:solution:multi` | clean-code-refactor |

Auxiliary dependency skill: `boro-ontologist` (platform-independent BORO methodology;
loaded by `ob-ontologist` when required)
