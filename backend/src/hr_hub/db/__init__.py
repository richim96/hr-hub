"""Database submodule: engine, session lifecycle and FastAPI wiring."""

from logging import Logger

from hr_hub.logger import get_logger
from hr_hub.db.engine import create_db_engine  # noqa: E402
from hr_hub.db.session import build_sessionmaker, get_session  # noqa: E402

LOGGER: Logger = get_logger("hr_hub.db")

__all__ = ["create_db_engine", "build_sessionmaker", "get_session"]
