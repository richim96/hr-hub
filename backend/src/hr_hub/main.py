"""Entry point for the HR Hub server."""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from hr_hub import LOGGER
from hr_hub.api.employee import employee_router
from hr_hub._clients import HRISClient, ITTasksClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.hris_client = HRISClient()
    app.state.it_tasks_client = ITTasksClient()

    LOGGER.info("✅ Mock clients initialized")

    yield

    LOGGER.info("👋 Shutting down clients")


app: FastAPI = FastAPI(
    title="HR Hub",
    description="HR Hub Server",
    lifespan=lifespan,
    version="0.1.0",
)
prefix: str = "/hr-hub/api/v0.1"

app.include_router(employee_router, prefix=prefix)
