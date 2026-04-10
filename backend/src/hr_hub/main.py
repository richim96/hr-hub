"""Entry point for the HR Hub server."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import find_dotenv, load_dotenv

from hr_hub import LOGGER
from hr_hub.api.employee import employee_router
from hr_hub.db import build_sessionmaker, create_db_engine

load_dotenv(find_dotenv())


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_engine = create_db_engine()
    app.state.db_sessionmaker = build_sessionmaker(app.state.db_engine)

    LOGGER.info("✅ App context initialized")

    yield

    LOGGER.info("👋 Clearing app context...")
    app.state.db_engine.dispose()
    LOGGER.info("👋 DB engine disposed")


app: FastAPI = FastAPI(
    title="HR Hub",
    description="HR Hub Server",
    lifespan=lifespan,
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],    # Frontend port
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router, prefix="/hr-hub/api/v0.1")
