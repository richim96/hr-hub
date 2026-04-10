"""Session lifecycle and FastAPI dependency."""

from typing import Iterator

from fastapi import Request
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from hr_hub.db import LOGGER


def build_sessionmaker(engine: Engine) -> sessionmaker[Session]:
    """Create a `sessionmaker` bound to the given engine.

    Called once at startup in the FastAPI `lifespan` and attached to
    `app.state.db_sessionmaker`. Requests then acquire a session via the
    `get_session` dependency.

    Args:
        engine (Engine): The SQLAlchemy engine built by `create_db_engine`.

    Returns:
        A configured `sessionmaker` factory.
    """

    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_session(request: Request) -> Iterator[Session]:
    """FastAPI dependency that yields a database session.

    The session is committed when the handler returns successfully, rolled
    back on any exception, and always closed. Service functions receive the
    session via dependency injection and must not call `session.commit()`.

    Usage::

        @router.post("/foo")
        def handler(session: Session = Depends(get_session)):
            ...

    Args:
        request (Request): The incoming FastAPI request (used to reach `app.state`).

    Yields:
        Session: An active SQLAlchemy session bound to the app's engine.
    """
    session_factory: sessionmaker[Session] = request.app.state.db_sessionmaker
    session: Session = session_factory()

    try:
        yield session
        session.commit()
    except Exception as e:
        LOGGER.exception(f"DB session rollback due to unhandled exception:\n\t{e}")
        session.rollback()
        raise
    finally:
        session.close()
