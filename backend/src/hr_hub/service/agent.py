"""Agent orchestration service."""

from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart, UserPromptPart
from sqlalchemy.orm import Session

from hr_hub.agent.prompt_guard import is_prompt_safe
from hr_hub.agent.chat import QueryDeps, chat_agent
from hr_hub.model.dto import AgentChatResponse
from hr_hub.model.dto.agent import ChatTurn
from hr_hub.service import LOGGER


def _to_model_messages(history: list[ChatTurn]) -> list[ModelMessage]:
    """Convert frontend chat history to PydanticAI message objects.

    Args:
        history (list[ChatTurn]): Prior turns, oldest first.

    Returns:
        list[ModelMessage]: PydanticAI-compatible message history.
    """
    messages: list[ModelMessage] = []
    for turn in history:
        if turn.role == "user":
            messages.append(ModelRequest(parts=[UserPromptPart(content=turn.content)]))
        else:
            messages.append(ModelResponse(parts=[TextPart(content=turn.content)]))
    return messages


async def run_agent(
    message: str, session: Session, history: list[ChatTurn] | None = None
) -> AgentChatResponse:
    """Routes a user message through the prompt guard and the chat agent
    and return a response.

    Args:
        message (str): Raw user input from the frontend.
        session (Session): Active SQLAlchemy session (read-only; used by the
            query agent only).
        history (list[ChatTurn] | None): Prior turns in the session, oldest first.

    Returns:
        AgentChatResponse: Structured response with route, natural-language
            answer, and optional ``sql_query``.
    """
    safe: bool = await is_prompt_safe(message)

    if not safe:
        LOGGER.warning(f"Prompt guard blocked message: {message[:120]!r}")
        return AgentChatResponse(
            answer="You cannot fool a Goomba 🍄",
            blocked=True,
        )

    deps = QueryDeps(session=session)
    message_history = _to_model_messages(history or [])

    try:
        query_result = await chat_agent.run(
            message, deps=deps, message_history=message_history
        )
        sql_used: str | None = deps.queries[-1] if deps.queries else None
        LOGGER.info(f"Chat agent SQL: {sql_used!r}")
        return AgentChatResponse(answer=query_result.output, sql_query=sql_used)
    except Exception as e:
        LOGGER.error(f"Query agent error: {e}")
        return AgentChatResponse(
            answer="Could not find an answer — please rephrase your question.",
            sql_query=deps.queries[-1] if deps.queries else None,
        )
