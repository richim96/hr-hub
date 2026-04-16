"""Pydantic response schema for people-team tickets."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class TicketDTO(BaseModel):
    """Full ticket record — used for all ticket read responses.

    Attributes:
        request_id (str): Unique identifier for the ticket.
        request_type (str): Always ``"people_ticket"``.
        status (Literal["Pending", "Canceled", "Completed"]): Current processing status.
        submitted_by (str): Email of the person who submitted the ticket.
        title (str): Title of the ticket.
        text (str): Full description of the ticket issue.
        actions (list[dict[str, Any]]): JSON-serialized workflow actions recorded during processing.
        llm_result (dict[str, Any] | None): LLM analysis result, populated once the agent runs.
        created_at (datetime): UTC timestamp when the ticket was created.
    """

    model_config = ConfigDict(from_attributes=True)

    request_id: str
    request_type: str
    status: Literal["Pending", "Canceled", "Completed"]
    submitted_by: str
    title: str
    text: str
    actions: list[dict[str, Any]]
    llm_result: dict[str, Any] | None = None
    created_at: datetime
