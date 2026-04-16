"""Agent request and response envelopes for POST /agent/chat."""

from pydantic import BaseModel, ConfigDict


class AgentChatRequest(BaseModel):
    """Inbound request body for ``POST /agent/chat``.

    Attributes:
        message (str): The user's natural-language message — either a question
            about HR data or ticket text to be classified.
    """

    model_config = ConfigDict(from_attributes=True)

    message: str


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
