"""New hire workflow."""

from datetime import datetime, timezone
from fastapi import Request

from hr_hub.model.dto import EmployeeDTO, APIResponse
from hr_hub.model.dto import NewHireRequest


def start_onboarding(request: Request, event: NewHireRequest) -> APIResponse:
    """Start the new hire workflow.

    Args:
        event (NewHireRequest): The new hire event containing employee details
    """

    employee: EmployeeDTO = event.employee
    # This becomes ORM operation with database
    employee_record = request.app.state.hris_client.create_employee(
        employee
    )
    actions: list[APIResponse.Action] = [APIResponse.Action(
        action="create_employee",
        success=employee_record.success,
        details=f"Employee {employee.email} creation {'succeeded' if employee_record.success else 'failed'}. Response: {employee_record}",
    ), ]
    if employee_record.success:
        actions += _create_it_tasks(employee)

    return APIResponse(
        event_id=event.request_id,
        event_type=event.request_type,
        status="completed" if employee_record.success else "failed",
        actions=actions,
    )


def update_employee_data():
    pass


def _create_it_tasks(employee: EmployeeDTO) -> list[APIResponse.Action]:
    """Create IT tasks for the new hire."""
    return []
