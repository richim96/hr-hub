"""SQLAlchemy engine construction."""

import os
from sqlalchemy import Engine, create_engine
from hr_hub.db import LOGGER


def create_db_engine() -> Engine:
    """Build the SQLAlchemy engine from the `SQL_DB_HOST` environment variable.

    Called once at application startup from the FastAPI `lifespan` context
    manager. The resulting engine is attached to `app.state` and shared across
    requests.

    Raises:
        RuntimeError: If `SQL_DB_HOST` is not set in the environment.

    Returns:
        Engine: A configured SQLAlchemy engine.
    """
    db_url: str = os.getenv("SQL_DB_HOST", "")
    if not db_url:
        raise RuntimeError("SQL_DB_HOST is not set — cannot build DB engine.")

    # SQLite needs `check_same_thread=False` when used from a threaded server
    # like FastAPI/uvicorn, where a session may touch the connection from a
    # different thread than the one that created it.
    connect_args: dict = {}
    if db_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    engine: Engine = create_engine(db_url, connect_args=connect_args, future=True)
    LOGGER.info(f"✅ DB engine created for {engine.url.render_as_string(hide_password=True)}")

    return engine
