"""Data Transfer Objects (DTOs) used in HR Hub."""

from hr_hub.model.dto.employee import EmployeeSchema
from hr_hub.model.dto.requests import NewHireRequest
from hr_hub.model.dto.requests import EmployeeChangeRequest
from hr_hub.model.dto.requests import TicketRequest
from hr_hub.model.dto.response import ResponseSchema


__all__ = [
    "EmployeeSchema",
    "NewHireRequest",
    "EmployeeChangeRequest",
    "TicketRequest",
    "ResponseSchema"
]
