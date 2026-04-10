# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency management.

```bash
uv sync                                                        # install deps
uv run fastapi dev src/hr_hub/main.py                         # dev server (auto-reload)
uv run fastapi run src/hr_hub/main.py                         # prod server
uv run pytest                                                  # all tests
uv run pytest tests/path/to/test_file.py::test_function_name  # single test
uv run ruff check .                                            # lint
uv run mypy src/                                               # type check
uv run alembic revision --autogenerate -m "description"        # new migration
uv run alembic upgrade head                                    # apply migrations
```

API docs: `http://127.0.0.1:8000/docs`

## Architecture

HR Hub is an AI-augmented HR workflow automation backend built with FastAPI + PydanticAI.

**Request flow:** HTTP → `api/` routers → `service/` layer → database (SQLAlchemy ORM)

All routes are prefixed with `/hr-hub/api/v0.1`. App-level state (db session, clients) lives on `app.state`, set during `lifespan` in `main.py`.

## Module rules

Detailed rules for each module live in `.claude/rules/`:

| Module | Rules file | Responsibility |
|--------|-----------|----------------|
| `api/` | [rules/api.md](rules/api.md) | HTTP routing only — log, delegate to service, return `APIResponse` |
| `service/` | [rules/service.md](rules/service.md) | All business logic; orchestrates DB writes, agent calls, action tracking |
| `model/orm.py` | [rules/model.md](rules/model.md) | SQLAlchemy ORM — authoritative DB schema (`Employee`, `EmployeeInfo`, `ITTask`) |
| `model/dto/` | [rules/dto.md](rules/dto.md) | Pydantic schemas; `APIResponse` is the only outbound type |
| `agent/` | [rules/agent.md](rules/agent.md) | PydanticAI agent (`hr_agent`); tools are read-only, call raw SQL |
| `db/` | [rules/db.md](rules/db.md) | Engine, session lifecycle, Alembic wiring |

## Environment variables

See `.env_example`:
- `SQL_DB_HOST` — SQLAlchemy database URL
- `OPENAI_API_KEY` — PydanticAI agent
- `VECTOR_DB_PATH` — ChromaDB (RAG/vector search)
- `SOTA_PATH` — attrition prediction model
- `TAVILY_API_KEY` — web search tool for the agent

## Current scaffolding

`_CLIENTS/` (`HRISClient`, `ITTasksClient`, `TicketingClient`) are in-memory mocks with a 10% random failure rate. They are temporary and will be replaced with direct ORM/DB operations.
