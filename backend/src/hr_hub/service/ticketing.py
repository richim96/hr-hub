"""Ticketing service."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from hr_hub.model import Ticket
from hr_hub.model.dto import APIResponseDTO, NewTicketRequest, UpdateTicketRequest
from hr_hub.service import LOGGER


def create_ticket(request: NewTicketRequest, session: Session) -> APIResponseDTO:
    """Persist a new people-team ticket and return a completed APIResponse.

    The ticket is stored in the database immediately.  LLM processing
    (``llm_result``) is not performed yet — that will be wired in when the
    HR agent is integrated.

    Args:
        request (TicketRequestDTO): Inbound ticket request from the frontend.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        APIResponseDTO: Completed response with a ``create_ticket`` action.
    """
    action = APIResponseDTO.Action(
        action="create_ticket",
        success=True,
        details=f"Ticket '{request.subject}' submitted by {request.submitted_by}.",
    )

    row = Ticket(
        request_id=request.request_id,
        request_type=request.request_type,
        status="pending",
        submitted_by=str(request.submitted_by),
        subject=request.subject,
        text=request.text,
        actions=[action.model_dump()],
        llm_result=None,
        created_at=datetime.now(timezone.utc),
    )

    try:
        session.add(row)
        session.flush()
        LOGGER.info(f"Ticket created [ {request.request_id} -> {request.subject!r} ]")
    except Exception as e:
        LOGGER.error(f"Could not persist ticket {request.request_id}: {e}")
        return APIResponseDTO(
            request_id=request.request_id,
            request_type="people_ticket",
            status="failed",
            actions=[
                APIResponseDTO.Action(
                    action="create_ticket",
                    success=False,
                    details=f"Could not save ticket: {e}",
                )
            ],
        )

    return APIResponseDTO(
        request_id=request.request_id,
        request_type="people_ticket",
        status="pending",
        actions=[action],
    )


def delete_ticket(request_id: str, session: Session) -> APIResponseDTO:
    """Hard-delete a ticket from the database.

    Args:
        request_id (str): Primary key of the ticket to delete.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        APIResponseDTO: Status and action describing what happened.
    """
    from uuid import uuid4
    response_id = str(uuid4())

    row = session.get(Ticket, request_id)
    if row is None:
        return APIResponseDTO(
            request_id=response_id,
            request_type="people_ticket",
            status="failed",
            actions=[APIResponseDTO.Action(
                action="delete_ticket",
                success=False,
                details=f"Ticket {request_id!r} not found.",
            )],
        )

    try:
        session.delete(row)
        session.flush()
        LOGGER.info(f"Ticket deleted [ {request_id} ]")
    except Exception as e:
        LOGGER.error(f"Could not delete ticket {request_id}: {e}")
        return APIResponseDTO(
            request_id=response_id,
            request_type="people_ticket",
            status="failed",
            actions=[APIResponseDTO.Action(
                action="delete_ticket",
                success=False,
                details=f"Could not delete ticket: {e}",
            )],
        )

    return APIResponseDTO(
        request_id=response_id,
        request_type="people_ticket",
        status="completed",
        actions=[APIResponseDTO.Action(
            action="delete_ticket",
            success=True,
            details=f"Ticket {request_id} deleted.",
        )],
    )


def update_ticket(request_id: str, request: UpdateTicketRequest, session: Session) -> APIResponseDTO:
    """Partially update a ticket's subject and/or text.

    Args:
        request_id (str): Primary key of the ticket to update.
        request (UpdateTicketRequest): Fields to update; only non-None values are written.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        APIResponseDTO: Status and action describing what happened.
    """
    row = session.get(Ticket, request_id)
    if row is None:
        return APIResponseDTO(
            request_id=request_id,
            request_type="people_ticket",
            status="failed",
            actions=[APIResponseDTO.Action(
                action="update_ticket",
                success=False,
                details=f"Ticket {request_id!r} not found.",
            )],
        )

    if request.subject is not None:
        row.subject = request.subject
    if request.text is not None:
        row.text = request.text

    try:
        session.flush()
        LOGGER.info(f"Ticket updated [ {request_id} ]")
    except Exception as e:
        LOGGER.error(f"Could not update ticket {request_id}: {e}")
        return APIResponseDTO(
            request_id=request_id,
            request_type="people_ticket",
            status="failed",
            actions=[APIResponseDTO.Action(
                action="update_ticket",
                success=False,
                details=f"Could not update ticket: {e}",
            )],
        )

    return APIResponseDTO(
        request_id=request_id,
        request_type="people_ticket",
        status=row.status,
        actions=[APIResponseDTO.Action(
            action="update_ticket",
            success=True,
            details=f"Ticket {request_id} updated.",
        )],
        subject=row.subject,
        text=row.text,
        submitted_by=row.submitted_by,
    )


def list_tickets(session: Session) -> list[APIResponseDTO]:
    """Return all stored tickets as APIResponse objects, newest first.

    Args:
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        list[APIResponseDTO]: All persisted tickets ordered by creation time descending.
    """
    try:
        rows: list[Ticket] = (
            session.query(Ticket)
            .order_by(Ticket.created_at.desc())
            .all()
        )
    except Exception as e:
        LOGGER.error(f"DB error fetching tickets: {e}")
        return []

    result: list[APIResponseDTO] = []
    for row in rows:
        actions = [APIResponseDTO.Action(**a) for a in (row.actions or [])]
        llm = APIResponseDTO.LLMResult(**row.llm_result) if row.llm_result else None
        result.append(
            APIResponseDTO(
                request_id=row.request_id,
                request_type="people_ticket",
                status=row.status,
                actions=actions,
                llm_result=llm,
                subject=row.subject,
                text=row.text,
                submitted_by=row.submitted_by,
            )
        )
    return result
