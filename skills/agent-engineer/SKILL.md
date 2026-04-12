---
name: agent-engineer
description: >
  Agent implementation skill. Extends ob-engineer with agent-specific construction
  patterns using ol_ai_services agent_dev_kit: BaseTool implementation, interop
  client configuration, agent configuration wiring, orchestration graph building,
  skill manifest creation, and memory integration. When tools or components are
  missing from ol_ai_services, implements them following BaseTool and interop
  contracts for registration into the service layer. Use when: implementing an
  agent from an approved architecture design, building tools for agent use,
  creating skill manifests, wiring orchestration graphs, or reviewing agent
  implementation code. Canonical address: engineer:implement:agent:python.
---

# Agent Engineer

## Role

You are an agent engineer. You extend the `ob-engineer` role with agent-specific
implementation patterns using `ol_ai_services.agent_dev_kit`.

**Read `skills/ob-engineer/SKILL.md` first and follow all of it.** Then read
`skills/python-data-engineer/SKILL.md` and `skills/data-engineer/SKILL.md`
(ob-engineer's parents). This file contains only the additions and overrides
that apply to agent building work.

---

## Session Start — Verify Platform

Before implementing, confirm the agent platform:

1. Verify `ol_ai_services` is importable in the target project
2. Read `skills/agent-architect/references/ol-ai-services-map.md`
   for the correct import paths and available components
3. Read `references/ob-library-selection.md` (inherited from ob-engineer) to confirm
   the active OB variant
4. If `ol_ai_services` is not available, raise to the architect — do not implement
   without the platform

---

## Additional References

| Reference | Content |
|-----------|---------|
| `references/agent-implementation.md` | Construction order, code layout, agent configuration patterns, orchestration graphs, runners |
| `references/tool-implementation.md` | BaseTool subclass patterns, Pydantic schemas, registration, testing |
| `references/interop-implementation.md` | MCP/REST client configuration, tool discovery, service wiring |
| `references/skill-manifest.md` | SkillDefinition YAML creation, prompt file layout, progressive disclosure, evaluation |

---

## Construction Order

Build agent components in this order (leaf-before-whole):

```
1. Common knowledge    — enums, types, constants for the agent domain
2. Tool implementations — BaseTool subclasses for each MISSING tool
3. Interop configs      — InteropServiceConfigs for each INTEROP tool
4. Agent configuration  — AgentConfiguration with model, tools, memory, constraints
5. Orchestration graph  — (if multi-agent) nodes, edges, conditional routes
6. Skill manifest       — (if packaging as skill) YAML + prompts + references
7. Runner / entry point — wire everything, create facade calls
8. Tests                — tool unit tests -> config tests -> graph tests -> E2E tests
```

---

## Code Layout Convention

```
[agent_name]/
+-- common_knowledge/               # agent-domain enums, types, constants
|   +-- tool_name_enums.py          # registered tool name constants
|   +-- model_config_enums.py       # model name and parameter constants
|   +-- prompt_constants.py         # system prompt fragments as constants
+-- tools/                          # custom tool implementations
|   +-- [verb]_[subject]_tools.py   # one BaseTool subclass per file
|   +-- [verb]_[subject]_tool_inputs.py
|   +-- [verb]_[subject]_tool_outputs.py
+-- interop/                        # interop service configurations
|   +-- [service]_interop_configs.py
+-- configurations/                 # agent configurations
|   +-- [agent_name]_configurations.py
+-- orchestration/                  # multi-agent orchestration (if needed)
|   +-- [agent_name]_orchestration_graphs.py
+-- skills/                         # skill manifests (if packaging as skill)
|   +-- skill.yaml                  # SkillDefinition manifest
|   +-- prompts/
|   |   +-- system_prompt.md
|   |   +-- task_template.md
|   +-- references/
+-- runners/                        # entry points
|   +-- [agent_name]_runners.py
+-- tests/
    +-- test_tools/                 # tool unit tests
    +-- test_configurations/        # configuration validation tests
    +-- test_orchestration/         # graph validation tests
    +-- test_integration/           # agent E2E tests
```

---

## Implementation Patterns

### Step 1: Common Knowledge

All domain vocabulary as enums — no hardcoded strings in processing logic.

```python
# tool_name_enums.py
from enum import Enum


class ToolNameEnums(
    Enum,
):
    SEARCH_DOCUMENTS = (
        "search_documents"
    )
    CREATE_ISSUE = (
        "create_issue"
    )
```

```python
# model_config_enums.py
from enum import Enum


class ModelConfigEnums(
    Enum,
):
    DEFAULT_MODEL = (
        "claude-sonnet-4-6"
    )
    REASONING_MODEL = (
        "claude-opus-4-6"
    )
```

### Step 2: Tool Implementation

Follow `references/tool-implementation.md` for the full BaseTool pattern.

Key rules:
- One tool class per file (OB convention: one public function per file)
- Class name: `VerbSubjectTools` (plural CamelCase, BORO naming)
- All parameters use named kwargs with `*` enforcement
- Input/output as Pydantic models with full type annotations
- Errors returned in output schema, never raised from `_run()`
- Register via `ToolService.register_tool()`

### Step 3: Interop Configuration

Follow `references/interop-implementation.md` for service wiring.

Key rules:
- One config factory per external service
- Transport selection: MCP for standardized tools, REST for legacy APIs, DIRECT for Python libs
- Configuration values from enums, not hardcoded strings
- Auth config from environment variables (read once at entry point)

### Step 4: Agent Configuration

Follow `references/agent-implementation.md` for configuration patterns.

Key rules:
- Factory function returns `AgentConfiguration` (not direct instantiation in runner)
- Model name from `ModelConfigEnums`
- System prompt as constant or loaded from file
- Memory config matches architect's design
- All named parameters with `*` enforcement

### Step 5: Orchestration Graph (if multi-agent)

Follow `references/agent-implementation.md` for graph patterns.

Key rules:
- Graph must be a valid DAG (no cycles)
- Each node maps to an existing `AgentConfiguration`
- Conditional routes use `on_status` for edge evaluation
- Entry node explicitly declared

### Step 6: Skill Manifest (if packaging as skill)

Follow `references/skill-manifest.md` for YAML manifest creation.

Key rules:
- Manifest metadata triggers auto-discovery (description must be specific)
- Progressive disclosure: L1 metadata, L2 prompts, L3 references
- Input/output schemas as JSON Schema
- Evaluation queries for testing (10+ cases)

### Step 7: Runner / Entry Point

Follow `references/agent-implementation.md` for runner wiring.

Key rules:
- Environment variables read once at this level only
- Custom tools registered before agent creation
- Interop tools discovered and registered before agent creation
- Facade used for all lifecycle operations
- Thread ID passed through for conversation continuity

### Step 8: Tests

Follow construction order for tests:

| Test Level | Scope | Dependencies |
|-----------|-------|-------------|
| Tool unit tests | Each tool in isolation | Mock external services |
| Configuration tests | Agent config is well-formed | No external deps |
| Orchestration tests | Graph is valid DAG | No external deps |
| Integration tests | Agent executes end-to-end | Real tools, real facade |

---

## Sub-Skill Delegation

| Sub-task | Delegate to |
|----------|------------|
| Domain enums and BIE objects | `bie-data-engineer` |
| BIE component model (if no model exists) | `bie-component-ontologist` |
| MCP server implementation | Use `references/interop-implementation.md` |
| Skill manifest creation | Use `references/skill-manifest.md` |

---

## Verification Checklist

After implementation, verify:

- [ ] All custom tools extend `BaseTool` with proper Pydantic schemas
- [ ] All tools registered via `ToolService` (not ad-hoc instantiation)
- [ ] Interop service configs only in `interop/` directory
- [ ] Agent configuration uses enum constants, not hardcoded strings
- [ ] System prompt stored as constant or file, not inline in runner
- [ ] Memory configuration matches architect's design
- [ ] Orchestration graph is a valid DAG (no cycles)
- [ ] Each tool independently testable
- [ ] No module-level mutable state
- [ ] All parameters use named kwargs with `*` enforcement (OB convention)
- [ ] All type annotations present on params and returns (OB convention)
- [ ] Class names plural CamelCase (OB convention)
- [ ] One public function per file (OB convention)
- [ ] Private methods use `__double_underscore` (OB convention)
- [ ] No hardcoded strings — all in enums/constants (OB convention)
- [ ] Environment variables read once at runner level only

---

## Quality Gates

```bash
ruff check src/                    # linting
ruff format src/                   # formatting (20-char line discipline via review)
mypy src/ --strict                 # type checking in strict mode
pytest tests/test_tools/           # tool unit tests pass
pytest tests/test_configurations/  # config validation tests pass
pytest tests/test_orchestration/   # graph validation tests pass
pytest tests/test_integration/     # E2E tests pass
```

---

## Review Mode

When reviewing existing agent code, check against:

| Principle | Expected | Signal if Missing |
|-----------|----------|------------------|
| Tool registration | All tools via ToolService | Direct tool instantiation without registration |
| BaseTool contract | All tools extend BaseTool with schemas | Custom tool interfaces, no Pydantic schema |
| Interop boundary | Interop configs in `interop/` only | API calls scattered through agent logic |
| Configuration as code | AgentConfiguration objects via factory | Raw dict configs, hardcoded model names |
| Constants layer | Enums for tool names, model names, prompts | Hardcoded strings throughout |
| Memory config | Explicit MemoryConfiguration | No memory config, or memory wired ad-hoc |
| Orchestration explicit | OrchestrationGraph with named nodes/edges | Implicit agent chaining via code |
| Test coverage | Tests for tools, config, orchestration, E2E | No tests, or only integration tests |
| OB conventions | Named params, typed, plural classes, one-function files | PEP 8 defaults in OB codebase |
| Construction order | Leaf-before-whole build sequence | Monolithic setup, circular dependencies |

Severity classification:
- **CRITICAL**: Tools not registered (unreusable); no BaseTool contract (unresolvable); circular dependencies
- **MAJOR**: Missing tests; ad-hoc interop; no constants layer; missing type annotations
- **MINOR**: Naming inconsistencies; suboptimal construction order; loose memory config
