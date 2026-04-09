"""New hire workflow."""

from datetime import datetime, timezone
from fastapi import Request

from hr_hub.model.dto import EmployeeSchema, ResponseSchema
from backend.src.hr_hub.model.dto.response import Action
from hr_hub.model.dto import NewHireRequest
from hr_hub._clients.hris import HRISResponse


def start_onboarding(request: Request, event: NewHireRequest) -> ResponseSchema:
    """Start the new hire workflow.

    Args:
        event (NewHireEvent): The new hire event containing employee details
    """

    employee: EmployeeSchema = event.employee
    # This becomes ORM operation
    employee_record: HRISResponse = request.app.state.hris_client.create_employee(
        employee
    )
    actions: list[Action] = _create_it_tasks(employee)

    return ResponseSchema(
        event_id=event.request_id,
        event_type=event.request_type,
        status="completed" if employee_record.success else "failed",
        processed_at=datetime.now(timezone.utc),
        actions_taken=[
            Action(
                integration="hris",
                action="create_employee",
                success=employee_record.success,
                details=f"Employee {employee.email} creation {'succeeded' if employee_record.success else 'failed'} in HRIS. Response: {employee_record}",
            ),
        ] + actions,
        summary=f"Employee {employee.email} creation {'succeeded' if employee_record.success else 'failed'} in HRIS.",
    )


def update_employee_data():
    pass


def _create_it_tasks(employee: EmployeeSchema) -> list[Action]:
    """Create IT tasks for the new hire."""
    return []
