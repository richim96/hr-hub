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

| File | Purpose |
|------|---------|
| `employee.py` | `EmployeeDTO`, `EmployeeEquipmentDTO`, `EmployeeInfoDTO` |
| `change.py` | `ChangeDTO` (old/new value pair for update events) |
| `requests.py` | Inbound request envelopes: `NewHireRequest`, `EmployeeChangeRequest`, `TicketRequest` |
| `response.py` | `APIResponse` — the single outbound type for all endpoints |

## APIResponse structure

`APIResponse` is the only response type returned from the API. It contains:
- `actions_taken: list[APIResponse.Action]` — each integration step as a nested `Action` object
- `llm_result: APIResponse.LLMResult | None` — populated when the agent is invoked
- `summary: str` — human-readable description of what happened

`Action` and `LLMResult` are defined as nested classes inside `APIResponse`. Reference them as `APIResponse.Action` and `APIResponse.LLMResult`, not as standalone imports.

## Exports

All public DTOs are re-exported from `model/dto/__init__.py`. Import DTOs from there, not from individual files:
```python
from hr_hub.model.dto import NewHireRequest, APIResponse
```
