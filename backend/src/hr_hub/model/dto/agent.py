"""Agent request and response envelopes for POST /agent/chat."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class ChatTurn(BaseModel):
    """A single turn in a conversation history.

    Attributes:
        role (Literal["user", "assistant"]): Speaker of the turn.
        content (str): Text content of the turn.
    """

    model_config = ConfigDict(from_attributes=True)

    role: Literal["user", "assistant"]
    content: str


class AgentChatRequest(BaseModel):
    """Inbound request body for ``POST /agent/chat``.

    Attributes:
        message (str): The user's natural-language message.
        history (list[ChatTurn]): Prior turns in the session, oldest first.
            Excludes the current message.
    """

    model_config = ConfigDict(from_attributes=True)

    message: str
    history: list[ChatTurn] = []


class AgentChatResponse(BaseModel):
    """Response envelope returned by ``POST /agent/chat``.

    Attributes:
        answer (str): Natural-language response from the agent.
        sql_query (str | None): Last SQL SELECT executed by the query agent
            (populated on the ``db_query`` route only; not displayed by the frontend).
        blocked (bool): ``True`` when the prompt guard rejected the message.
    """

    model_config = ConfigDict(from_attributes=True)

    answer: str
    sql_query: str | None = None
    blocked: bool = False
