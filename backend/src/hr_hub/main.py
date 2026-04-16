"""Entry point for the HR Hub server."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import find_dotenv, load_dotenv

from hr_hub import LOGGER
from hr_hub.api.employee import employee_router
from hr_hub.api.prediction import prediction_router
from hr_hub.api.it_task import it_task_router
from hr_hub.api.ticketing import ticketing_router
from hr_hub.db import build_sessionmaker, create_db_engine
from hr_hub.service.prediction import load_model

load_dotenv(find_dotenv())

_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
ALLOWED_ORIGINS: list[str] = [o.strip() for o in _raw.split(",") if o.strip()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_engine = create_db_engine()
    app.state.db_sessionmaker = build_sessionmaker(app.state.db_engine)
    app.state.attrition_model = load_model()

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
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router, prefix="/hr-hub/api/v0.1")
app.include_router(prediction_router, prefix="/hr-hub/api/v0.1")
app.include_router(it_task_router, prefix="/hr-hub/api/v0.1")
app.include_router(ticketing_router, prefix="/hr-hub/api/v0.1")
