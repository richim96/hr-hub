#!/bin/sh
set -e

echo "Running database migrations..."
uv run alembic upgrade head

echo "Starting HR Hub backend..."
exec uv run fastapi run src/hr_hub/main.py --host 0.0.0.0 --port 8000
