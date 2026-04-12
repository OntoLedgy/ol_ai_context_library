# ol_ai_services Architecture Map

Reference map of the ol_ai_services agent development kit. Use this to identify
available components before designing custom ones.

**Source**: [ol_ai_services/agent_dev_kit](https://github.com/OntoLedgy/ol_artificial_intelligence_interop_services/tree/master/ol_ai_services/agent_dev_kit)

---

## Service Architecture Overview

```
AgentDevelopmentKitFacade (unified entry point)
+-- AgentService              -- Agent configuration CRUD + validation
+-- ToolService               -- Tool registration, resolution, query
+-- ExecutionService          -- Execution lifecycle + WebSocket events
+-- AgentFactory              -- Agent instantiation from config (LangGraph)
+-- OrchestrationEngine       -- Multi-agent DAG execution
+-- PromptService             -- Prompt template management
+-- OrchestrationGraphManager -- Graph persistence
+-- AgentMemoryService        -- Recall, persist, consolidate
+-- SkillExecutionService     -- Skill invocation pipeline
    +-- SkillRegistry         -- Manifest discovery from skills directory
    +-- SkillTemplateRenderer -- Jinja2 prompt rendering
    +-- (uses AgentFactory + ToolService + AgentExecutionRuntime)
```

---

## Key Components

### Agent Configuration

```
AgentConfiguration:
    agent_id: UUID
    workspace_id: UUID
    name: str
    description: str
    model_name: str               # e.g., "claude-sonnet-4-6", "gpt-4"
    system_prompt: str
    prompt_template_id: UUID      # optional reference to stored template
    tool_ids: List[str]           # tools available to this agent
    sub_agent_ids: List[str]      # for hierarchical composition
    backend_storage: StorageStrategy  # PERSISTENT | EPHEMERAL | FILESYSTEM
    middleware_config: Dict       # custom middleware hooks
    interrupt_config: Dict        # human-in-the-loop (approval gates)
    memory_config: MemoryConfiguration
```

### Tool System

**Source types:**

| Type | Description | Resolution |
|------|-----------|-----------|
| `RUNTIME` | Live instance registered at runtime | Lookup from in-memory dict |
| `PACKAGE` | Importable Python class | Dynamic import via `importlib` |
| `BUILTIN` | deepagents built-in (filesystem, todo, shell, delegation) | Framework provides |
| `INTEROP` | Remote service via MCP/REST | Interop client discovery |

**BaseTool contract:**

```
BaseTool (ABC):
    name: str
    description: str
    input_schema: Type[ToolInput]    # Pydantic model
    output_schema: Type[ToolOutput]  # Pydantic model

    _run(*, input_data: ToolInput) -> ToolOutput   # abstract
    run(**kwargs) -> ToolOutput                     # validates + calls _run
```

**Key operations:**
- `ToolService.register_tool(tool)` — stores metadata in DB + runtime instance in memory
- `ToolService.resolve_tools(tool_ids)` — resolves by source type strategy
- `ToolService.list_tools(workspace_id)` — query registered tools

### Interop System

**Transport types:** MCP (SSE/stdio), REST (HTTP), DIRECT (Python import)

**InteropServiceConfigs:**

```
InteropServiceConfigs:
    service_name: str              # human-readable name
    transport: TransportTypes      # MCP | REST | DIRECT
    endpoint: str                  # URL or stdio command
    auth_config: Optional[Dict]    # auth credentials
    tool_prefix: Optional[str]     # prefix for discovered tools
    timeout_seconds: int = 30
    discovery_enabled: bool = True
    retry_config: Optional[RetryConfigs]
```

**Client lifecycle:**

```python
async with interop_client_factory.create_and_connect(config) as client:
    tools = await client.discover_tools()   # returns List[BaseTool]
    result = await client.invoke_tool(name, **kwargs)
```

**MCP Tool Factory**: Dynamically generates BaseTool subclasses from MCP tool
definitions at runtime. Converts JSON Schema to Pydantic models and generates
async `_run()` methods bound to the client callback.

### Skill System

**SkillDefinition manifest (YAML):**

```yaml
apiVersion: ol.ai/v1
kind: Skill
metadata:
    name: skill_name
    version: "1.0"
    category: prompt_category
spec:
    model:
        default: "claude-sonnet-4-6"
        allowed: ["claude-sonnet-4-6", "claude-opus-4-6"]
    input_schema: {JSON Schema}
    output_schema: {JSON Schema}
    tools:
        - name: tool_name
          source: PACKAGE | INTEROP
          implementation_class: module.path.ToolClass
          service: service_name  # if INTEROP
    prompts:
        system: path/to/system_prompt.md
        task: path/to/task_template.md
        references: [paths...]
    output_template: "Jinja2 template"
    execution:
        timeout_seconds: 120
        max_llm_calls: 10
        max_tool_calls: 20
        memory: {MemoryConfiguration}
```

**Skill invocation pipeline:**
1. Validate input against `input_schema`
2. Select model (with override support)
3. Load and render prompts (system + task + references)
4. Resolve tools (PACKAGE via import, INTEROP via client)
5. Execute transient agent with timeout
6. Render output template, validate against `output_schema`
7. Return result with metrics

### Orchestration System

**OrchestrationGraph:**

```
OrchestrationGraph:
    orchestration_id: UUID
    workspace_id: UUID
    name: str
    description: str
    nodes: List[AgentNode]        # agent_id + input_mapping
    edges: List[AgentEdge]        # from_node -> to_node + conditional route
    entry_node_id: str
```

**Execution**: BFS traversal from entry node. For each node: create execution,
run agent, evaluate conditional routes on outgoing edges, follow edges with
satisfied conditions.

### Execution Lifecycle

```
PENDING -> RUNNING -> COMPLETED
                   -> FAILED
```

Each transition broadcasts WebSocket events. Metrics captured: duration,
LLM calls, tool calls.

**AgentExecutionRuntime flow:**
1. Load agent configuration
2. Create execution record (PENDING)
3. Create agent via AgentFactory
4. Inject recalled memories as system context
5. Invoke agent (RUNNING)
6. Extract output and metrics
7. Complete execution (COMPLETED) or fail (FAILED)

### Memory System

```
AgentMemoryService:
    recall_for_context(query, config) -> memories    # injected before LLM call
    store_conversation(execution) -> stored           # post-execution
    store_archival(content) -> stored                  # manual important docs
    consolidate(agent_id) -> consolidated              # merge + compress
```

Token budgeting with fallback tokenizer (tiktoken or whitespace-based).

---

## Available Built-in Tools (deepagents)

| Tool | Category | Description |
|------|----------|------------|
| `filesystem` | I/O | File read, write, search |
| `todo` | Management | Task tracking |
| `shell` | System | Command execution |
| `delegation` | Orchestration | Sub-agent invocation |

---

## Configuration Patterns

### Environment Variables
- `{SERVICE_NAME}_ENDPOINT` or `{SERVICE_NAME}_MCP_ENDPOINT`
- `{SERVICE_NAME}_TOOL_PREFIX`
- `{SERVICE_NAME}_AUTH_*`

### Database Abstraction
- All persistence via `DatabaseFacade` (PostgreSQL + SQLite)
- Schema management via `schema_loader.execute_schema_file()`
- Workspace isolation on all entities

### Checkpointer
- Shared `MemorySaver` across all agent instances
- `thread_id` determines conversation history lookup
- Supports cross-conversation memory via `InMemoryStore`

---

## Dependency Graph

```
AgentDevelopmentKitFacade
  |
  +-- AgentService
  |     +-- AgentConfigurationManager (DB persistence)
  |
  +-- ToolService
  |     +-- ToolRegistryManager (DB persistence)
  |     +-- _runtime_tools (in-memory dict)
  |
  +-- ExecutionService
  |     +-- ExecutionHistoryManager (DB persistence)
  |     +-- WebSocket broadcaster
  |
  +-- AgentFactory
  |     +-- DeepAgentsWrapper (LangGraph abstraction)
  |     +-- LangChainClientFactory (LLM creation)
  |     +-- MemorySaver (shared checkpointer)
  |
  +-- OrchestrationEngine
  |     +-- AgentFactory (creates sub-agent network)
  |     +-- ExecutionService (per-node execution)
  |
  +-- AgentMemoryService
  |     +-- Memory engine (vector/hybrid/graph)
  |
  +-- SkillExecutionService
        +-- SkillRegistry
        +-- SkillTemplateRenderer
        +-- AgentFactory
        +-- ToolService
        +-- AgentExecutionRuntime
```
