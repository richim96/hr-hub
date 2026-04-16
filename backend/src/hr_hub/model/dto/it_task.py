"""IT task schemas — read DTO and request envelopes."""

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


class NewITTaskRequest(BaseModel):
    """Inbound payload for creating a new IT task.

    Attributes:
        employee_id (str): ID of the employee this task belongs to.
        employee_email (str): Email of the employee.
        title (str): Short title of the task.
        description (str): Detailed description of the work required.
        assignee (str): Email of the person or team assigned to this task.
        due_date (datetime): Deadline for the task.
        status (Literal["Pending", "Completed", "Canceled"]): Initial task status.
        task_metadata (dict[str, Any] | None): Arbitrary additional metadata.
    """

    model_config = ConfigDict(from_attributes=True)

    employee_id: str
    employee_email: str
    title: str
    description: str
    assignee: str
    due_date: datetime
    status: Literal["Pending", "Completed", "Canceled"] = "Pending"
    task_metadata: dict[str, Any] | None = None


class UpdateITTaskRequest(BaseModel):
    """Inbound payload for updating an existing IT task.

    Attributes:
        title (str): Updated task title.
        description (str): Updated task description.
        assignee (str): Updated assignee.
        due_date (datetime): Updated deadline.
        status (Literal["Pending", "Completed", "Canceled"]): Updated status.
    """

    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    assignee: str
    due_date: datetime
    status: Literal["Pending", "Completed", "Canceled"]
