"""API for people-team ticket management."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from hr_hub.api import LOGGER
from hr_hub.db import get_session
from hr_hub.model.dto import NewTicketRequest, UpdateTicketRequest, TicketDTO
from hr_hub.service.ticketing import classify_ticket, create_ticket, delete_ticket, list_tickets, update_ticket


ticketing_router: APIRouter = APIRouter(prefix="/ticketing", tags=["Ticketing"])


@ticketing_router.get("", response_model=list[TicketDTO])
async def get_tickets(
    session: Session = Depends(get_session),
) -> list[TicketDTO]:
    """List all people-team tickets, newest first.

    Args:
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info("List tickets request")
    return list_tickets(session)


@ticketing_router.post("", response_model=TicketDTO, status_code=201)
async def post_ticket(
    request: NewTicketRequest,
    session: Session = Depends(get_session),
) -> TicketDTO:
    """Submit a new people-team ticket.

    Args:
        request (NewTicketRequest): Ticket payload from the frontend.
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Create ticket request [ {request.request_id} -> {request.title!r} ]")
    ticket = await create_ticket(request, session)

    if ticket is None:
        raise HTTPException(status_code=500, detail="Failed to create ticket.")

    return ticket


@ticketing_router.patch("/{request_id}", response_model=TicketDTO)
async def patch_ticket(
    request_id: str,
    request: UpdateTicketRequest,
    session: Session = Depends(get_session),
) -> TicketDTO:
    """Partially update a ticket's subject and/or text.

    Args:
        request_id (str): Primary key of the ticket (path parameter).
        request (UpdateTicketRequest): Fields to update.
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Update ticket request [ request_id={request_id} ]")
    ticket = update_ticket(request_id, request, session)

    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket {request_id!r} not found.")

    return ticket


@ticketing_router.post("/{request_id}/classify", response_model=TicketDTO)
async def run_classification(
    request_id: str,
    session: Session = Depends(get_session),
) -> TicketDTO:
    """Run (or re-run) AI classification on an existing ticket.

    Args:
        request_id (str): Primary key of the ticket (path parameter).
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Classify ticket request [ request_id={request_id} ]")
    ticket = await classify_ticket(request_id, session)

    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket {request_id!r} not found.")

    return ticket


@ticketing_router.delete("/{request_id}", status_code=204)
async def remove_ticket(
    request_id: str,
    session: Session = Depends(get_session),
) -> None:
    """Hard-delete a ticket by ID.

    Args:
        request_id (str): Primary key of the ticket (path parameter).
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Delete ticket request [ request_id={request_id} ]")
    deleted = delete_ticket(request_id, session)

    if not deleted:
        raise HTTPException(status_code=404, detail=f"Ticket {request_id!r} not found.")
