"""IT task model."""

from datetime import date
from typing import Any

from pydantic import BaseModel, Field


class ITTask(BaseModel):
    """Model for IT task.

    Attributes:
        task_id (str): Unique identifier for the task (e.g., "task_001")
        title (str): Title of the task
        description (str): Detailed description of the task
        assignee (str): Email of the person or team assigned to the task
        due_date (Date | None): Optional due date for the task
        status (str): Current status of the task (e.g., "open", "in_progress", "closed")
        created_at (Date): Date when the task was created
        metadata (dict[str, Any]): Additional metadata related to the task
    """

    task_id: str
    title: str
    description: str
    assignee: str
    due_date: date | None
    status: str
    created_at: date
    metadata: dict[str, Any] = Field(default_factory=dict)
