# Agent Architecture Patterns

Reference catalog of agent topology and coordination patterns for use with ol_ai_services.

---

## 1. Single Agent Patterns

### 1.1 Tool-Using Agent

The simplest pattern: one agent with access to a set of tools.

```
Agent
  +-- Model: [LLM]
  +-- System Prompt: [task description + constraints]
  +-- Tools: [tool-1, tool-2, ..., tool-n]
```

**When to use**: Task is well-scoped, one domain, one role.

**ol_ai_services mapping**: Single `AgentConfiguration` with `tool_ids`.

### 1.2 Skill-Wrapped Agent

A single agent packaged as a reusable skill with defined inputs, outputs, and tool scope.

```
SkillDefinition (YAML manifest)
  +-- Agent (transient)
      +-- Model: [from manifest or override]
      +-- System Prompt: [from manifest prompts.system]
      +-- Task Prompt: [from manifest prompts.task, templated]
      +-- Tools: [from manifest spec.tools]
```

**When to use**: Reusable capability invoked by other agents or directly.

**ol_ai_services mapping**: `SkillDefinition` YAML + `SkillExecutionService`.

### 1.3 Memory-Augmented Agent

Agent with recall and persistence for long-running or multi-session tasks.

```
Agent
  +-- Model: [LLM]
  +-- Memory:
  |   +-- Recall: query-based context injection
  |   +-- Persistence: conversation history storage
  |   +-- Consolidation: periodic memory compression
  +-- Tools: [...]
```

**When to use**: Tasks spanning multiple sessions, knowledge accumulation.

**ol_ai_services mapping**: `AgentConfiguration.memory_config` + `AgentMemoryService`.

---

## 2. Multi-Agent Patterns

### 2.1 Orchestrator Pattern

A coordinator agent dispatches tasks to specialist sub-agents.

```
Orchestrator Agent
  +-- Decides which sub-agent to invoke
  +-- Sub-agents:
  |   +-- Research Agent (tools: search, read)
  |   +-- Analysis Agent (tools: compute, query)
  |   +-- Writing Agent (tools: generate, format)
  +-- Aggregates results
```

**When to use**: Complex tasks decomposable into specialist roles.

**ol_ai_services mapping**: `OrchestrationGraph` with `AgentNode` per sub-agent,
conditional `AgentEdge` routing.

### 2.2 Pipeline Pattern (Sequential)

Agents execute in a fixed sequence, each transforming the output for the next.

```
Agent-A -> Agent-B -> Agent-C -> Result
 (collect)  (transform)  (output)
```

**When to use**: Linear processing with clear stage boundaries.

**ol_ai_services mapping**: `OrchestrationGraph` with linear edges, no conditional routing.

### 2.3 Hierarchical Pattern

Agents delegate to sub-agents who may further delegate.

```
Executive Agent
  +-- Manager Agent A
  |   +-- Worker Agent A1
  |   +-- Worker Agent A2
  +-- Manager Agent B
      +-- Worker Agent B1
```

**When to use**: Large-scale tasks requiring multi-level decomposition.

**ol_ai_services mapping**: Nested `AgentConfiguration.sub_agent_ids` + multiple
`OrchestrationGraph` layers.

### 2.4 Peer Review Pattern

Independent agents produce competing outputs, a reviewer selects or synthesizes.

```
Agent-A --+
Agent-B --+-- Reviewer Agent -> Result
Agent-C --+
```

**When to use**: High-stakes outputs benefiting from diverse perspectives.

**ol_ai_services mapping**: Parallel `AgentNode` entries converging to a review node.

### 2.5 Router Pattern

A lightweight agent classifies input and routes to the appropriate specialist.

```
Router Agent
  +-- [intent=research] -> Research Agent
  +-- [intent=code]     -> Coding Agent
  +-- [intent=data]     -> Data Agent
```

**When to use**: Multi-domain entry point with clear intent classification.

**ol_ai_services mapping**: `OrchestrationGraph` with conditional edges keyed on
classification result.

### 2.6 Context Firewall Pattern

Sub-agents operate in isolated contexts to prevent cross-contamination.

```
Orchestrator (owns shared context)
  +-- Sub-agent A (sees only task-A context + shared)
  +-- Sub-agent B (sees only task-B context + shared)
  +-- Sub-agent C (sees only task-C context + shared)
```

**When to use**: When sub-agents handle sensitive or domain-specific context that
should not leak into other sub-agents. Also useful when individual sub-agents need
most of the context window for their own work.

**ol_ai_services mapping**: Separate `AgentConfiguration` per sub-agent with distinct
`system_prompt` and `tool_ids`. Orchestrator passes only relevant input via
`AgentNode.input_mapping`.

---

## 3. Pattern Selection Guide

| Requirement | Recommended Pattern |
|-------------|-------------------|
| Single task, single domain | Tool-Using Agent |
| Reusable capability | Skill-Wrapped Agent |
| Multi-session continuity | Memory-Augmented Agent |
| Specialist sub-tasks | Orchestrator |
| Linear data flow | Pipeline |
| Deep task decomposition | Hierarchical |
| Quality assurance | Peer Review |
| Multi-domain entry | Router |
| Sensitive context isolation | Context Firewall |

---

## 4. Pattern Composition

Patterns compose — a real agent system often combines multiple patterns:

```
Router (pattern 2.5)
  +-- Research Orchestrator (pattern 2.1)
  |   +-- Memory-Augmented Search Agent (pattern 1.3)
  |   +-- Tool-Using Summarizer (pattern 1.1)
  +-- Coding Pipeline (pattern 2.2)
      +-- Skill-Wrapped Linter (pattern 1.2)
      +-- Skill-Wrapped Tester (pattern 1.2)
```

When composing, maintain the BORO principle of explicit orchestration: every coordination
point is a named orchestrator with a clear purpose.

---

## 5. Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **God Agent** | One agent with 20+ tools, no sub-agents | Decompose into orchestrator + specialists |
| **Chatty Agents** | Sub-agents invoke each other in loops | Use orchestration graph with clear DAG |
| **Stateless When Stateful** | No memory config for multi-session task | Add memory configuration |
| **Tool Soup** | Tools not registered in service layer | Register all tools via ToolService |
| **Implicit Orchestration** | Agent chaining via ad-hoc code | Use OrchestrationEngine |
| **Context Overload** | All context loaded upfront | Use progressive disclosure |
| **Unconstrained Agent** | No approval gates or forbidden ops | Define constraints explicitly |
