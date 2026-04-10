"""Data Transfer Objects (DTOs) used in HR Hub."""

from hr_hub.model.dto.employee import EmployeeDTO, EmployeeEquipmentDTO, EmployeeInfoDTO
from hr_hub.model.dto.requests import NewHireRequest
from hr_hub.model.dto.requests import EmployeeChangeRequest
from hr_hub.model.dto.requests import TicketRequest
from hr_hub.model.dto.response import APIResponse


__all__ = [
    "EmployeeDTO",
    "EmployeeEquipmentDTO",
    "EmployeeInfoDTO",
    "NewHireRequest",
    "EmployeeChangeRequest",
    "TicketRequest",
    "APIResponse"
]
