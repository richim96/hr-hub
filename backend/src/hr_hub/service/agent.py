"""Agent orchestration service."""

from sqlalchemy.orm import Session

from hr_hub.agent.prompt_guard import is_prompt_safe
from hr_hub.agent.chat import QueryDeps, chat_agent
from hr_hub.model.dto import AgentChatResponse
from hr_hub.service import LOGGER


async def run_agent(message: str, session: Session) -> AgentChatResponse:
    """Routes a user message through the prompt guard and the chat agent
    and return a response.

    Args:
        message (str): Raw user input from the frontend.
        session (Session): Active SQLAlchemy session (read-only; used by the
            query agent only).

    Returns:
        AgentChatResponse: Structured response with route, natural-language
            answer, and optional ``sql_query``.
    """
    safe: bool = await is_prompt_safe(message)

    if not safe:
        LOGGER.warning(f"Prompt guard blocked message: {message[:120]!r}")
        return AgentChatResponse(
            answer="Your message was flagged as malicious and not processed",
            blocked=True,
        )

    deps = QueryDeps(session=session)

    try:
        query_result = await chat_agent.run(message, deps=deps)
        sql_used: str | None = deps.queries[-1] if deps.queries else None
        LOGGER.info(f"Chat agent SQL: {sql_used!r}")
        return AgentChatResponse(answer=query_result.output.answer, sql_query=sql_used)
    except Exception as exc:
        LOGGER.error(f"Query agent error: {exc}")
        return AgentChatResponse(
            answer="The query could not be completed — please rephrase your question.",
            sql_query=deps.queries[-1] if deps.queries else None,
        )
