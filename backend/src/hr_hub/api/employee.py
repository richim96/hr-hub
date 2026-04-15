"""API for creating employees and updating employee data."""

from typing import Any

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from hr_hub.api import LOGGER
from hr_hub.db import get_session
from hr_hub.service.prediction import get_attrition_model
from hr_hub.model.dto import NewHireRequest, UpdateEmployeeRequest, FullEmployeeDTO
from hr_hub.model.dto import APIResponseDTO
from hr_hub.service.employee import start_onboarding, list_employees, get_employee, update_employee, delete_employee


employee_router: APIRouter = APIRouter(prefix="/employee", tags=["Employee Operations"])


@employee_router.get("", response_model=list[FullEmployeeDTO])
async def get_employees(
    session: Session = Depends(get_session),
) -> list[FullEmployeeDTO]:
    """List all current employees (attrition=False) with their full profile.

    Args:
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info("List employees request")
    return list_employees(session)


@employee_router.get("/{employee_id}", response_model=FullEmployeeDTO)
async def get_employee_by_id(
    employee_id: str,
    session: Session = Depends(get_session),
) -> FullEmployeeDTO:
    """Fetch a single current employee by ID.

    Args:
        employee_id (str): Primary key of the employee (path parameter).
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Get employee request [ employee_id={employee_id} ]")
    emp = get_employee(employee_id, session)
    if emp is None:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id!r} not found.")
    return emp


@employee_router.post("/new-hire", response_model=APIResponseDTO)
async def create_employee(
    request: NewHireRequest,
    session: Session = Depends(get_session),
    attrition_model: Any | None = Depends(get_attrition_model),
) -> APIResponseDTO:
    """Create a new employee.

    Args:
        request (NewHireRequestDTO): The new hire request data.
        session (Session): The SQLAlchemy session connecting to the database.
        attrition_model (Any | None): Attrition prediction model — injected by FastAPI.
    """
    LOGGER.info(
        f"Received request for new hire [ {request.request_id} -> {request.employee.email} ]."
    )
    return start_onboarding(request, session, attrition_model)


@employee_router.patch("/{employee_id}", response_model=APIResponseDTO)
async def patch_employee(
    employee_id: str,
    request: UpdateEmployeeRequest,
    session: Session = Depends(get_session),
    attrition_model: Any | None = Depends(get_attrition_model),
) -> APIResponseDTO:
    """Partially update an employee's identity, equipment, or employment info.

    Triggers attrition re-scoring after a successful update.

    Args:
        employee_id (str): Primary key of the employee (path parameter).
        request (UpdateEmployeeRequest): Fields to update; omitted fields are unchanged.
        session (Session): SQLAlchemy session — injected by FastAPI.
        attrition_model (Any | None): Attrition prediction model — injected by FastAPI.
    """
    LOGGER.info(f"Update employee request [ employee_id={employee_id} ]")
    return update_employee(employee_id, request, session, attrition_model)


@employee_router.delete("/{employee_id}", response_model=APIResponseDTO)
async def remove_employee(
    employee_id: str,
    session: Session = Depends(get_session),
) -> APIResponseDTO:
    """Hard-delete an employee and all their related records.

    Args:
        employee_id (str): Primary key of the employee (path parameter).
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Delete employee request [ employee_id={employee_id} ]")
    return delete_employee(employee_id, session)
