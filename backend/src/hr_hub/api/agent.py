"""API router for the Groq-powered HR agent chat endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from hr_hub.api import LOGGER
from hr_hub.db import get_session
from hr_hub.model.dto import AgentChatRequest, AgentChatResponse
from hr_hub.service.agent import run_agent


agent_router: APIRouter = APIRouter(prefix="/agent", tags=["Agent"])


@agent_router.post("/chat", response_model=AgentChatResponse)
async def chat(
    request: AgentChatRequest,
    session: Session = Depends(get_session),
) -> AgentChatResponse:
    """Submit a message to the HR chat agent. The message passes through a
    prompt-safety guard before reaching the agent.

    Args:
        request (AgentChatRequest): User message payload.
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Agent chat: {request.message[:60]!r}")
    return await run_agent(request.message, session)
