"""IT task CRUD service."""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Literal

from sqlalchemy.orm import Session

from hr_hub.model import ITTask
from hr_hub.model.dto import APIResponse
from hr_hub.model.dto.it_task import ITTaskDTO, NewITTaskRequest, UpdateITTaskRequest
from hr_hub.service import LOGGER


_DEFAULT_ASSIGNEE = "it-team@company.com"


def _due_in_business_days(days: int) -> datetime:
    """Return a UTC datetime that is ``days`` business days from now.

    Args:
        days (int): Number of business days (Monday–Friday) to add.

    Returns:
        datetime: UTC timestamp ``days`` working days in the future.
    """
    current = datetime.now(timezone.utc)
    count = 0
    while count < days:
        current += timedelta(days=1)
        if current.weekday() < 5:
            count += 1
    return current


# ---------------------------------------------------------------------------
# Onboarding task definitions
# ---------------------------------------------------------------------------

_DEFAULT_TASKS: list[tuple[str, str]] = [
    (
        "Provision hardware",
        "Prepare and ship the assigned equipment (laptop, monitor, headset) to the new hire.",
    ),
    (
        "Create system accounts",
        "Set up corporate email, Slack workspace, and HR portal access.",
    ),
    (
        "Schedule onboarding orientation",
        "Book the HR onboarding session and the first 1:1 with the direct manager.",
    ),
]

# One tuple per department (title, description). Engineering gets two entries.
_DEPARTMENT_TASKS: dict[str, list[tuple[str, str]]] = {
    "accounting": [
        (
            "Grant accounting software access",
            "Provision access to financial reporting and accounting tools (QuickBooks / SAP).",
        ),
    ],
    "engineering": [
        (
            "Add Claude Pro subscription",
            "Create a Claude Pro seat for the new engineer and add them to the team workspace.",
        ),
        (
            "Add to GitHub organization",
            "Send a GitHub organization invite and assign the appropriate team repositories.",
        ),
    ],
    "hr": [
        (
            "Enroll in HRIS and payroll system",
            "Set up access to the HR information system and complete payroll enrollment.",
        ),
    ],
    "IT": [
        (
            "Configure IT admin tools",
            "Provision IT service desk access and infrastructure management tool credentials.",
        ),
    ],
    "management": [
        (
            "Schedule executive onboarding briefing",
            "Arrange introductory meetings with senior leadership and provide strategic context.",
        ),
    ],
    "marketing": [
        (
            "Set up marketing platform access",
            "Grant access to CRM, design tools (Figma), and campaign management platforms.",
        ),
    ],
    "product_management": [
        (
            "Set up product management tools",
            "Grant access to Jira, Confluence, and product analytics platforms.",
        ),
    ],
    "r&d": [
        (
            "Complete lab access and safety induction",
            "Set up laboratory credentials and schedule the mandatory safety briefing.",
        ),
    ],
    "sales": [
        (
            "Configure CRM and assign sales territory",
            "Set up Salesforce access and assign the new hire's initial sales territory.",
        ),
    ],
    "support": [
        (
            "Set up customer support platform access",
            "Grant access to the ticketing system (Zendesk / Intercom) and support knowledge base.",
        ),
    ],
}


def create_onboarding_tasks(
    employee_id: str,
    employee_email: str,
    department: Literal[
        "accounting", "engineering", "hr", "IT", "management",
        "marketing", "product_management", "r&d", "sales", "support",
    ],
    session: Session,
) -> list[APIResponse.Action]:
    """Create the default onboarding IT tasks for a newly hired employee.

    Inserts 3 tasks common to all employees plus department-specific tasks
    (1 per department, 2 for engineering).  Each task produces one
    ``create_task`` action in the returned list.  On DB failure a single
    failure action is returned instead.

    Args:
        employee_id (str): Primary key of the new employee.
        employee_email (str): Email address of the new employee.
        department (Literal["accounting", "engineering", "hr", "IT", "management", "marketing", "product_management", "r&d", "sales", "support"]): The employee's department, used to select extra tasks.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        list[APIResponseDTO.Action]: One action per created task, or a single failure action on error.
    """
    task_definitions: list[tuple[str, str]] = (
        _DEFAULT_TASKS + _DEPARTMENT_TASKS.get(department, [])
    )
    due_date = _due_in_business_days(5)

    rows: list[ITTask] = [
        ITTask(
            task_id=f"task_{uuid.uuid4().hex}",
            employee_id=employee_id,
            employee_email=employee_email,
            title=title,
            description=description,
            assignee=_DEFAULT_ASSIGNEE,
            due_date=due_date,
            status="Pending",
        )
        for title, description in task_definitions
    ]

    try:
        for row in rows:
            session.add(row)
        session.flush()
        LOGGER.info(
            f"Created {len(rows)} onboarding tasks for employee {employee_id} "
            f"(department={department})"
        )
        return [
            APIResponse.Action(
                action="create_task",
                success=True,
                details=f"Task '{row.title}' created for {employee_id}.",
            )
            for row in rows
        ]
    except Exception as e:
        LOGGER.error(f"Could not create onboarding tasks for {employee_id}: {e}")
        return [
            APIResponse.Action(
                action="create_task",
                success=False,
                details=f"Could not create onboarding tasks: {e}",
            )
        ]


def list_it_tasks(session: Session, employee_id: str | None = None) -> list[ITTaskDTO]:
    """Return all IT tasks, optionally scoped to a single employee.

    Args:
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.
        employee_id (str | None): If provided, only return tasks for this employee.

    Returns:
        list[ITTaskDTO]: All matching IT task records.
    """
    try:
        query = session.query(ITTask)
        if employee_id:
            query = query.filter(ITTask.employee_id == employee_id)
        rows: list[ITTask] = query.all()
        return [ITTaskDTO.model_validate(row) for row in rows]
    except Exception as e:
        LOGGER.error(f"DB error fetching tasks: {e}")
        return []


def get_it_task(task_id: str, session: Session) -> ITTaskDTO | None:
    """Fetch a single IT task by its primary key.

    Args:
        task_id (str): Primary key of the task to retrieve.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        ITTaskDTO: The task record, or None if not found.
    """
    try:
        row: ITTask | None = session.query(ITTask).filter(ITTask.task_id == task_id).first()
        return ITTaskDTO.model_validate(row) if row else None
    except Exception as e:
        LOGGER.error(f"DB error fetching task {task_id}: {e}")
        return None


def create_it_task(payload: NewITTaskRequest, session: Session) -> ITTaskDTO | None:
    """Insert a new IT task and return the persisted record.

    Args:
        payload (NewITTaskRequest): Task data supplied by the caller.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        ITTaskDTO: The newly created task, or None if the insert failed.
    """
    task_id = f"task_{uuid.uuid4().hex}"
    row = ITTask(
        task_id=task_id,
        employee_id=payload.employee_id,
        employee_email=payload.employee_email,
        title=payload.title,
        description=payload.description,
        assignee=payload.assignee,
        due_date=payload.due_date,
        status=payload.status,
        task_metadata=payload.task_metadata,
    )

    try:
        session.add(row)
        session.flush()
        LOGGER.info(f"Created task {task_id} for employee {payload.employee_id}")
        return ITTaskDTO.model_validate(row)
    except Exception as e:
        LOGGER.error(f"Could not create task for employee {payload.employee_id}: {e}")
        return None


def update_it_task(task_id: str, payload: UpdateITTaskRequest, session: Session) -> ITTaskDTO | None:
    """Apply a partial update to an existing IT task.

    Only fields explicitly set in the payload (non-None) are written to the DB.

    Args:
        task_id (str): Primary key of the task to update.
        payload (UpdateITTaskRequest): Fields to update (all optional).
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        ITTaskDTO: The updated task, or None if not found or update failed.
    """
    try:
        row: ITTask | None = session.query(ITTask).filter(ITTask.task_id == task_id).first()
    except Exception as e:
        LOGGER.error(f"DB error fetching task {task_id} for update: {e}")
        return None

    if row is None:
        return None

    updates = payload.model_dump()
    for field, value in updates.items():
        setattr(row, field, value)

    try:
        session.flush()
        LOGGER.info(f"Updated task {task_id}: {list(updates.keys())}")
        return ITTaskDTO.model_validate(row)
    except Exception as e:
        LOGGER.error(f"Could not update task {task_id}: {e}")
        return None


def delete_it_task(task_id: str, session: Session) -> bool:
    """Delete an IT task by its primary key.

    Args:
        task_id (str): Primary key of the task to delete.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        bool: True if the task was deleted, False if not found or deletion failed.
    """
    try:
        row: ITTask | None = session.query(ITTask).filter(ITTask.task_id == task_id).first()
    except Exception as e:
        LOGGER.error(f"DB error fetching task {task_id} for deletion: {e}")
        return False

    try:
        session.delete(row)
        session.flush()
        LOGGER.info(f"Deleted task {task_id}")
    except Exception as e:
        LOGGER.error(f"Could not delete task {task_id}: {e}")
        return False
    
    return True
