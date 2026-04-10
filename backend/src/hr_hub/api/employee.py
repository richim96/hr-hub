"""API for creating employees and updating employee data."""

from datetime import datetime, timezone
from fastapi import APIRouter, Request

from hr_hub.api import LOGGER
from hr_hub.model.dto import NewHireRequest, EmployeeChangeRequest
from hr_hub.model.dto import APIResponse
from hr_hub.service.employee import start_onboarding


employee_router: APIRouter = APIRouter(prefix="/employee", tags=["Employee Operations"])


@employee_router.post("/new-hire", response_model=APIResponse)
async def create_employee(request: Request, event: NewHireRequest) -> APIResponse:
    """Create a new employee.

    Args:
        event (NewHireEvent): The new hire event data.
    """
    LOGGER.info(
        f"Received request for new hire [ {event.request_id} -> {event.employee.email} ]. Processing onboarding."
    )
    return start_onboarding(request, event)


@employee_router.patch("/change", response_model=APIResponse)
async def update_employee(
    request: Request, event: EmployeeChangeRequest
) -> APIResponse | None:
    """Update employee details based on the provided change event.

    Args:
        event (EmployeeChangeEvent): The employee change event data.
    """
    pass
