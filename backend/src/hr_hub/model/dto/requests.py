"""DTOs for processing frontend requests."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from hr_hub.model.dto.employee import EmployeeDTO, EmployeeEquipmentDTO, EmployeeInfoDTO


class NewHireRequest(BaseModel):
    """Data Transfer Object for new hire requests.

    Attributes:
        request_id (str): Unique identifier for the new hire request (e.g., "evt_001")
        request_type (Literal["new_hire"]): Type of request.
        employee (EmployeeDTO): Employee details
        equipment (EmployeeEquipmentDTO): Equipment details for the new hire
        info (EmployeeInfoDTO): Detailed info of the new hire
    """

    request_id: str
    request_type: Literal["new_hire"]
    employee: EmployeeDTO
    equipment: EmployeeEquipmentDTO
    info: EmployeeInfoDTO


class UpdateEmployeeRequest(BaseModel):
    """Partial-update payload for an existing employee.

    All fields are optional — only non-None fields are written to the database.
    Covers identity, equipment, and employment-info columns.

    Attributes:
        first_name (str | None): Updated first name.
        last_name (str | None): Updated last name.
        gender (Literal["M", "F"] | None): Updated gender.
        email (EmailStr | None): Updated email address.
        manager_email (EmailStr | None): Updated manager email.
        laptop (str | None): Updated laptop model.
        monitor (bool | None): Updated monitor flag.
        headset (bool | None): Updated headset flag.
        department (Literal["sales", "engineering", "support", "IT", "product_management", "marketing", "r&d", "accounting", "hr", "management"] | None): Updated department.
        salary (Literal["low", "medium", "high"] | None): Updated salary tier.
        active_projects (int | None): Updated active project count.
        avg_monthly_hours (int | None): Updated average monthly hours.
        years_at_company (int | None): Updated years at company.
        work_accidents (bool | None): Updated work accidents flag.
        received_promotion (bool | None): Updated promotion flag.
        last_evaluation (float | None): Updated last evaluation score in [0, 1].
        satisfaction_score (float | None): Updated satisfaction score in [0, 1].
        attrition (bool | None): Updated attrition flag.
        attrition_risk (float | None): Updated attrition risk score in [0, 1].
    """

    model_config = ConfigDict(from_attributes=True)

    # Identity
    first_name: str | None = None
    last_name: str | None = None
    gender: Literal["M", "F"] | None = None
    email: EmailStr | None = None
    manager_email: EmailStr | None = None

    # Equipment
    laptop: str | None = None
    monitor: bool | None = None
    headset: bool | None = None

    # Employment info
    department: Literal[
        "sales", "engineering", "support", "IT", "product_management",
        "marketing", "r&d", "accounting", "hr", "management",
    ] | None = None
    salary: Literal["low", "medium", "high"] | None = None
    active_projects: int | None = Field(default=None, ge=0)
    avg_monthly_hours: int | None = Field(default=None, ge=0)
    years_at_company: int | None = Field(default=None, ge=0)
    work_accidents: bool | None = None
    received_promotion: bool | None = None
    last_evaluation: float | None = Field(default=None, ge=0.0, le=1.0)
    satisfaction_score: float | None = Field(default=None, ge=0.0, le=1.0)
    attrition: bool | None = None
    attrition_risk: float | None = Field(default=None, ge=0.0, le=1.0)


class NewTicketRequest(BaseModel):
    """Data Transfer Object for people ticket events.

    Attributes:
        request_id (str): Unique identifier for the ticket request (e.g., "evt_003").
        request_type (Literal["people_ticket"]): Type of request.
        submitted_by (EmailStr): Email of the person who submitted the ticket.
        title (str): Title of the ticket.
        text (str): Detailed description of the ticket issue.
    """

    request_id: str
    request_type: Literal["people_ticket"]
    submitted_by: EmailStr
    title: str
    text: str


class UpdateTicketRequest(BaseModel):
    """Partial-update payload for an existing people-team ticket.

    All fields are optional — only non-None fields are written to the database.

    Attributes:
        title (str | None): Updated ticket title.
        text (str | None): Updated ticket description.
    """

    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    text: str | None = None


class ScoreAllAttritionRequest(BaseModel):
    """Request to re-score attrition risk for all current employees.

    Attributes:
        request_id (str): Unique identifier for the request (e.g., "req_002").
        request_type (Literal["prediction"]): Must be "prediction".
    """

    request_id: str
    request_type: Literal["prediction"]


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


