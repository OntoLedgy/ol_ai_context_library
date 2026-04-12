# Skill Manifest Guide

How to create SkillDefinition YAML manifests for packaging agents as reusable skills
in ol_ai_services.

---

## 1. Manifest Structure

```yaml
apiVersion: ol.ai/v1
kind: Skill
metadata:
    name: [skill-name]
    version: "1.0"
    category: [prompt_category]
    description: >
        Brief description of what this skill does and when to use it.
        Include trigger conditions for auto-invocation.
spec:
    model:
        default: "claude-sonnet-4-6"
        allowed:
            - "claude-sonnet-4-6"
            - "claude-opus-4-6"
    input_schema:
        type: object
        properties:
            query:
                type: string
                description: "The user's request"
        required:
            - query
    output_schema:
        type: object
        properties:
            result:
                type: string
                description: "The skill's output"
    tools:
        - name: [tool_name]
          description: "What this tool does"
          source: PACKAGE
          implementation_class: "module.path.ToolClass"
        # For INTEROP tools:
        # - name: [tool_name]
        #   source: INTEROP
        #   service: "service_name"
    prompts:
        system: prompts/system_prompt.md
        task: prompts/task_template.md
        references:
            - references/domain_knowledge.md
            - references/examples.md
    output_template: |
        ## Result
        {{ result }}
    execution:
        timeout_seconds: 120
        max_llm_calls: 10
        max_tool_calls: 20
        memory:
            engine_type: "vector"
            recall_enabled: true
            max_recall_results: 5
            max_recall_tokens: 500
```

---

## 2. File Layout

```
skills/
+-- [skill-name]/
    +-- skill.yaml              # SkillDefinition manifest
    +-- prompts/
    |   +-- system_prompt.md    # Agent identity + constraints
    |   +-- task_template.md    # Task prompt with {{ variables }}
    +-- references/             # Domain knowledge loaded as context
        +-- [topic].md
        +-- ...
```

---

## 3. Prompt Files

### System Prompt

```markdown
# [Skill Name]

You are a [role description].

## Capabilities
- [capability 1]
- [capability 2]

## Constraints
- [constraint 1]
- [constraint 2]

## Output Format
[Expected output structure]
```

### Task Template (Jinja2)

```markdown
## Task

{{ query }}

{% if context %}
## Context

{{ context }}
{% endif %}

## Instructions

1. [step 1]
2. [step 2]
3. [step 3]
```

---

## 4. Progressive Disclosure

Apply three-level progressive disclosure:

| Level | Content | Token Budget | Loading |
|-------|---------|-------------|---------|
| **L1** | Manifest metadata (name, description) | ~100 tokens | Always in context |
| **L2** | System prompt + task template body | <500 lines | On trigger match |
| **L3** | Reference documents | Unlimited | On demand during execution |

### Description Optimization

The manifest `description` is the primary trigger for auto-invocation by the
SkillRegistry. It must be specific enough to trigger correctly:

```yaml
# BAD — too vague, will undertrigger
description: "Helps with documents"

# GOOD — specific triggers and scope
description: >
    Searches, summarizes, and answers questions about project documentation.
    Use when: user asks about existing docs, needs a doc summary, wants to
    find information across multiple documents. Supports PDF, Markdown, and
    HTML sources.
```

### Description Checklist

- [ ] States what the skill does (actions)
- [ ] States when to use it (trigger conditions)
- [ ] States what it supports (scope/formats)
- [ ] Does NOT trigger on unrelated requests

---

## 5. Skill Registration

Skills are discovered by `SkillRegistry` from the skills directory:

```python
# Automatic discovery:
# Place skill.yaml in the skills directory.
# SkillRegistry.discover_skills() finds it.

# Manual invocation:
result = (
    await skill_execution_service
    .invoke_skill(
        skill_name="skill-name",
        input_data={
            "query": "user request",
        },
        workspace_id=workspace_id,
    )
)
```

### Skill Execution Pipeline

1. **Validate** input against `input_schema` (jsonschema)
2. **Select model** (default or override, checked against allowed list)
3. **Load prompts** (system + task), render Jinja2 templates
4. **Assemble messages** (system message with references + user message)
5. **Resolve tools** (PACKAGE via import, INTEROP via client connect + discover)
6. **Execute** transient agent with timeout via AgentExecutionRuntime
7. **Render output** template, validate against `output_schema`
8. **Return result** with metrics (duration, LLM calls, tool calls)

---

## 6. Evaluation

Design 10+ evaluation queries to verify the skill triggers correctly and
produces quality output:

```yaml
evaluations:
    # Should-trigger cases (verify recall)
    - query: "[realistic user request that should invoke this skill]"
      expected: "[what the output should contain]"
      should_trigger: true

    - query: "[another valid request, different phrasing]"
      expected: "[expected output]"
      should_trigger: true

    # Should-NOT-trigger cases (verify precision)
    - query: "[request that looks similar but is out of scope]"
      should_trigger: false

    - query: "[completely unrelated request]"
      should_trigger: false
```

### Evaluation Design Rules

- Mix of should-trigger (60%) and should-not-trigger (40%)
- Should-trigger cases use varied phrasing (not just rewording the description)
- Should-not-trigger cases include near-misses (similar domain, different task)
- Expected outputs are specific enough to grade programmatically

---

## 7. Manifest Naming Conventions

| Artefact | Convention | Example |
|----------|-----------|---------|
| Skill name | lowercase, hyphens, max 64 chars | `document-search` |
| Manifest file | `skill.yaml` | `skill.yaml` |
| System prompt file | `system_prompt.md` | `prompts/system_prompt.md` |
| Task template file | `task_template.md` | `prompts/task_template.md` |
| Reference files | `[topic].md` | `references/search_syntax.md` |
| Category | lowercase, domain-aligned | `"analysis"`, `"engineering"`, `"research"` |

---

## 8. Manifest Validation Checklist

Before registering:

- [ ] `metadata.name` is unique across the skill registry
- [ ] `metadata.description` is specific with clear trigger conditions
- [ ] `spec.input_schema` covers all required parameters
- [ ] `spec.output_schema` matches what the skill actually produces
- [ ] `spec.tools` lists all tools the skill needs (source type correct)
- [ ] `spec.prompts.system` file exists and is well-structured
- [ ] `spec.prompts.task` file exists with correct Jinja2 variables
- [ ] `spec.execution.timeout_seconds` is realistic for the task
- [ ] `spec.execution.max_llm_calls` prevents runaway execution
- [ ] Evaluation queries written (10+ cases, mixed trigger/no-trigger)
- [ ] All referenced files exist at their declared paths
