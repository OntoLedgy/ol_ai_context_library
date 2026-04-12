# Agent Implementation Guide

Detailed patterns for agent configuration, orchestration graph building,
and runner wiring using ol_ai_services.

---

## 1. Agent Configuration Patterns

### Simple Agent (Single Model, Tools Only)

```python
from ol_ai_services.agent_dev_kit.objects.agent_configuration import (
    AgentConfiguration,
)
from ol_ai_services.agent_dev_kit.objects.agent_configuration import (
    StorageStrategy,
)
from ..common_knowledge.model_config_enums import (
    ModelConfigEnums,
)
from ..common_knowledge.prompt_constants import (
    SIMPLE_AGENT_SYSTEM_PROMPT,
)


def create_simple_agent_configuration(
    *,
    workspace_id: str,
    tool_ids: list[str],
) -> AgentConfiguration:
    return AgentConfiguration(
        workspace_id=workspace_id,
        name="simple_agent",
        description=(
            "A simple tool-using agent"
        ),
        model_name=(
            ModelConfigEnums
            .DEFAULT_MODEL
            .value
        ),
        system_prompt=(
            SIMPLE_AGENT_SYSTEM_PROMPT
        ),
        tool_ids=tool_ids,
        backend_storage=(
            StorageStrategy.EPHEMERAL
        ),
    )
```

### Memory-Augmented Agent

```python
from ol_ai_services.agent_dev_kit.objects.memory_configuration import (
    MemoryConfiguration,
)


def create_memory_agent_configuration(
    *,
    workspace_id: str,
    tool_ids: list[str],
) -> AgentConfiguration:
    return AgentConfiguration(
        workspace_id=workspace_id,
        name="memory_agent",
        description=(
            "Agent with recall "
            "and persistence"
        ),
        model_name=(
            ModelConfigEnums
            .DEFAULT_MODEL
            .value
        ),
        system_prompt=(
            MEMORY_AGENT_SYSTEM_PROMPT
        ),
        tool_ids=tool_ids,
        backend_storage=(
            StorageStrategy.PERSISTENT
        ),
        memory_config=MemoryConfiguration(
            engine_type="vector",
            recall_enabled=True,
            max_recall_results=5,
            max_recall_tokens=500,
        ),
    )
```

### Agent with Human-in-the-Loop

```python
def create_supervised_agent_configuration(
    *,
    workspace_id: str,
    tool_ids: list[str],
) -> AgentConfiguration:
    return AgentConfiguration(
        workspace_id=workspace_id,
        name="supervised_agent",
        description=(
            "Agent requiring approval "
            "for destructive actions"
        ),
        model_name=(
            ModelConfigEnums
            .DEFAULT_MODEL
            .value
        ),
        system_prompt=(
            SUPERVISED_AGENT_SYSTEM_PROMPT
        ),
        tool_ids=tool_ids,
        interrupt_config={
            "require_approval": [
                "delete_record",
                "send_email",
                "modify_config",
            ],
        },
    )
```

---

## 2. Orchestration Graph Building

### Linear Pipeline

```python
from ol_ai_services.agent_dev_kit.objects.orchestration_graph import (
    OrchestrationGraph,
    AgentNode,
    AgentEdge,
)


def create_pipeline_graph(
    *,
    workspace_id: str,
    collect_agent_id: str,
    transform_agent_id: str,
    output_agent_id: str,
) -> OrchestrationGraph:
    return OrchestrationGraph(
        workspace_id=workspace_id,
        name="data_pipeline",
        description=(
            "Linear data processing "
            "pipeline"
        ),
        nodes=[
            AgentNode(
                node_id="collect",
                agent_id=collect_agent_id,
                input_mapping={
                    "source": "input.source",
                },
            ),
            AgentNode(
                node_id="transform",
                agent_id=transform_agent_id,
                input_mapping={
                    "data": "collect.output",
                },
            ),
            AgentNode(
                node_id="output",
                agent_id=output_agent_id,
                input_mapping={
                    "data": (
                        "transform.output"
                    ),
                },
            ),
        ],
        edges=[
            AgentEdge(
                from_node_id="collect",
                to_node_id="transform",
            ),
            AgentEdge(
                from_node_id="transform",
                to_node_id="output",
            ),
        ],
        entry_node_id="collect",
    )
```

### Conditional Router

```python
def create_router_graph(
    *,
    workspace_id: str,
    router_agent_id: str,
    research_agent_id: str,
    coding_agent_id: str,
    data_agent_id: str,
) -> OrchestrationGraph:
    return OrchestrationGraph(
        workspace_id=workspace_id,
        name="task_router",
        description=(
            "Routes tasks to "
            "specialist agents"
        ),
        nodes=[
            AgentNode(
                node_id="router",
                agent_id=(
                    router_agent_id
                ),
            ),
            AgentNode(
                node_id="research",
                agent_id=(
                    research_agent_id
                ),
            ),
            AgentNode(
                node_id="coding",
                agent_id=(
                    coding_agent_id
                ),
            ),
            AgentNode(
                node_id="data",
                agent_id=(
                    data_agent_id
                ),
            ),
        ],
        edges=[
            AgentEdge(
                from_node_id="router",
                to_node_id="research",
                conditional_route={
                    "on_status": (
                        "research"
                    ),
                },
            ),
            AgentEdge(
                from_node_id="router",
                to_node_id="coding",
                conditional_route={
                    "on_status": (
                        "coding"
                    ),
                },
            ),
            AgentEdge(
                from_node_id="router",
                to_node_id="data",
                conditional_route={
                    "on_status": "data",
                },
            ),
        ],
        entry_node_id="router",
    )
```

### Peer Review (Parallel + Merge)

```python
def create_peer_review_graph(
    *,
    workspace_id: str,
    reviewer_a_id: str,
    reviewer_b_id: str,
    synthesizer_id: str,
) -> OrchestrationGraph:
    return OrchestrationGraph(
        workspace_id=workspace_id,
        name="peer_review",
        description=(
            "Parallel review with "
            "synthesis"
        ),
        nodes=[
            AgentNode(
                node_id="reviewer_a",
                agent_id=reviewer_a_id,
            ),
            AgentNode(
                node_id="reviewer_b",
                agent_id=reviewer_b_id,
            ),
            AgentNode(
                node_id="synthesizer",
                agent_id=synthesizer_id,
                input_mapping={
                    "review_a": (
                        "reviewer_a.output"
                    ),
                    "review_b": (
                        "reviewer_b.output"
                    ),
                },
            ),
        ],
        edges=[
            AgentEdge(
                from_node_id="reviewer_a",
                to_node_id="synthesizer",
            ),
            AgentEdge(
                from_node_id="reviewer_b",
                to_node_id="synthesizer",
            ),
        ],
        entry_node_id="reviewer_a",
    )
```

---

## 3. Runner Wiring

### Full Runner Template

```python
# [agent_name]_runners.py
import os

from ol_ai_services.agent_dev_kit.facade import (
    AgentDevelopmentKitFacade,
)
from ..common_knowledge.tool_name_enums import (
    ToolNameEnums,
)
from ..tools.verb_subject_tools import (
    VerbSubjectTools,
)
from ..interop.service_interop_configs import (
    create_service_interop_config,
)
from ..configurations.agent_configurations import (
    create_agent_configuration,
)


async def run_agent(
    *,
    facade: AgentDevelopmentKitFacade,
    workspace_id: str,
    input_message: str,
    thread_id: str | None = None,
) -> dict:
    # 1. Read environment config
    #    (once, at entry point)
    service_endpoint = os.environ[
        "SERVICE_MCP_ENDPOINT"
    ]

    # 2. Register custom tools
    custom_tool = VerbSubjectTools()
    await facade.register_tool(
        tool=custom_tool,
    )

    # 3. Connect interop and
    #    discover tools
    interop_config = (
        create_service_interop_config(
            endpoint=service_endpoint,
        )
    )
    interop_tools = (
        await facade
        .discover_interop_tools(
            config=interop_config,
            workspace_id=workspace_id,
        )
    )

    # 4. Collect all tool IDs
    tool_ids = [
        ToolNameEnums
        .VERB_SUBJECT
        .value,
    ] + [
        tool.name
        for tool in interop_tools
    ]

    # 5. Create agent configuration
    agent_config = (
        create_agent_configuration(
            workspace_id=workspace_id,
            tool_ids=tool_ids,
        )
    )
    agent_id = await facade.create_agent(
        configuration=agent_config,
    )

    # 6. Execute
    execution = (
        await facade.execute_agent(
            agent_id=agent_id,
            input_data={
                "message": input_message,
            },
            thread_id=thread_id,
        )
    )

    return execution
```

### Runner Rules

1. **Environment variables read here only** — never in tools, configs, or orchestration
2. **Tool registration before agent creation** — all tools must be registered first
3. **Interop discovery before agent creation** — discover and register external tools
4. **Facade for all lifecycle ops** — do not call internal services directly
5. **Thread ID for continuity** — pass through for multi-turn conversations
6. **No business logic in runner** — runner is wiring only, like a bclearer pipeline runner

---

## 4. Testing Patterns

### Tool Unit Test

```python
import pytest

from ..tools.verb_subject_tools import (
    VerbSubjectTools,
)


@pytest.fixture
def tool() -> VerbSubjectTools:
    return VerbSubjectTools()


@pytest.mark.asyncio
async def test_happy_path(
    tool: VerbSubjectTools,
) -> None:
    result = await tool.run(
        param_one="test_value",
    )
    assert result.success is True
    assert result.result != ""


@pytest.mark.asyncio
async def test_error_handling(
    tool: VerbSubjectTools,
) -> None:
    result = await tool.run(
        param_one="",
    )
    assert result.success is False
    assert result.error_message != ""
```

### Configuration Validation Test

```python
from ..configurations.agent_configurations import (
    create_agent_configuration,
)


def test_config_is_valid() -> None:
    config = create_agent_configuration(
        workspace_id="test-ws",
        tool_ids=[
            "tool_a",
            "tool_b",
        ],
    )
    assert config.name != ""
    assert config.model_name != ""
    assert len(config.tool_ids) == 2
```

### Orchestration Graph Test

```python
from ..orchestration.agent_orchestration_graphs import (
    create_pipeline_graph,
)


def test_graph_is_valid_dag() -> None:
    graph = create_pipeline_graph(
        workspace_id="test-ws",
        collect_agent_id="a1",
        transform_agent_id="a2",
        output_agent_id="a3",
    )
    assert (
        graph.entry_node_id
        == "collect"
    )
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 2
    # Verify no cycles:
    # all to_node_ids come after
    # from_node_ids in topological order
    node_order = {
        node.node_id: i
        for i, node
        in enumerate(graph.nodes)
    }
    for edge in graph.edges:
        assert (
            node_order[
                edge.from_node_id
            ]
            < node_order[
                edge.to_node_id
            ]
        )
```

### Integration Test

```python
@pytest.mark.asyncio
async def test_agent_end_to_end() -> None:
    facade = (
        AgentDevelopmentKitFacade(...)
    )
    result = await run_agent(
        facade=facade,
        workspace_id="test-ws",
        input_message="test query",
    )
    assert (
        result["status"]
        == "COMPLETED"
    )
```
