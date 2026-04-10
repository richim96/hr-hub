---
description: Rules for working in src/hr_hub/db/
---

# DB Module Rules

The `db/` module owns everything related to the database connection, session lifecycle, and query helpers. It is the only place in the codebase that should hold SQLAlchemy `Engine` and `Session` objects.

## Session management

- Create the `Engine` once at startup and attach it to `app.state` in the `lifespan` context manager in `main.py`.
- Expose sessions as a FastAPI dependency (e.g., `get_session`) that yields a `Session` and commits/rolls back on exit. Handlers and service functions receive sessions via dependency injection, never by importing a global session.
- Use `sessionmaker` or `Session` from `sqlalchemy.orm`. Do not use the legacy `scoped_session` pattern.

## Alembic

- ORM models are defined in `model/orm.py`. `alembic/env.py` imports `Base.metadata` from there — do not duplicate model definitions.
- Always generate migrations with `--autogenerate` and review the generated script before applying.
- Migration scripts go in `alembic/versions/`. Do not hand-edit the revision chain (`down_revision`, `branch_labels`).
- The database URL comes from the `SQL_DB_HOST` environment variable. It must never be hardcoded.

## Logging

Use the module-level logger from `db/__init__.py`:
```python
from hr_hub.db import LOGGER
```
