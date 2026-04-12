# Context Engineering for Agents

Patterns for managing agent context: budgeting, progressive disclosure,
memory architecture, and constraint design.

---

## 1. Context Budget Design

Every agent has a finite context window. The architect must allocate it.

### Context Slot Taxonomy

| Slot | Description | Loading | Mutability |
|------|------------|---------|-----------|
| **System Prompt** | Agent identity, role, constraints | Always | Static per session |
| **Tool Descriptions** | Schemas and usage docs for each tool | Always | Static per config |
| **Memory Recall** | Retrieved relevant past context | Per-invocation | Dynamic |
| **Task Input** | User request + attachments | Per-invocation | Dynamic |
| **Conversation History** | Prior turns in this thread | Accumulated | Growing |
| **Reference Documents** | Domain knowledge, guidelines | On-demand | Static |
| **Scratchpad** | Agent's working notes | During execution | Ephemeral |

### Budget Allocation Principles

1. **System prompt + tools <= 30% of window** — leave room for dynamic content
2. **Memory recall <= 10% of window** — focused retrieval, not exhaustive
3. **Conversation history management** — summarize when history exceeds budget
4. **Reference documents via progressive disclosure** — load only when needed
5. **Reserve >= 25% for model output** — generation needs room
6. **Budget for tool results** — each tool call returns tokens that consume the window

### Budget Template

```
Model: [name] — [context window size] tokens

| Slot                 | Max Tokens | % of Window | Strategy          |
|---------------------|-----------|-------------|-------------------|
| System prompt        |           |             | Always loaded     |
| Tool descriptions    |           |             | Always loaded     |
| Memory recall        |           |             | Top-k by relevance|
| Task input           |           |             | Truncate if over  |
| Conversation history |           |             | Summarize if over |
| Reference docs       |           |             | Load on demand    |
| Tool results buffer  |           |             | Per-invocation    |
| Output reserve       |           |             | Generation buffer |
| TOTAL                |           | 100%        |                   |
```

### Budget Validation

After filling the template, verify:
- Total does not exceed model context window
- No single slot exceeds 40% (prevents one slot from starving others)
- Output reserve is at least 25%
- Dynamic slots (memory + history + tool results) have fallback strategies for overflow

---

## 2. Progressive Disclosure for Agents

Load information in layers, not all at once.

### Layer 1: Always Present (~30% of budget)
- Agent identity and role
- Core constraints and rules
- Tool schemas (names + input/output types + descriptions)

### Layer 2: Loaded on Trigger (~20% of budget)
- Detailed tool usage examples (when tool is about to be used)
- Domain-specific guidelines (when entering that domain)
- Reference documents (when task mentions them)

### Layer 3: Loaded on Demand (~15% of budget)
- Full API documentation (when debugging tool usage)
- Historical context (when task references past work)
- Large data samples (when analysis requires them)

### Design Principle

For each piece of context, ask: "Does the agent need this on every invocation,
or only when a specific condition is met?" If conditional, move it to Layer 2 or 3.

### Disclosure Mechanisms in ol_ai_services

| Mechanism | Layer | Implementation |
|-----------|-------|---------------|
| System prompt | L1 | `AgentConfiguration.system_prompt` |
| Tool schemas | L1 | Automatic from `tool_ids` |
| Memory recall | L2 | `MemoryConfiguration.recall_enabled` — query-triggered |
| Skill references | L2/L3 | `SkillDefinition.spec.prompts.references` — loaded by SkillExecutionService |
| Prompt templates | L2 | `SkillDefinition.spec.prompts.task` — Jinja2 with conditional sections |

---

## 3. Memory Architecture Design

### Memory Configuration Options

```python
MemoryConfiguration:
    engine_type: str          # "vector", "hybrid", "graph"
    recall_enabled: bool      # Auto-recall on each invocation
    max_recall_results: int   # Top-k memories to inject
    max_recall_tokens: int    # Token budget for recalled content
```

### Memory Strategy Selection

| Agent Type | Recall | Persistence | Consolidation | Rationale |
|-----------|--------|------------|---------------|-----------|
| Stateless task agent | Disabled | None | None | Each invocation is independent |
| Conversational agent | Enabled | Conversation history | Summarize after N turns | Maintain thread coherence |
| Knowledge worker | Enabled | Archival + conversation | Periodic merge | Accumulate domain expertise |
| Pipeline agent | Disabled | Execution log only | None | State carried in orchestration, not memory |
| Multi-session researcher | Enabled | Archival | Consolidate per topic | Build knowledge across sessions |

### Memory Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Recall Everything** | Exceeds context budget, dilutes focus | Set strict `max_recall_tokens` |
| **Never Consolidate** | Memory grows unbounded, retrieval quality degrades | Schedule periodic consolidation |
| **Memory as Database** | Using memory for structured data lookup | Use tools for structured queries |
| **No Relevance Filter** | Irrelevant memories injected | Use semantic search with similarity threshold |
| **Duplicate Memories** | Same fact stored multiple times | Consolidation merges duplicates |

---

## 4. Constraint Design

### Constraint Taxonomy

| Constraint Type | Description | Implementation |
|----------------|------------|----------------|
| **Approval Gates** | Actions requiring human confirmation | `interrupt_config` in AgentConfiguration |
| **Forbidden Operations** | Actions the agent must never take | System prompt + tool filtering |
| **Cost Limits** | Token/API call budgets | `max_llm_calls`, `max_tool_calls` in execution config |
| **Scope Boundaries** | What domains/data the agent can access | Tool selection (only provide tools for allowed domains) |
| **Output Constraints** | Format/content requirements for output | System prompt + `output_template` in SkillDefinition |
| **Time Limits** | Maximum execution duration | `timeout_seconds` in execution config |

### Constraint Design Template

```yaml
Constraints:
  approval_gates:
    - action: [what requires approval]
      trigger: [condition]
      approver: [human | supervisor agent]

  forbidden_operations:
    - operation: [what is forbidden]
      reason: [why]
      enforcement: [system prompt | tool omission | middleware]

  cost_limits:
    max_llm_calls: [N]
    max_tool_calls: [N]
    timeout_seconds: [N]

  scope_boundaries:
    allowed_domains: [list]
    allowed_data_sources: [list]
    tool_whitelist: [explicit list of allowed tool_ids]

  output_constraints:
    format: [structured | freeform]
    validation: [schema | template | none]
    max_output_tokens: [N]
```

### Constraint Priority

1. **Safety** — prevent harmful actions (highest priority)
2. **Correctness** — ensure output quality
3. **Cost** — stay within budget
4. **Scope** — stay within domain
5. **Format** — match expected output shape (lowest priority)

### Constraint Enforcement Layers

| Layer | Mechanism | Strength |
|-------|-----------|----------|
| **System prompt** | Natural language instructions | Soft — model may ignore |
| **Tool omission** | Don't give the agent the tool | Hard — cannot circumvent |
| **Interrupt config** | Pause before execution | Hard — requires approval |
| **Middleware** | Pre/post-processing hooks | Hard — code-enforced |
| **Output validation** | Schema check on output | Hard — rejects invalid output |

Best practice: use hard enforcement for safety and correctness constraints,
soft enforcement (system prompt) only for format and style preferences.

---

## 5. Harness Engineering Principles

Industry best practices for agent harness design:

1. **Context is architecture** — treat context window allocation as seriously as
   memory allocation in systems design
2. **Tools are the agent's API** — design them as carefully as any public API;
   the agent is your user
3. **Constraints are features** — well-designed constraints make agents more reliable,
   not less capable
4. **Memory is not free** — every recalled token competes with working memory;
   budget accordingly
5. **Progressive disclosure scales** — load what is needed, when it is needed;
   never load everything upfront
6. **Test with realistic context** — evaluation must use realistic context loads,
   not empty contexts; an agent that works with 100 tokens of context may fail
   at 50,000
7. **Start simple, add complexity reactively** — begin with the simplest agent
   topology; add sub-agents, memory, and orchestration only when a clear need
   emerges from testing
