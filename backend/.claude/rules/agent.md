---
description: Rules for working in src/hr_hub/agent/
---

# Agent Module Rules

The agent is built with [PydanticAI](https://ai.pydantic.dev/) and uses OpenAI as the underlying model provider.

## Agent definition

The agent lives in `agent/agent.py` and is exported via `agent/__init__.py` as `hr_agent`. Do not create additional top-level agent instances; add tools and system prompt sections to the existing `hr_agent`.

## Tools

- All tools live in `agent/`. Each file should group tools by domain (e.g., `employee_tool.py`, `ticketing_tool.py`).
- Register tools by passing them explicitly to the `tools=[...]` list in the `Agent(...)` constructor. Do not use wildcard imports to register tools.
- Tools must be plain Python functions decorated with `@hr_agent.tool` or passed as callables. They must have typed signatures — PydanticAI derives the tool schema from type annotations. They are bound to the scope of the model. Actions will be defined internally to the tools. A tool can query the database, but only query it. It cannot update or delete data, it is restricted to read-only (SELECT statements). Queries should come in text form directly from the LLM, the orm layer should use the query directly: it's an extra layer of complexity not needed for the agent's use case.

## Environment

The agent loads its API key from the environment via `python-dotenv`. The relevant key is `OPENAI_API_KEY`. Do not hardcode model names as string literals outside of `agent.py` — define a module-level constant if the model name needs to be referenced more than once.

## Logging

Use the module-level `LOGGER` from `agent/__init__.py`:
```python
from hr_hub.agent import LOGGER
```
