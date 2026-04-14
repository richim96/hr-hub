"""DTOs for processing frontend requests."""

from datetime import date
from typing import TypeAlias, Literal

from pydantic import BaseModel, EmailStr

from hr_hub.model.dto.employee import EmployeeDTO, EmployeeEquipmentDTO, EmployeeInfoDTO
from hr_hub.model.dto.change import ChangeDTO


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


class EmployeeChangeRequest(BaseModel):
    """Data Transfer Object for employee change events.

    Attributes:
        request_id (str): Unique identifier for the change request (e.g., "evt_002")
        request_type (Literal["employee_change"]): Type of request.
        employee_email (EmailStr): Email of the employee undergoing the change
        changes (dict[str, ChangeSchema]):
            Dictionary of changed fields with their old and new values
        effective_date (Date): Date when the change takes effect
    """

    request_id: str
    request_type: Literal["employee_change"]
    employee_email: EmailStr
    changes: dict[EmployeeField, ChangeDTO]
    effective_date: date


class TicketRequest(BaseModel):
    """Data Transfer Object for people ticket events.

    Attributes:
        event_id (str): Unique identifier for the ticket request (e.g., "evt_003")
        request_type (Literal["people_ticket"]): Type of request.
        submitted_by (EmailStr): Email of the person who submitted the ticket
        subject (str): Subject of the ticket
        text (str): Detailed description of the ticket issue
    """

    request_id: str
    request_type: Literal["people_ticket"]
    submitted_by: EmailStr
    subject: str
    text: str


# ----- Type Aliases -----
EmployeeField: TypeAlias = Literal[
    "first_name",
    "last_name",
    "email",
    "start_date",
    "team",
    "role",
    "manager",
    "location",
]
