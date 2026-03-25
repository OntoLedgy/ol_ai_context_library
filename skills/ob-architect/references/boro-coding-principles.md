# BORO Coding Principles — Architectural Translations

This file captures how BORO coding conventions, when lifted to the architectural level,
produce specific structural patterns. These principles guide `ob-architect` during both
Design Mode and Review Mode.

Source: BORO/Ontoledgy Confluence space (BORO Clean Coding sections). Each section
identifies its source convention.

---

## 2.1 Actor-Action Module Architecture

**Source:** File naming convention (actor files + action functions); file rename rule

Every architectural component is named as an **actor** — what it IS (noun). Its primary
public interface expresses its **action** — what it DOES (verb). Renaming the action
renames the actor.

**Architectural implications:**
- No "utility" modules — every module is a purposeful actor
- Each component has one public API entry point by default
- Module identity is tied to its function; if its purpose changes, it must be redesigned
- Component naming: `[domain_noun]_[role].py` with `do_action()` as the public function

**In architecture documents:**
- All component names follow actor naming (e.g. `TransactionLoader`, `IdentityResolver`)
- Each component box in diagrams shows its public action alongside its name

---

## 2.2 Orchestration as First-Class Architectural Concern

**Source:** Orchestrator pattern; nested orchestrators

Multi-step processes are managed by explicitly named orchestrators. Orchestrators compose
other orchestrators, creating a visible pipeline hierarchy.

**Architectural implications:**
- Architecture must designate orchestration layers explicitly
- Clear separation between orchestration logic (what runs next) and execution logic (what is done)
- Orchestrators are visible in architecture diagrams — not implicit `main()` functions
- Orchestrator hierarchy maps directly to the solution's processing stages
- Canonical naming: `orchestrate_[stage_name]()` in `[stage_name]_orchestrator.py`
- Nested orchestrators represent the decomposition hierarchy visually

**In architecture documents:**
- Every multi-step solution has a named orchestration layer in the component diagram
- Orchestration chain is explicit: `run_pipeline → orchestrate_ingest → orchestrate_identify → ...`

---

## 2.3 Constant / Enum Configuration Layer

**Source:** No hardcoded strings; constants in separate files; enums in separate classes

All domain vocabulary — type names, column names, status values, configuration keys — is
separated from processing logic in a dedicated constants/enums layer.

**Architectural implications:**
- A constants/configuration layer is mandatory in every solution architecture
- Domain vocabulary is a first-class architectural concern
- Enums create self-documenting, type-safe APIs across component boundaries
- Changing domain vocabulary only touches the constants layer

**In architecture documents:**
- Constants/enums layer appears as a distinct architectural component
- Processing components depend on the constants layer, not the reverse

---

## 2.4 Explicit Contract Architecture

**Source:** Mandatory type annotations; mandatory named parameters; return type declarations

All component interfaces are fully specified with types. Named parameters enforce clarity
at call sites. No implicit duck-typing contracts across module boundaries.

**Architectural implications:**
- All public APIs carry full type contracts (parameters and return types)
- Component integration is verifiable without runtime testing
- `*` parameter enforces named-only calling at architectural boundaries
- API design: simple calls for common cases; all complex cases still possible

**In architecture documents:**
- Component interfaces include full type signatures
- Integration points between components are specified with their parameter and return types

---

## 2.5 Fail-Fast Boundary Design

**Source:** Fail Fast principle; specific exception handling

Validation occurs at ingress points. Specific exception types are used at each layer.
No silent failures.

**Architectural implications:**
- Validation is architecturally located at system boundaries (ingress adapters, entry points)
- Error propagation paths are designed, not ad hoc
- Exception types are domain-specific; each layer defines its own exception vocabulary
- Architecture designates which components are validation gates

**In architecture documents:**
- Ingress validation components are explicitly named in the design
- Error flow is included in the component interaction diagram

---

## 2.6 Library-First Platform Design

**Source:** Check `nf_common` first; DRY rule

Every solution is designed against an inventory of available platform libraries.
Custom code is only written when no platform function exists.

**Architectural implications:**
- Platform library inventory is an input to solution design, not an afterthought
- Architecture explicitly maps which platform library provides each cross-cutting function
- Custom components only appear when platform coverage is absent
- Platform dependencies are explicit in architecture documents

**In architecture documents:**
- Technology mapping includes a platform library column: "What does the platform provide?"
- Rationale is required for every custom component that overlaps with platform scope

---

## 2.7 Minimal Surface Area

**Source:** YAGNI; one-public-function-per-file; no speculative abstractions

Architectural scope is strictly bounded by current requirements. Each component exposes
the minimum interface needed.

**Architectural implications:**
- No speculative architectural components for hypothetical future requirements
- Feature scope is negotiated before design begins
- Component interfaces are minimal by default — extended only when proven necessary
- Over-engineering is an architectural defect, not a virtue

**In architecture documents:**
- Open questions section must capture scope negotiations; nothing speculative is included in the design
- Components without a current use case are not included

---

## 2.8 Decomposition Hierarchy

**Source:** Function decomposition into sub-functions; private functions hidden behind public interface

Architectural components have internal hierarchies. The public interface hides implementation
complexity.

**Architectural implications:**
- Architecture is described at multiple levels: L1 orchestrators → L2 workers → L3 helpers
- Each level has its own actor-action naming
- Internal complexity is an implementation detail; only public interfaces appear in top-level diagrams
- Nested orchestrators represent the decomposition hierarchy visually

**In architecture documents:**
- Top-level diagram shows L1 orchestrators and their public interfaces only
- Drill-down diagrams are produced for complex components when requested
