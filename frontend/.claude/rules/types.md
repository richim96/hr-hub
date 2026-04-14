---
description: Rules for working in src/lib/types/
---

# Types Module Rules

`lib/types/index.ts` holds all TypeScript interfaces that mirror the backend Pydantic DTOs. These are the single source of truth for payload shapes across the frontend.

## Mapping from backend DTOs

| Backend DTO | Frontend interface |
|-------------|-------------------|
| `EmployeeDTO` | `Employee` |
| `EmployeeEquipmentDTO` | `EmployeeEquipment` |
| `EmployeeInfoDTO` | `EmployeeInfo` |
| `ChangeDTO` | `ChangeField` |
| `NewHireRequest` | `NewHireRequest` |
| `EmployeeChangeRequest` | `EmployeeChangeRequest` |
| `TicketRequest` | `TicketRequest` |
| `APIResponse` | `APIResponse` |
| `APIResponse.Action` | `APIAction` |
| `APIResponse.LLMResult` | `LLMResult` |

## Conventions

- All field names match the backend JSON keys exactly (including `type` alias for `request_type`).
- Optional fields use `field?: Type` — do not use `field: Type | null` for fields that are absent in the payload.
- Enum literals match backend `Literal[...]` exactly (case-sensitive).
- Never import backend Python files — derive types from the DTO source files and sample payloads in `_INTERNAL_DOCS/`.
- Do not add frontend-only state (loading, selected, etc.) to DTO interfaces. Use separate wrapper types in the stores.
- `ITTask` is a separate interface modelling the `it_task` ORM table — it is not in the backend DTOs directly but is needed for the Tasks dashboard.
