"""New hire workflow."""

from sqlalchemy.orm import Session

from hr_hub.model import Employee, EmployeeInfo
from hr_hub.model.dto import (
    APIResponse,
    EmployeeDTO,
    EmployeeEquipmentDTO,
    EmployeeInfoDTO,
    NewHireRequest,
)
from hr_hub.service import LOGGER


def start_onboarding(request: NewHireRequest, session: Session) -> APIResponse:
    """Start the new hire workflow.

    Persists the new employee (core record + employment info) to the database.
    The caller owns the transaction — this function only `flush`es to surface
    integrity errors early; commit happens in the `get_session` dependency.

    Args:
        request (NewHireRequest): The new hire request containing employee details.
        session (Session): Active SQLAlchemy session bound to the app engine.

    Returns:
        APIResponse: Status and per-step actions describing what happened.
    """
    LOGGER.info(
        f"Starting onboarding for [ {request.request_id} -> {request.employee.email} ]"
    )

    actions: list[APIResponse.Action] = []
    create_action = _create_employee(
        session, request.employee, request.equipment, request.info
    )
    actions.append(create_action)

    if create_action.success:
        actions += _create_it_tasks(request.employee)

    return APIResponse(
        request_id=request.request_id,
        request_type=request.request_type,
        status="completed" if create_action.success else "failed",
        actions=actions,
    )


def update_employee_data():
    pass


def _create_employee(
    session: Session,
    employee: EmployeeDTO,
    equipment: EmployeeEquipmentDTO,
    info: EmployeeInfoDTO,
) -> APIResponse.Action:
    """Insert an `Employee` and its `EmployeeInfo` row in the same flush.

    Args:
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.
        employee (EmployeeDTO): Core employee identity data (name, email, manager).
        equipment (EmployeeEquipmentDTO): Equipment assigned to the employee at hire.
        info (EmployeeInfoDTO): Employment profile data (department, salary tier, attrition signals).

    Returns:
        Action: Summary of the action taken.
    """
    employee_row: Employee = Employee(
        **employee.model_dump(),
        **equipment.model_dump()
    )
    info_row: EmployeeInfo = EmployeeInfo(
        employee_id=employee.employee_id,
        **info.model_dump(),
    )

    try:
        session.add(employee_row)
        session.add(info_row)
        session.flush()
    except Exception as e:
        session.rollback()
        LOGGER.error(
            f"Could not create employee {employee.email}: {e}"
        )
        return APIResponse.Action(
            action="create_employee",
            success=False,
            details=f"Could not create employee {employee.email}: {e}",
        )

    return APIResponse.Action(
        action="create_employee",
        success=True,
        details=f"Employee {employee.email} created successfully.",
    )


def _create_it_tasks(employee: EmployeeDTO) -> list[APIResponse.Action]:
    """Create IT tasks for the new hire."""
    return []
