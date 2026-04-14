# HR Hub

AI-augmented HR workflow automation. HR Hub lets an HR team manage employees, IT tasks, and support tickets through a web dashboard backed by an LLM agent that classifies requests and triggers downstream actions.

## What it does

- **Employee management** — onboard new hires, view and edit employee records, track attrition risk scores
- **IT task management** — create and monitor IT tasks linked to employees
- **Ticketing** — submit support tickets processed by an LLM agent that classifies topics, assesses confidence, and logs actions taken
- **HR chat assistant** — conversational interface to the HR agent for ad-hoc queries

## Project layout

| Directory | What it is |
|-----------|-----------|
| `backend/` | FastAPI server — API routes, business logic, PydanticAI agent, SQLAlchemy ORM |
| `frontend/` | SvelteKit dashboard — employee, task, and ticket views + chat widget |
| `notebooks/` | Data work: attrition model training, DB seed notebook |
| `mock-cloud/` | Local stand-in for cloud infrastructure: `db/` (SQLite file), `storage/` (static data files) |

## Quick start

**Prerequisites:** [uv](https://docs.astral.sh/uv/), [Yarn](https://yarnpkg.com/), [Jupyter](https://jupyter.org/) (for seeding), [Docker](https://www.docker.com/) (optional)

**Development**
```bash
make reset-db   # delete DB → migrate → seed
make dev        # backend (:8000) + frontend (:5173) concurrently
```

**Production (local)**
```bash
make prod       # builds frontend, then starts both prod servers
```

**Docker**
```bash
# Copy .env.example to .env and fill in secrets (OPENAI_API_KEY etc.)
make docker-up-build   # build images and start containers
# backend → :8000  |  frontend → :3000
```

See each subdirectory's `README.md` for detailed setup instructions.

## Makefile targets

| Target | What it does |
|--------|-------------|
| `make reset-db` | Delete DB → run revision → run migrations → seed |
| `make dev` | Dev servers for backend (:8000) and frontend (:5173) |
| `make full-reset` | `reset-db` then `dev` |
| `make prod` | Build frontend, start both in production mode |
| `make backend-prod` | FastAPI production server only |
| `make frontend-prod` | Build + start SvelteKit Node server (:3000) |
| `make docker-up-build` | Build Docker images and start all containers |
| `make docker-down` | Stop and remove containers |
| `make docker-reset` | Full wipe (volumes included) and rebuild |
