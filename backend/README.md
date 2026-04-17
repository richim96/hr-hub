# HR Hub Backend

FastAPI backend for the HR Hub platform. Handles employee onboarding, IT task management, ticketing, and an AI agent for ad-hoc HR queries.

## Stack

| Layer | Technology |
|-------|-----------|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| AI agent | [PydanticAI](https://ai.pydantic.dev/) + Groq |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) 2 |
| Database | SQLite (via `mock-cloud/db/hr_hub.db`) |
| Migrations | [Alembic](https://alembic.sqlalchemy.org/) |
| Dependency mgmt | [uv](https://docs.astral.sh/uv/) |

## Setup

```bash
uv sync
```

Copy `.env.example` to `.env` and fill in the values (see [Environment variables](#environment-variables)).

## Commands

```bash
# Development
uv run fastapi dev src/hr_hub/main.py       # dev server with auto-reload on :8000

# Production
uv run fastapi run src/hr_hub/main.py       # production server on :8000

# Testing & quality
uv run pytest                               # all tests
uv run pytest tests/path/to/test.py::name  # single test
uv run ruff check .                         # lint
uv run mypy src/                            # type check

# Database migrations
uv run alembic revision --autogenerate -m "description"  # generate migration from ORM changes
uv run alembic upgrade head                              # apply pending migrations
```

API docs (Swagger UI) available at `http://127.0.0.1:8000/docs` when the server is running.

## Environment variables

| Variable | Description |
|----------|-------------|
| `SQL_DB_HOST` | SQLAlchemy database URL (e.g. `sqlite:///./mock-cloud/db/hr_hub.db`) |
| `GROQ_API_KEY` | Groq API key for the PydanticAI agent |
| `OPENAI_API_KEY` | OpenAI API key (optional, for embedding / auxiliary calls) |
| `SOTA_PATH` | Path to the attrition prediction model |
| `ALLOWED_ORIGINS` | Comma-separated CORS origins (default: `http://localhost:5173,http://localhost:3000`) |

## Architecture

All routes are prefixed with `/hr-hub/api/v0.1`.

```
HTTP request
  └─ api/          routers — log, delegate, return APIResponse
       └─ service/ business logic — ORM writes, agent calls, action tracking
            ├─ model/orm.py    SQLAlchemy schema (Employee, EmployeeInfo, ITTask)
            ├─ model/dto/      Pydantic request/response schemas
            ├─ agent/          PydanticAI hr_agent (read-only DB tools)
            └─ db/             engine, session lifecycle, Alembic wiring
```

`APIResponse` is the single outbound type for every endpoint. It carries `request_id`, `status`, a list of `actions` (one per integration step), and an optional `llm_result`.

## Migration workflow

When ORM models change:

```bash
# 1. Generate a migration from the diff between ORM and current DB schema
uv run alembic revision --autogenerate -m "add salary column"

# 2. Review the generated file in alembic/versions/
# 3. Apply it
uv run alembic upgrade head
```

The database URL is read from `SQL_DB_HOST`. In Docker it is overridden via the env var so Alembic and the app use the same path.
