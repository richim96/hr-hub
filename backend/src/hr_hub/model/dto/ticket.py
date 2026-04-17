"""People-team ticket schemas — read DTO and request envelopes."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, EmailStr

from hr_hub.model.dto.response import Status


class TicketDTO(BaseModel):
    """Full ticket record — used for all ticket read responses.

    Attributes:
        request_id (str): Unique identifier for the ticket.
        request_type (str): Always ``"people_ticket"``.
        status (Status): Current processing status.
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
    status: Status
    submitted_by: str
    title: str
    text: str
    actions: list[dict[str, Any]]
    llm_result: dict[str, Any] | None = None
    created_at: datetime


class NewTicketRequest(BaseModel):
    """Inbound payload for submitting a new people-team ticket.

    Attributes:
        request_id (str): Unique identifier for the request (e.g., ``"evt_003"``).
        request_type (Literal["people_ticket"]): Must be ``"people_ticket"``.
        submitted_by (EmailStr): Email of the submitting employee.
        title (str): Short title of the issue.
        text (str): Full description of the ticket issue.
    """

    request_id: str
    request_type: Literal["people_ticket"]
    submitted_by: EmailStr
    title: str
    text: str


class UpdateTicketRequest(BaseModel):
    """Partial-update payload for an existing people-team ticket.

    All fields are optional — only non-None values are written to the database.

    Attributes:
        title (str | None): Updated ticket title.
        text (str | None): Updated ticket description.
    """

    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    text: str | None = None
