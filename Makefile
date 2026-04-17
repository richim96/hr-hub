DB_PATH := mock-cloud/db/hr_hub.db

.PHONY: help \
        delete-db revision migrate seed reset-db \
        backend frontend dev full-reset \
        backend-prod frontend-build frontend-prod prod \
        docker-build docker-up docker-up-build docker-down docker-reset

help:
	@echo "HR Hub — available targets:"
	@echo ""
	@echo "  Database"
	@echo "    delete-db       Delete the SQLite database file"
	@echo "    revision        Autogenerate a new migration  (MSG=\"description\")"
	@echo "    migrate         Apply pending migrations (alembic upgrade head)"
	@echo "    seed            Execute the db_seed notebook"
	@echo "    reset-db        delete-db → revision → migrate → seed (MSG=\"description\")"
	@echo ""
	@echo "  Development"
	@echo "    backend         FastAPI dev server with auto-reload (:8000)"
	@echo "    frontend        SvelteKit dev server with HMR       (:5173)"
	@echo "    dev             Start both concurrently (Ctrl-C stops both)"
	@echo "    full-reset      reset-db → dev"
	@echo ""
	@echo "  Production (local)"
	@echo "    backend-prod    FastAPI production server            (:8000)"
	@echo "    frontend-build  Build SvelteKit for production"
	@echo "    frontend-prod   Build then start the Node server     (:3000)"
	@echo "    prod            Build frontend, then start both servers"
	@echo ""
	@echo "  Docker"
	@echo "    docker-build    Build all images"
	@echo "    docker-up       Start containers (build if needed)"
	@echo "    docker-up-build Rebuild images and start containers"
	@echo "    docker-down     Stop and remove containers"
	@echo "    docker-reset    docker-down (with volumes) → docker-up-build"

# ── Database ──────────────────────────────────────────────────────────────────

delete-db:
	rm -f $(DB_PATH)
	@echo "Deleted $(DB_PATH)"

revision:
	@test -n "$(MSG)" || (echo "Error: MSG is required. Usage: make revision MSG=\"description\"" && exit 1)
	cd backend && uv run alembic upgrade head # safety net to ensure db is running head before new revision
	cd backend && uv run alembic revision --autogenerate -m "$(MSG)"

migrate:
	cd backend && uv run alembic upgrade head

# Requires jupyter in the notebooks venv.
# If missing: cd notebooks && uv add jupyter && uv sync
seed:
	cd notebooks && uv run jupyter nbconvert --to notebook --execute db_seed.ipynb --output db_seed.ipynb

reset-db: delete-db revision migrate seed

# ── Development ───────────────────────────────────────────────────────────────

backend:
	cd backend && uv run fastapi dev src/hr_hub/main.py

frontend:
	cd frontend && yarn dev

dev:
	@trap 'kill 0' SIGINT; \
	  (cd backend && uv run fastapi dev src/hr_hub/main.py) & \
	  (until curl -sf http://127.0.0.1:8000/docs >/dev/null 2>&1; do sleep 0.5; done \
	    && cd frontend && yarn dev) & \
	  wait

full-reset: reset-db dev

# ── Production (local) ────────────────────────────────────────────────────────

backend-prod:
	cd backend && uv run fastapi run src/hr_hub/main.py

frontend-build:
	cd frontend && yarn build

frontend-prod: frontend-build
	cd frontend && node build

prod:
	@echo "Building frontend..."
	cd frontend && yarn build
	@echo "Starting production servers (Ctrl-C to stop both)..."
	@trap 'kill 0' SIGINT; \
	  (cd backend && uv run fastapi run src/hr_hub/main.py) & \
	  (until curl -sf http://127.0.0.1:8000/docs >/dev/null 2>&1; do sleep 0.5; done \
	  (cd frontend && node build) & \
	  wait

# ── Docker ────────────────────────────────────────────────────────────────────

docker-build:
	docker compose build

docker-up:
	docker compose up

docker-up-build:
	docker compose up --build

docker-down:
	docker compose down

# Removes named volumes (wipes the DB) then rebuilds from scratch
docker-reset:
	docker compose down -v
	docker compose up --build
