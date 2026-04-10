"""API for creating employees and updating employee data."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from hr_hub.api import LOGGER
from hr_hub.db import get_session
from hr_hub.model.dto import NewHireRequest, EmployeeChangeRequest
from hr_hub.model.dto import APIResponse
from hr_hub.service.employee import start_onboarding


employee_router: APIRouter = APIRouter(prefix="/employee", tags=["Employee Operations"])


@employee_router.post("/new-hire", response_model=APIResponse)
async def create_employee(
    request: NewHireRequest,
    session: Session = Depends(get_session),
) -> APIResponse:
    """Create a new employee.

    Args:
        request (NewHireEvent): The new hire request data.
        session (Session): The SQLAlchemy session connecting to the database.
    """
    LOGGER.info(
        f"Received request for new hire [ {request.request_id} -> {request.employee.email} ]."
    )
    return start_onboarding(request, session)


@employee_router.patch("/change", response_model=APIResponse)
async def update_employee(
    request: EmployeeChangeRequest,
    session: Session = Depends(get_session)
) -> APIResponse | None:
    """Update employee details based on the provided change request.

    Args:
        event (EmployeeChangeEvent): The employee change request data.
        session (Session): The SQLAlchemy session connecting to the database.
    """
    pass
