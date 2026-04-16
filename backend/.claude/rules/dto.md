---
description: Rules for working in src/hr_hub/model/dto/
---

# DTO Module Rules

`model/dto/` holds all Pydantic schemas used for API request/response serialization. DTOs are the contract between the HTTP layer and the service layer.

## Conventions

- All DTOs inherit from `pydantic.BaseModel`.
- Every DTO must include `model_config = ConfigDict(from_attributes=True)` to support direct construction from SQLAlchemy ORM instances via `Model.model_validate(orm_obj)`.
- Use `Field(alias=...)` / `Field(validation_alias=..., serialization_alias=...)` when the JSON key differs from the Python attribute name.
- Optional fields use `field: Type | None = None`. Do not use `Optional[Type]`.

## File layout

Each domain file owns **all** its Pydantic types — read DTOs, request envelopes, and response envelopes together.

| File | Contents |
|------|---------|
| `employee.py` | `EmployeeDTO`, `EmployeeEquipmentDTO`, `EmployeeInfoDTO`, `FullEmployeeDTO`, `NewHireRequest`, `UpdateEmployeeRequest` |
| `ticket.py` | `TicketDTO`, `NewTicketRequest`, `UpdateTicketRequest` |
| `it_task.py` | `ITTaskDTO`, `NewITTaskRequest`, `UpdateITTaskRequest` |
| `prediction.py` | `AttritionFeaturesDTO`, `ScoreAllAttritionRequest` |
| `agent.py` | `AgentChatRequest`, `AgentChatResponse` |
| `response.py` | `APIResponse` only — the shared synchronous response wrapper |

## APIResponse structure

`APIResponse` is the outbound type for the employee, ticket, and prediction endpoints. It contains:
- `request_id: str` — identifier of the processed request
- `request_type: Literal[...]` — one of `"new_hire"`, `"employee_change"`, `"people_ticket"`, `"prediction"`
- `status: Literal[...]` — one of `"completed"`, `"pending"`, `"failed"`
- `actions: list[APIResponse.Action]` — each integration step as a nested `Action` object
- `llm_result: APIResponse.LLMResult | None` — populated when the agent is invoked

`Action` and `LLMResult` are defined as nested classes inside `APIResponse`. Reference them as `APIResponse.Action` and `APIResponse.LLMResult`, not as standalone imports.

The agent endpoint (`/agent/chat`) uses `AgentChatResponse` from `agent.py` instead of `APIResponse`.

## Exports

All public DTOs are re-exported from `model/dto/__init__.py`. Import DTOs from there, not from individual files:
```python
from hr_hub.model.dto import NewHireRequest, APIResponse, AgentChatRequest
```
