# Interop Implementation Guide

How to configure and use interop clients for MCP and REST services in ol_ai_services.

---

## 1. InteropServiceConfigs

Every external service connection is defined by an `InteropServiceConfigs` object:

```python
from ol_ai_services.agent_dev_kit.objects.interop_service_configs import (
    InteropServiceConfigs,
)
from ol_ai_services.agent_dev_kit.objects.transport_types import (
    TransportTypes,
)
from ol_ai_services.agent_dev_kit.objects.interop_service_configs import (
    RetryConfigs,
)


def create_service_interop_config(
    *,
    endpoint: str,
    auth_token: str | None = None,
) -> InteropServiceConfigs:
    return InteropServiceConfigs(
        service_name=(
            "Human-Readable "
            "Service Name"
        ),
        transport=TransportTypes.MCP,
        endpoint=endpoint,
        auth_config=(
            {"bearer_token": auth_token}
            if auth_token
            else None
        ),
        tool_prefix="service",
        timeout_seconds=30,
        discovery_enabled=True,
        retry_config=RetryConfigs(
            max_retries=3,
            backoff_factor=2,
        ),
    )
```

---

## 2. MCP Client Usage

### Stdio Transport (Local MCP Server)

```python
config = InteropServiceConfigs(
    service_name=(
        "Local Document Search"
    ),
    transport=TransportTypes.MCP,
    endpoint=(
        "npx -y "
        "@myorg/document-search-mcp"
    ),
    discovery_enabled=True,
)
```

### SSE Transport (Remote MCP Server)

```python
config = InteropServiceConfigs(
    service_name=(
        "Remote Document Search"
    ),
    transport=TransportTypes.MCP,
    endpoint=(
        "https://mcp.example.com/sse"
    ),
    auth_config={
        "bearer_token": token,
    },
    discovery_enabled=True,
)
```

### Tool Discovery and Registration

```python
from ol_ai_services.agent_dev_kit.interop.interop_client_factories import (
    InteropClientFactories,
)

factory = InteropClientFactories()

async with (
    factory.create_and_connect(
        config=config,
    ) as client
):
    # Discover all tools from
    # the service
    discovered_tools = (
        await client.discover_tools()
    )

    # Register each discovered tool
    for tool in discovered_tools:
        await tool_service.register_tool(
            tool=tool,
            workspace_id=workspace_id,
        )

    # Or invoke a specific tool
    # directly
    result = (
        await client.invoke_tool(
            tool_name=(
                "search_documents"
            ),
            query=(
                "agent architecture"
            ),
            max_results=10,
        )
    )
```

---

## 3. REST Client Usage

```python
config = InteropServiceConfigs(
    service_name="Legacy API",
    transport=TransportTypes.REST,
    endpoint=(
        "https://api.example.com"
    ),
    auth_config={
        "bearer_token": token,
    },
    timeout_seconds=60,
    retry_config=RetryConfigs(
        max_retries=3,
        backoff_factor=2,
    ),
)
```

REST clients support:
- Automatic retry with exponential backoff
- Bearer token authentication
- Tool discovery via REST endpoints (if service supports it)
- Direct tool invocation via HTTP

---

## 4. Direct (Python Import) Client

```python
config = InteropServiceConfigs(
    service_name=(
        "Internal Library"
    ),
    transport=TransportTypes.DIRECT,
    endpoint=(
        "mypackage.tools"
        ".MyToolClass"
    ),
    discovery_enabled=False,
)
```

Use DIRECT transport for tools that are Python packages in the same environment.
No network calls, no serialization overhead.

---

## 5. Configuration from Environment

Following OB conventions, environment variables are read **once** at the entry point:

```python
# In runner (entry point only):
import os


service_endpoint = os.environ[
    "DOCUMENT_SEARCH_MCP_ENDPOINT"
]
auth_token = os.environ.get(
    "DOCUMENT_SEARCH_AUTH_TOKEN",
)

config = (
    create_document_search_interop_config(
        endpoint=service_endpoint,
        auth_token=auth_token,
    )
)
```

**Rules:**
- Environment variables read **once** at the entry point (runner)
- Values stored in configuration objects, not passed as function args between modules
- No `os.environ` access in tools, configurations, or orchestration modules
- All endpoints must be absolute URLs or valid stdio commands by the time they enter config

---

## 6. MCP Tool Factory (Dynamic Tool Generation)

When MCP tools are discovered, `MCPToolFactories` generates BaseTool subclasses at runtime:

```python
from ol_ai_services.agent_dev_kit.interop.mcp_tool_factories import (
    MCPToolFactories,
)

# Automatic — happens inside
# MCPInteropClients.discover_tools()
#
# You rarely call this directly;
# use discover_tools() instead.
```

**What it does:**
1. Reads MCP tool definition (name, description, JSON Schema)
2. Converts JSON Schema to Pydantic `input_schema` and `output_schema`
3. Generates async `_run()` method bound to the client callback
4. Creates a BaseTool subclass at runtime via `type()` and `create_model()`

The generated tools conform to the same BaseTool contract as hand-written tools
and can be registered with `ToolService` identically.

---

## 7. Naming Conventions

| Artefact | Convention | Example |
|----------|-----------|---------|
| Config factory function | `create_[service]_interop_config()` | `create_document_search_interop_config()` |
| Config module file | `[service]_interop_configs.py` | `document_search_interop_configs.py` |
| Service name (display) | Title Case, human-readable | `"Document Search Service"` |
| Tool prefix | lowercase, short | `"docsearch"` |
| Environment variable (endpoint) | `{SERVICE}_MCP_ENDPOINT` | `DOCUMENT_SEARCH_MCP_ENDPOINT` |
| Environment variable (auth) | `{SERVICE}_AUTH_TOKEN` | `DOCUMENT_SEARCH_AUTH_TOKEN` |

---

## 8. Implementing a New MCP Server

When the architect's design calls for a new MCP server (not just a client):

### Python (using FastMCP or mcp package)

```python
# [service]_mcp/server.py
from mcp.server import Server
from mcp.types import Tool

server = Server(
    name="service-mcp",
)


@server.tool()
async def search_documents(
    *,
    query: str,
    max_results: int = 10,
) -> str:
    """Search documents by
    semantic query.

    Use when the user asks about
    existing documentation.
    Returns max 10 results.
    """
    # Implementation
    results = (
        await __execute_search(
            query=query,
            max_results=max_results,
        )
    )
    return results
```

### TypeScript (using @modelcontextprotocol/sdk)

```typescript
import { McpServer } from
  "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({
  name: "service-mcp-server",
  version: "1.0.0",
});

server.tool(
  "search_documents",
  {
    query: z.string(),
    max_results: z.number()
      .default(10),
  },
  async ({ query, max_results }) => {
    // Implementation
  },
);
```

### MCP Server Rules

1. **Tool naming**: `snake_case`, action-oriented verbs
2. **Tool descriptions**: Same quality rules as BaseTool descriptions
3. **Pagination**: Implement with `has_more`, `next_offset`/`next_cursor`, `total_count`
4. **Annotations**: Provide `readOnlyHint`, `destructiveHint`, `idempotentHint`
5. **Error format**: Structured JSON with code, message, details
6. **Transport**: stdio for local, SSE for remote
