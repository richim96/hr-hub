"""Pydantic response schema for IT tasks."""

from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict


class ITTaskDTO(BaseModel):
    """Full IT task record — used for all task responses.

    Attributes:
        task_id (str): Unique identifier for the task.
        employee_id (str): ID of the employee this task belongs to.
        employee_email (str | None): Email of the employee. Indexed on the DB.
        title (str): Short title of the task.
        description (str | None): Detailed description of the work required.
        assignee (str | None): Email of the person or team assigned to this task.
        due_date (datetime | None): Optional deadline for the task.
        status (Literal["Pending", "Completed", "Canceled"] | None): Current task status.
        task_metadata (dict[str, Any] | None): Arbitrary additional metadata.
    """

    model_config = ConfigDict(from_attributes=True)

    task_id: str
    employee_id: str
    employee_email: str | None = None
    title: str
    description: str | None = None
    assignee: str | None = None
    due_date: datetime | None = None
    status: Literal["Pending", "Completed", "Canceled"] | None = None
    task_metadata: dict[str, Any] | None = None
