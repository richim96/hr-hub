"""API for IT task management."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from hr_hub.api import LOGGER
from hr_hub.db import get_session
from hr_hub.model.dto import ITTaskDTO, NewITTaskRequest, UpdateITTaskRequest
from hr_hub.service.it_task import list_it_tasks, get_it_task, create_it_task, update_it_task, delete_it_task


it_task_router: APIRouter = APIRouter(prefix="/it-tasks", tags=["IT Tasks"])


@it_task_router.get("", response_model=list[ITTaskDTO])
async def get_it_tasks(
    employee_id: str | None = None,
    session: Session = Depends(get_session),
) -> list[ITTaskDTO]:
    """List all IT tasks, optionally filtered by employee.

    Args:
        employee_id (str | None): If provided, only return tasks for this employee.
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"List tasks request [ employee_id={employee_id} ]")
    return list_it_tasks(session, employee_id)


@it_task_router.get("/{task_id}", response_model=ITTaskDTO)
async def get_it_task_by_id(
    task_id: str,
    session: Session = Depends(get_session),
) -> ITTaskDTO:
    """Fetch a single IT task by ID.

    Args:
        task_id (str): Primary key of the task (path parameter).
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Get task request [ task_id={task_id} ]")
    task = get_it_task(task_id, session)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id!r} not found.")
    
    return task


@it_task_router.post("", response_model=ITTaskDTO, status_code=201)
async def post_it_task(
    payload: NewITTaskRequest,
    session: Session = Depends(get_session),
) -> ITTaskDTO:
    """Create a new IT task.

    Args:
        payload (NewITTaskRequest): Task data.
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Create task request [ employee_id={payload.employee_id} -> {payload.title!r} ]")
    task = create_it_task(payload, session)

    if task is None:
        raise HTTPException(status_code=500, detail="Failed to create task.")
    
    return task


@it_task_router.patch("/{task_id}", response_model=ITTaskDTO)
async def patch_it_task(
    task_id: str,
    payload: UpdateITTaskRequest,
    session: Session = Depends(get_session),
) -> ITTaskDTO:
    """Apply a partial update to an existing IT task.

    Args:
        task_id (str): Primary key of the task to update (path parameter).
        payload (UpdateITTaskRequest): Fields to update.
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Update task request [ task_id={task_id} ]")
    task = update_it_task(task_id, payload, session)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id!r} not found.")

    return task



@it_task_router.delete("/{task_id}", status_code=204)
async def remove_it_task(
    task_id: str,
    session: Session = Depends(get_session),
) -> None:
    """Delete an IT task by ID.

    Args:
        task_id (str): Primary key of the task to delete (path parameter).
        session (Session): SQLAlchemy session — injected by FastAPI.
    """
    LOGGER.info(f"Delete task request [ task_id={task_id} ]")
    deleted = delete_it_task(task_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id!r} not found.")
