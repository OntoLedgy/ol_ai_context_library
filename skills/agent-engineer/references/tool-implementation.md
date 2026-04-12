# Tool Implementation Guide

How to implement tools for registration into ol_ai_services using the BaseTool contract.

---

## 1. BaseTool Contract

Every tool inherits from `ol_ai_services.agent_dev_kit.tools.base_tool.BaseTool`:

```python
from abc import ABC, abstractmethod
from typing import Type
from pydantic import BaseModel


class BaseTool(ABC):
    name: str
    description: str
    input_schema: Type[BaseModel]
    output_schema: Type[BaseModel]

    @abstractmethod
    async def _run(
        self,
        *,
        input_data: BaseModel,
    ) -> BaseModel:
        ...

    async def run(
        self,
        **kwargs,
    ) -> BaseModel:
        # Validates input against
        # input_schema, calls _run(),
        # handles errors
        ...
```

---

## 2. Implementation Template

### Step 1: Define Input Schema

```python
# [verb]_[subject]_tool_inputs.py
from pydantic import (
    BaseModel,
    Field,
)


class VerbSubjectToolInputs(
    BaseModel,
):
    """Input schema for
    [tool description]."""

    param_one: str = Field(
        description=(
            "What this parameter "
            "controls"
        ),
    )
    param_two: int = Field(
        default=10,
        description=(
            "Optional parameter "
            "with default"
        ),
    )
```

### Step 2: Define Output Schema

```python
# [verb]_[subject]_tool_outputs.py
from pydantic import (
    BaseModel,
    Field,
)


class VerbSubjectToolOutputs(
    BaseModel,
):
    """Output schema for
    [tool description]."""

    result: str = Field(
        description=(
            "The primary result"
        ),
    )
    success: bool = Field(
        default=True,
        description=(
            "Whether the operation "
            "succeeded"
        ),
    )
    error_message: str = Field(
        default="",
        description=(
            "Error details if "
            "success is false"
        ),
    )
```

### Step 3: Implement Tool

```python
# [verb]_[subject]_tools.py
from ol_ai_services.agent_dev_kit.tools.base_tool import (
    BaseTool,
)
from .verb_subject_tool_inputs import (
    VerbSubjectToolInputs,
)
from .verb_subject_tool_outputs import (
    VerbSubjectToolOutputs,
)


class VerbSubjectTools(
    BaseTool,
):
    name: str = "verb_subject"
    description: str = (
        "Clear description of what "
        "this tool does and when "
        "to use it."
    )
    input_schema = (
        VerbSubjectToolInputs
    )
    output_schema = (
        VerbSubjectToolOutputs
    )

    async def _run(
        self,
        *,
        input_data: (
            VerbSubjectToolInputs
        ),
    ) -> VerbSubjectToolOutputs:
        try:
            result = (
                await self
                .__do_the_work(
                    param_one=(
                        input_data
                        .param_one
                    ),
                    param_two=(
                        input_data
                        .param_two
                    ),
                )
            )
        except SpecificError as error:
            return (
                VerbSubjectToolOutputs(
                    result="",
                    success=False,
                    error_message=(
                        str(error)
                    ),
                )
            )
        return VerbSubjectToolOutputs(
            result=result,
            success=True,
        )

    async def __do_the_work(
        self,
        *,
        param_one: str,
        param_two: int,
    ) -> str:
        # Private implementation
        ...
```

### Step 4: Register Tool

```python
from ol_ai_services.agent_dev_kit.tools.tool_service import (
    ToolService,
)


# In the runner (entry point):
tool = VerbSubjectTools()
await tool_service.register_tool(
    tool=tool,
    workspace_id=workspace_id,
)
```

---

## 3. Naming Conventions (OB/BORO)

| Artefact | Convention | Example |
|----------|-----------|---------|
| Tool name (string) | `snake_case`, verb + subject | `"search_documents"` |
| Tool class | Plural CamelCase, `VerbSubjectTools` | `SearchDocumentTools` |
| Input schema class | Plural CamelCase, `VerbSubjectToolInputs` | `SearchDocumentToolInputs` |
| Output schema class | Plural CamelCase, `VerbSubjectToolOutputs` | `SearchDocumentToolOutputs` |
| Module file (tool) | `verb_subject_tools.py` | `search_document_tools.py` |
| Module file (input) | `verb_subject_tool_inputs.py` | `search_document_tool_inputs.py` |
| Module file (output) | `verb_subject_tool_outputs.py` | `search_document_tool_outputs.py` |
| Private methods | `__double_underscore` | `__build_query()` |

---

## 4. Tool Design Principles

### Description Quality

Tool descriptions are critical — they are the agent's only API documentation:

- **Lead with what it does**: "Searches documents in the knowledge base by semantic query"
- **Include when to use**: "Use when the user asks about existing documentation"
- **Mention key parameters**: "Requires a query string; optionally filters by date range"
- **Note limitations**: "Returns max 10 results; does not search attachments"

### Schema Design

- **Required vs optional**: Mark truly required params; use defaults for optional
- **Field descriptions**: Every field has a description (the agent reads these)
- **Constrained types**: Use `Field(ge=1, le=100)` for bounded values
- **Enum fields**: Use `Literal["option_a", "option_b"]` for fixed choices
- **No bare `dict` or `Any`**: Use typed models or `dict[str, str]` at minimum

### Error Handling

Tools return errors in the output schema — they do **not** raise exceptions from `_run()`.
The agent needs structured error information to decide what to do next.

Every output schema must include:
- `success: bool` — whether the operation succeeded
- `error_message: str` — details if `success` is `False`

### Idempotency

If a tool is idempotent, document it. If not, the agent needs to know to avoid
duplicate calls. Include this in the tool description.

---

## 5. Testing Tools

### Unit Test Template

```python
# test_verb_subject_tools.py
import pytest

from [module].verb_subject_tools import (
    VerbSubjectTools,
)


@pytest.fixture
def tool() -> VerbSubjectTools:
    return VerbSubjectTools()


@pytest.mark.asyncio
async def test_run_with_valid_input(
    tool: VerbSubjectTools,
) -> None:
    result = await tool.run(
        param_one="test_value",
    )
    assert result.success is True
    assert result.result != ""


@pytest.mark.asyncio
async def test_run_returns_error(
    tool: VerbSubjectTools,
) -> None:
    # Test with input that triggers
    # error path
    result = await tool.run(
        param_one="invalid",
    )
    assert result.success is False
    assert result.error_message != ""


@pytest.mark.asyncio
async def test_schema_validation(
    tool: VerbSubjectTools,
) -> None:
    # Verify input schema rejects
    # invalid types
    with pytest.raises(
        ValidationError,
    ):
        await tool.run(
            param_one=123,  # wrong type
        )
```

### Test Checklist

- [ ] Happy path returns expected output
- [ ] Error path returns structured error (not exception)
- [ ] Input schema rejects invalid types
- [ ] Required parameters are enforced
- [ ] Optional parameters use defaults
- [ ] Output schema is complete (all fields populated)
- [ ] Tool is stateless (multiple calls produce independent results)
