# Technology Stack

> **How to use this document.** Steering doc — describes WHAT we build with. Authoritative reference
> for downstream design and implementation. If something isn't here, it isn't sanctioned. Adding a
> new language, framework, or major dependency requires a steering refresh, not a silent introduction.

| | |
|---|---|
| **Project** | [name] |
| **Last reviewed** | [YYYY-MM-DD] |
| **Approved by** | [name(s)] |
| **Confluence page** | [URL, set on first publish] |

## Project Type
[One sentence: what kind of project this is — web app, CLI, library, data pipeline, agent, etc.]

## Core Technologies

### Primary Language(s)
- **Language**: [e.g. Python 3.11, Go 1.21, TypeScript 5.x, Rust 1.75]
- **Runtime / compiler**: [as applicable]
- **Language tooling**: [package manager, build tool, formatter]

### Application Architecture
[One paragraph describing the high-level structural pattern: monolith, microservices, pipeline-of-stages, agent-orchestration, plugin-host, etc. Link to the architecture document if one exists.]

### Key Frameworks & Libraries
[The major load-bearing dependencies. Include version constraints. Do not list every transitive dep.]

| Name | Purpose | Version |
|---|---|---|
| [framework] | [why we use it] | [pinned / range] |
| [library] | [why we use it] | [pinned / range] |

### Data Storage
- **Primary storage**: [e.g. PostgreSQL 16, S3, files, in-memory]
- **Caching**: [Redis, in-process, none]
- **Data formats**: [JSON, Parquet, Protocol Buffers, Avro]
- **Schema management**: [Alembic, Liquibase, app-managed]

### External Integrations
- **APIs we depend on**: [list with auth method per integration]
- **Protocols**: [REST, gRPC, WebSocket, message queue]
- **Credential management**: [Vault, env vars, cloud secrets manager]

## Platform Libraries (if applicable)
[For projects on the OL / bclearer stack, list the platform libraries in use. See
`skills/software-architect/references/technology-stack.md` for the canonical inventory. Otherwise
delete this section.]

- **Foundation**: [e.g. nf_common]
- **Domain**: [e.g. bclearer_pdk]
- **Other OL platform libs**: [as applicable]

## Allowlist & Discouraged Libraries
[Governance: which libraries we deliberately do or do not use. New libraries outside the allowlist
require a steering refresh discussion.]

### Allowlist
- [Library / category — approved use cases]

### Discouraged / forbidden
- [Library / category — reason; what to use instead]

## Tooling by Lifecycle Stage

| Stage | Tools |
|---|---|
| Build | [build system, package manager] |
| Lint / format | [linter, formatter] |
| Type check | [tool] |
| Unit tests | [framework] |
| Integration / e2e tests | [framework, harness] |
| Coverage | [tool] |
| Static analysis / security | [tools] |
| Pre-commit hooks | [tool, hook list] |
| CI / CD | [provider, pipeline location] |
| Docs generation | [tool] |

## Frontend / UI Tooling (if applicable)
[Delete if not relevant.]

- **UI framework**: [React, Vue, Svelte]
- **State management**: [Redux, Zustand, signals]
- **Component library**: [internal, vendor]
- **Visualisation**: [Recharts, D3, ECharts]
- **Build / bundler**: [Vite, Webpack]
- **Live reload / dev experience**: [HMR, etc.]

## Deployment & Distribution (if applicable)
- **Target platform**: [cloud, on-prem, desktop, embedded]
- **Distribution**: [SaaS, downloadable, package registry, app store]
- **Installation requirements**: [system prerequisites]
- **Update mechanism**: [how users receive updates]
- **Environments**: [dev, staging, prod — and any specifics on each]

## Technical Requirements & Constraints

### Performance
[Concrete targets, not aspirations.]

- [e.g. p95 API latency < 200ms]
- [e.g. ingest pipeline must process N records/sec]

### Compatibility
- **Operating systems**: [supported targets]
- **Browsers** (if applicable): [supported versions]
- **Standards compliance**: [protocols, file formats]

### Security & Compliance
- **Security requirements**: [authn, authz, encryption at rest / in transit]
- **Compliance standards**: [GDPR, HIPAA, SOC2 — as applicable]
- **Threat model summary**: [key adversaries and trust boundaries]

### Scalability & Reliability
- **Expected load**: [users, requests, data volume, growth projections]
- **Availability target**: [SLO uptime]
- **Disaster recovery**: [RPO, RTO]

## Technical Decisions & Rationale

| # | Decision | Alternatives considered | Why this | Date |
|---|---|---|---|---|
| 1 | [chosen tech / pattern] | [what else was on the table] | [the deciding reason] | [YYYY-MM-DD] |
| 2 | | | | |

## Known Limitations
[Tech debt and acknowledged gaps. Each entry should say what it costs us today and when we'd consider addressing it.]

- **[Limitation]**: [impact today, conditions under which we'd revisit]
