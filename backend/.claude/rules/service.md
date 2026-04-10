---
description: Rules for working in src/hr_hub/service/
---

# Service Module Rules

The service layer contains all business logic. It sits between the API routers and the database, and is the only place that orchestrates multi-step workflows.

## Responsibilities

Each service function should:
1. Accept typed inputs (DTOs or primitives) and a database session (injected).
2. Perform ORM reads/writes via the session.
3. Coordinate any agent calls if LLM processing is needed.
4. Return an `APIResponse` populated with the full list of `APIResponse.Action` objects that describe what happened (including failures).

## File layout

| File | Workflow |
|------|---------|
| `employee.py` | New hire onboarding (`start_onboarding`), employee data changes (`update_employee_data`) |
| `ticketing.py` | People-team ticket creation and routing |
| `prediction.py` | Attrition risk scoring (loads/caches the SOTA model at startup) |

## Action tracking

Every discrete step (db write, agent call, external side-effect) should produce an `APIResponse.Action`:
```python
APIResponse.Action(action="create_employee", success=True, details="...")
```
Collect actions in a list and pass them to `APIResponse.actions`.

## Error handling

Do not raise exceptions from service functions for expected failure cases (e.g., employee not found, duplicate record). Return an `APIResponse` with `status="failed"` and a descriptive `Action` with `success=False`. Raise only for unrecoverable programmer errors. However, you should handle exceptions! The error message should be logged in "details" and the status set to failed. There should be code explicitly handling exceptions for results depending on external services (db work, llm response etc.).

## Database access

Service functions receive a SQLAlchemy `Session` as a parameter. Do not import or construct sessions inside service functions. Do not call `session.commit()` inside a service function — commit is the caller's responsibility (typically the FastAPI dependency).
