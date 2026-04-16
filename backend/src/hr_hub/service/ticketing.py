"""Ticketing service."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from hr_hub.model import Ticket
from hr_hub.model.dto import APIResponseDTO, NewTicketRequest, UpdateTicketRequest
from hr_hub.model.dto.ticket import TicketDTO
from hr_hub.service import LOGGER


def create_ticket(request: NewTicketRequest, session: Session) -> TicketDTO | None:
    """Persist a new people-team ticket and return the created record.

    Args:
        request (NewTicketRequest): Inbound ticket request from the frontend.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        TicketDTO: The newly created ticket, or None if the insert failed.
    """
    action = APIResponseDTO.Action(
        action="create_ticket",
        success=True,
        details=f"Ticket '{request.title}' submitted by {request.submitted_by}.",
    )

    row = Ticket(
        request_id=request.request_id,
        request_type=request.request_type,
        status="Pending",
        submitted_by=str(request.submitted_by),
        title=request.title,
        text=request.text,
        actions=[action.model_dump()],
        llm_result=None,
        created_at=datetime.now(timezone.utc),
    )

    try:
        session.add(row)
        session.flush()
        LOGGER.info(f"Ticket created [ {request.request_id} -> {request.title!r} ]")
        return TicketDTO.model_validate(row)
    except Exception as e:
        LOGGER.error(f"Could not persist ticket {request.request_id}: {e}")
        return None


def delete_ticket(request_id: str, session: Session) -> bool:
    """Hard-delete a ticket from the database.

    Args:
        request_id (str): Primary key of the ticket to delete.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        bool: True if the ticket was deleted, False if not found or deletion failed.
    """
    try:
        row: Ticket | None = session.get(Ticket, request_id)
    except Exception as e:
        LOGGER.error(f"DB error fetching ticket {request_id} for deletion: {e}")
        return False

    if row is None:
        return False

    try:
        session.delete(row)
        session.flush()
        LOGGER.info(f"Ticket deleted [ {request_id} ]")
        return True
    except Exception as e:
        LOGGER.error(f"Could not delete ticket {request_id}: {e}")
        return False


def update_ticket(request_id: str, request: UpdateTicketRequest, session: Session) -> TicketDTO | None:
    """Partially update a ticket's subject and/or text.

    Only fields explicitly set in the request (non-None) are written to the DB.

    Args:
        request_id (str): Primary key of the ticket to update.
        request (UpdateTicketRequest): Fields to update; only non-None values are written.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        TicketDTO: The updated ticket, or None if not found or update failed.
    """
    try:
        row: Ticket | None = session.get(Ticket, request_id)
    except Exception as e:
        LOGGER.error(f"DB error fetching ticket {request_id} for update: {e}")
        return None

    if row is None:
        return None

    if request.title is not None:
        row.title = request.title
    if request.text is not None:
        row.text = request.text

    try:
        session.flush()
        LOGGER.info(f"Ticket updated [ {request_id} ]")
        return TicketDTO.model_validate(row)
    except Exception as e:
        LOGGER.error(f"Could not update ticket {request_id}: {e}")
        return None


def list_tickets(session: Session) -> list[TicketDTO]:
    """Return all stored tickets ordered by creation time descending.

    Args:
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        list[TicketDTO]: All persisted tickets, newest first.
    """
    try:
        rows: list[Ticket] = (
            session.query(Ticket)
            .order_by(Ticket.created_at.desc())
            .all()
        )
        return [TicketDTO.model_validate(row) for row in rows]
    except Exception as e:
        LOGGER.error(f"DB error fetching tickets: {e}")
        return []
