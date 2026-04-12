# Tool Design Guidelines

How to design tools for registration into ol_ai_services. Covers gap analysis,
BaseTool design, MCP server design, and interop configuration.

---

## 1. Tool Gap Analysis Method

For every capability the agent needs, determine whether ol_ai_services already provides it.

### Step 1: Check Built-in Tools

deepagents provides built-in tools:
- `filesystem` — file read/write/search
- `todo` — task management
- `shell` — command execution
- `delegation` — sub-agent invocation

If the need maps to a built-in, use `source_type: BUILTIN`.

### Step 2: Check Registered Package Tools

Search the tool registry for existing PACKAGE tools:

```python
tool_service.list_tools(
    workspace_id=workspace_id,
)
```

If a matching tool exists, reference its `tool_id` in the agent configuration.

### Step 3: Check Interop Services

Check if an external service provides the capability via MCP or REST:
- Review existing `InteropServiceConfigs` in the configuration
- Check for MCP servers that expose the needed operations
- Check community MCP servers for the domain

If available, use `source_type: INTEROP`.

### Step 4: Design New Tool

If no existing source covers the need, design a new tool for registration.

---

## 2. Tool Design Spec Template

For each MISSING tool identified in the gap analysis:

```yaml
Tool Design Spec:
  name: [snake_case, action-oriented verb + subject]
  description: >
    [Clear description of what this tool does, when to use it,
     key parameters, and limitations]
  source_type: [RUNTIME | PACKAGE | INTEROP]

  input_schema:
    type: object
    properties:
      [param_name]:
        type: [string | integer | boolean | array | object]
        description: [what this parameter controls]
    required: [list of required params]

  output_schema:
    type: object
    properties:
      [field_name]:
        type: [type]
        description: [what this field contains]
      success:
        type: boolean
        description: whether the operation succeeded
      error_message:
        type: string
        description: error details if success is false

  implementation_approach:
    class_name: [PascalCase, plural BORO naming — VerbSubjectTools]
    module_path: [Python import path]
    dependencies: [external packages needed]

  error_handling:
    [error_condition]: [how to handle — return in output, never raise]

  constraints:
    timeout_seconds: [max execution time]
    idempotent: [true | false]
    read_only: [true | false]
    destructive: [true | false]
```

### Naming Conventions (OB/BORO)

| Artefact | Convention | Example |
|----------|-----------|---------|
| Tool name (string) | `snake_case`, verb + subject | `search_documents`, `create_issue` |
| Tool class | Plural CamelCase, `VerbSubjectTools` | `SearchDocumentTools` |
| Input schema | Plural CamelCase, `VerbSubjectToolInputs` | `SearchDocumentToolInputs` |
| Output schema | Plural CamelCase, `VerbSubjectToolOutputs` | `SearchDocumentToolOutputs` |
| Module file | `verb_subject_tools.py` | `search_document_tools.py` |

### Description Quality Checklist

Tool descriptions are the agent's API documentation — they must be precise:

- [ ] **Lead with what it does**: "Searches documents in the knowledge base by semantic query"
- [ ] **Include when to use**: "Use when the user asks about existing documentation"
- [ ] **Mention key parameters**: "Requires a query string; optionally filters by date range"
- [ ] **Note limitations**: "Returns max 10 results; does not search attachments"

### BaseTool Contract

Every tool must implement:

```python
class VerbSubjectTools(BaseTool):
    name: str = "verb_subject"
    description: str = "Clear description"
    input_schema: Type[ToolInput] = VerbSubjectToolInputs
    output_schema: Type[ToolOutput] = VerbSubjectToolOutputs

    async def _run(
        self,
        *,
        input_data: VerbSubjectToolInputs,
    ) -> VerbSubjectToolOutputs:
        ...
```

### Error Handling Principle

Tools return errors in the output schema — they do not raise exceptions from `_run()`.
The agent needs structured error information to decide what to do next. Include a
`success: bool` and `error_message: str` in every output schema.

---

## 3. MCP Server Design Guidelines

When a tool should be a standalone service accessible by multiple agents.

### When to Design an MCP Server

| Signal | Recommendation |
|--------|---------------|
| Tool wraps a stateful external service | MCP server |
| Tool needed by multiple agents across workspaces | MCP server |
| Tool requires separate authentication | MCP server |
| Tool is a simple pure function | Package tool (no server needed) |
| Tool is agent-specific, not reusable | Runtime tool (no server needed) |

### MCP Server Design Spec Template

```yaml
MCP Server Design:
  name: [service-name]-mcp
  transport: [stdio | sse]

  tools:
    - name: [tool_name]
      description: [description]
      input_schema: {JSON Schema}
      annotations:
        readOnlyHint: [true | false]
        destructiveHint: [true | false]
        idempotentHint: [true | false]
        openWorldHint: [true | false]

  authentication:
    type: [none | bearer | oauth2.1]

  pagination:
    supported: [true | false]
    pattern: [offset | cursor]
    fields: [has_more, next_offset/next_cursor, total_count]

  error_handling:
    standard_errors: [list of error types]
    error_format: structured JSON with code, message, details
```

### MCP Naming Conventions

| Artefact | Pattern | Example |
|----------|---------|---------|
| Server package (Python) | `{service}_mcp` | `document_search_mcp` |
| Server package (TypeScript) | `{service}-mcp-server` | `document-search-mcp-server` |
| Tool names | `snake_case`, action-oriented | `search_documents`, `get_document_by_id` |
| Service prefix | lowercase, short | `docsearch` |

### MCP Best Practices

1. **Tool naming**: `snake_case`, service prefix, action-oriented verbs
2. **Response format**: Support both JSON and Markdown
3. **Pagination**: Always implement with `has_more`, `next_offset`/`next_cursor`, `total_count`
4. **Transport**: Streamable HTTP (SSE) for remote, stdio for local
5. **Security**: OAuth 2.1 for remote, input validation via Zod/Pydantic
6. **Tool annotations**: Always provide `readOnlyHint`, `destructiveHint`, `idempotentHint`

---

## 4. Interop Configuration Design

For each INTEROP tool, design the service configuration:

```yaml
InteropServiceConfig:
  service_name: [human-readable name]
  transport: [MCP | REST | DIRECT]
  endpoint: [URL or stdio command]
  auth_config: [if needed]
  tool_prefix: [optional prefix for discovered tools]
  timeout_seconds: [default 30]
  discovery_enabled: [true — unless manually registering tools]
  retry_config:
    max_retries: 3
    backoff_factor: 2
```

### Transport Selection Guide

| Criterion | MCP | REST | DIRECT |
|-----------|-----|------|--------|
| Tool discovery | Automatic | Manual endpoint mapping | Import-based |
| Schema enforcement | MCP protocol | OpenAPI / manual | Python types |
| Deployment | Separate process | HTTP server | Same process |
| Best for | Standardized tool servers | Legacy HTTP APIs | Internal Python libraries |

---

## 5. Tool Registration Path

The architect designs; the engineer registers. But every tool design must include
a clear registration path:

| Source Type | Registration Path |
|-------------|------------------|
| RUNTIME | `tool_service.register_tool(tool_instance)` |
| PACKAGE | `tool_service.register_tool(tool_instance)` — tool auto-detected as PACKAGE |
| BUILTIN | Framework provides — no explicit registration needed |
| INTEROP | `interop_client.discover_tools()` then `tool_service.register_tool()` per tool |

---

## 6. Tool Design Checklist

Before handing off to the engineer:

- [ ] Tool name follows `verb_subject` convention
- [ ] Description is agent-readable (what, when, params, limits)
- [ ] Input schema has required/optional clearly marked with descriptions
- [ ] Output schema includes `success` and `error_message` fields
- [ ] Source type selected with rationale
- [ ] Registration path documented
- [ ] Error handling returns structured output (no exceptions)
- [ ] Constraints specified (timeout, idempotency, read-only, destructive)
- [ ] If MCP: server spec complete with annotations and pagination
- [ ] If INTEROP: service config complete with transport and auth
