"""API for people-team ticket management."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from hr_hub.api import LOGGER
from hr_hub.db import get_session
from hr_hub.model.dto import APIResponseDTO, NewTicketRequest, UpdateTicketRequest
from hr_hub.service.ticketing import create_ticket, delete_ticket, list_tickets, update_ticket


ticketing_router: APIRouter = APIRouter(prefix="/ticketing", tags=["Ticketing"])


@ticketing_router.get("", response_model=list[APIResponseDTO])
async def get_tickets(
    session: Session = Depends(get_session),
) -> list[APIResponseDTO]:
    """List all people-team tickets, newest first.

    Args:
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info("List tickets request")
    return list_tickets(session)


@ticketing_router.post("", response_model=APIResponseDTO)
async def post_ticket(
    request: NewTicketRequest,
    session: Session = Depends(get_session),
) -> APIResponseDTO:
    """Submit a new people-team ticket.

    Args:
        request (TicketRequestDTO): Ticket payload from the frontend.
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Create ticket request [ {request.request_id} -> {request.subject!r} ]")
    return create_ticket(request, session)


@ticketing_router.patch("/{request_id}", response_model=APIResponseDTO)
async def patch_ticket(
    request_id: str,
    request: UpdateTicketRequest,
    session: Session = Depends(get_session),
) -> APIResponseDTO:
    """Partially update a ticket's subject and/or text.

    Args:
        request_id (str): Primary key of the ticket (path parameter).
        request (UpdateTicketRequest): Fields to update.
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Update ticket request [ request_id={request_id} ]")
    return update_ticket(request_id, request, session)


@ticketing_router.delete("/{request_id}", response_model=APIResponseDTO)
async def remove_ticket(
    request_id: str,
    session: Session = Depends(get_session),
) -> APIResponseDTO:
    """Hard-delete a ticket by ID.

    Args:
        request_id (str): Primary key of the ticket (path parameter).
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Delete ticket request [ request_id={request_id} ]")
    return delete_ticket(request_id, session)
