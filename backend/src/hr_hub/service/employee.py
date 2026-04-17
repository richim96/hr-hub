"""New hire workflow."""

from typing import Any
from uuid import uuid4

from sqlalchemy.orm import Session

from hr_hub.model import Employee, EmployeeInfo, ITTask
from hr_hub.model.dto import (
    APIResponse,
    EmployeeDTO,
    EmployeeEquipmentDTO,
    EmployeeInfoDTO,
    FullEmployeeDTO,
    NewHireRequest,
    UpdateEmployeeRequest,
)
from hr_hub.service import LOGGER
from hr_hub.service.it_task import create_onboarding_tasks
from hr_hub.service.prediction import score_employee

_EMPLOYEE_FIELDS = {"first_name", "last_name", "gender", "email", "manager_email", "laptop", "monitor", "headset"}
_INFO_FIELDS = {
    "department", "salary", "active_projects", "avg_monthly_hours",
    "years_at_company", "work_accidents", "received_promotion",
    "last_evaluation", "satisfaction_score", "attrition", "attrition_risk",
}


def start_onboarding(
    request: NewHireRequest,
    session: Session,
    attrition_model: Any | None,
) -> APIResponse:
    """Start the new hire workflow.

    Args:
        request (NewHireRequestDTO): The new hire request containing employee details.
        session (Session): Active SQLAlchemy session bound to the app engine.
        attrition_model (Any | None): Loaded sklearn Pipeline from app.state. Passed to the scoring step.

    Returns:
        APIResponseDTO: Status and per-step actions describing what happened.
    """
    LOGGER.info(f"Starting onboarding for {request.employee.email}")
    actions: list[APIResponse.Action] = []
    create_action = _create_employee(
        session, request.employee, request.equipment, request.info
    )
    actions.append(create_action)

    if create_action.success:
        actions += create_onboarding_tasks(
            employee_id=request.employee.employee_id,
            employee_email=request.employee.email,
            department=request.info.department,
            session=session,
        )
        actions.append(score_employee(request.employee.employee_id, session, attrition_model))

    return APIResponse(
        request_id=request.request_id,
        request_type=request.request_type,
        status="Completed" if create_action.success else "Canceled",
        actions=actions,
    )


def update_employee(
    employee_id: str,
    request: UpdateEmployeeRequest,
    session: Session,
    attrition_model: Any | None = None,
) -> APIResponse:
    """Apply a partial update to an employee's identity, equipment, and/or employment info.

    Args:
        employee_id (str): Primary key of the employee to update.
        request (UpdateEmployeeRequest): Partial update payload; None fields are skipped.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.
        attrition_model (Any | None): Loaded sklearn Pipeline from app.state. Passed through to scoring.

    Returns:
        APIResponseDTO: Status and per-step actions describing what happened.
    """
    request_id = str(uuid4())

    employee = session.get(Employee, employee_id)
    if employee is None:
        return APIResponse(
            request_id=request_id,
            request_type="employee_change",
            status="Canceled",
            actions=[APIResponse.Action(
                action="update_employee",
                success=False,
                details=f"Employee {employee_id!r} not found.",
            )],
        )

    info = session.get(EmployeeInfo, employee_id)

    for field, value in request.model_dump(exclude_none=True).items():
        if field in _EMPLOYEE_FIELDS:
            setattr(employee, field, value)
        elif field in _INFO_FIELDS and info is not None:
            setattr(info, field, value)

    try:
        session.flush()
    except Exception as e:
        LOGGER.error(f"Could not update employee {employee_id}: {e}")
        return APIResponse(
            request_id=request_id,
            request_type="employee_change",
            status="Canceled",
            actions=[APIResponse.Action(
                action="update_employee",
                success=False,
                details=f"Could not update employee {employee_id}: {e}",
            )],
        )

    actions: list[APIResponse.Action] = [APIResponse.Action(
        action="update_employee",
        success=True,
        details=f"Employee {employee_id} updated successfully.",
    )]
    actions.append(score_employee(employee_id, session, attrition_model))

    return APIResponse(
        request_id=request_id,
        request_type="employee_change",
        status="Completed",
        actions=actions,
    )


def delete_employee(employee_id: str, session: Session) -> APIResponse:
    """Hard-delete an employee and all related records from the database.

    Args:
        employee_id (str): Primary key of the employee to delete.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        APIResponseDTO: Status and per-step actions describing what happened.
    """
    request_id = str(uuid4())

    employee = session.get(Employee, employee_id)
    if employee is None:
        return APIResponse(
            request_id=request_id,
            request_type="employee_change",
            status="Canceled",
            actions=[APIResponse.Action(
                action="delete_employee",
                success=False,
                details=f"Employee {employee_id!r} not found.",
            )],
        )

    try:
        session.query(ITTask).filter(ITTask.employee_id == employee_id).delete()
        info = session.get(EmployeeInfo, employee_id)
        if info is not None:
            session.delete(info)
        session.delete(employee)
        session.flush()
    except Exception as e:
        LOGGER.error(f"Could not delete employee {employee_id}: {e}")
        return APIResponse(
            request_id=request_id,
            request_type="employee_change",
            status="Canceled",
            actions=[APIResponse.Action(
                action="delete_employee",
                success=False,
                details=f"Could not delete employee {employee_id}: {e}",
            )],
        )

    return APIResponse(
        request_id=request_id,
        request_type="employee_change",
        status="Completed",
        actions=[APIResponse.Action(
            action="delete_employee",
            success=True,
            details=f"Employee {employee_id} deleted successfully.",
        )],
    )


def list_employees(session: Session) -> list[FullEmployeeDTO]:
    """Return all current employees (attrition=False).

    Args:
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        list[FullEmployeeDTO]: One record per current employee with a linked EmployeeInfo row.
    """
    rows = (
        session.query(Employee, EmployeeInfo)
        .join(EmployeeInfo, Employee.employee_id == EmployeeInfo.employee_id)
        .filter(EmployeeInfo.attrition.isnot(True))
        .all()
    )

    return [_build_full_dto(emp, info) for emp, info in rows]


def get_employee(employee_id: str, session: Session) -> FullEmployeeDTO | None:
    """Fetch a single current employee by ID.

    Returns None if the employee does not exist or has attrition=True.

    Args:
        employee_id (str): Primary key of the employee to retrieve.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        FullEmployeeDTO: The employee's full profile, or None if not found.
    """
    row = (
        session.query(Employee, EmployeeInfo)
        .join(EmployeeInfo, Employee.employee_id == EmployeeInfo.employee_id)
        .filter(Employee.employee_id == employee_id)
        .first()
    )
    if row is None:
        return None
    
    return _build_full_dto(row[0], row[1])


def _build_full_dto(emp: Employee, info: EmployeeInfo) -> FullEmployeeDTO:
    """Merge an Employee ORM row and its EmployeeInfo into a FullEmployeeDTO.

    Args:
        emp (Employee): Core employee ORM record.
        info (EmployeeInfo): Linked employment profile ORM record.

    Returns:
        FullEmployeeDTO: Flat DTO combining both rows.
    """
    return FullEmployeeDTO(
        employee_id=emp.employee_id,
        first_name=emp.first_name,
        last_name=emp.last_name,
        gender=emp.gender,
        email=emp.email,
        manager_email=emp.manager_email,
        laptop=emp.laptop,
        monitor=emp.monitor,
        headset=emp.headset,
        department=info.department,
        salary=info.salary,
        active_projects=info.active_projects,
        avg_monthly_hours=info.avg_monthly_hours,
        years_at_company=info.years_at_company,
        work_accidents=info.work_accidents,
        received_promotion=info.received_promotion,
        last_evaluation=info.last_evaluation,
        satisfaction_score=info.satisfaction_score,
        attrition=info.attrition,
        attrition_risk=info.attrition_risk,
    )


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
        APIResponseDTO.Action: Summary of the action taken.
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
