"""Data Transfer Objects (DTOs) used in HR Hub."""

from hr_hub.model.dto.employee import EmployeeDTO, EmployeeEquipmentDTO, EmployeeInfoDTO, FullEmployeeDTO
from hr_hub.model.dto.prediction import AttritionFeaturesDTO
from hr_hub.model.dto.requests import NewHireRequest
from hr_hub.model.dto.requests import UpdateEmployeeRequest
from hr_hub.model.dto.requests import NewTicketRequest
from hr_hub.model.dto.requests import UpdateTicketRequest
from hr_hub.model.dto.requests import ScoreAllAttritionRequest
from hr_hub.model.dto.requests import NewITTaskRequest
from hr_hub.model.dto.requests import UpdateITTaskRequest
from hr_hub.model.dto.response import APIResponseDTO
from hr_hub.model.dto.it_task import ITTaskDTO


__all__ = [
    "EmployeeDTO",
    "EmployeeEquipmentDTO",
    "EmployeeInfoDTO",
    "FullEmployeeDTO",
    "AttritionFeaturesDTO",
    "ScoreAllAttritionRequest",
    "NewHireRequest",
    "UpdateEmployeeRequest",
    "NewTicketRequest",
    "UpdateTicketRequest",
    "NewITTaskRequest",
    "UpdateITTaskRequest",
    "APIResponseDTO",
    "ITTaskDTO",
]
