---
description: Rules for working in src/hr_hub/api/
---

# API Module Rules

FastAPI routers handle HTTP routing only. Business logic belongs in `service/`.

## Router setup

- Each domain gets its own router file and `APIRouter` instance with a `prefix` and `tags`.
- Routers are registered in `main.py` under the global prefix `/hr-hub/api/v0.1`.
- Import routers into `main.py` and call `app.include_router(...)`.

## Handler responsibilities

Handlers should:
1. Log the incoming request with enough context to trace it (request ID, relevant identifiers).
2. Delegate immediately to a `service/` function.
3. Return the result as an `APIResponse`.

Handlers should not contain business logic, ORM queries, or direct database access.

## Request/response types

- All handlers use types from `model/dto/`. Request bodies are Pydantic models; responses are `APIResponse`.
- Declare `response_model=APIResponse` on every route decorator.
- Access app-level state (db session, clients) via `request.app.state`, not via module-level globals.

## Logging

Each router file gets its own logger via `api/__init__.py`:
```python
from hr_hub.api import LOGGER
```
