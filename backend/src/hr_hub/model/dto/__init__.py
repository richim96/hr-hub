"""Data Transfer Objects (DTOs) used in HR Hub."""

from hr_hub.model.dto.employee import (
    Department,
    Salary,
    EmployeeDTO,
    EmployeeEquipmentDTO,
    EmployeeInfoDTO,
    FullEmployeeDTO,
    NewHireRequest,
    UpdateEmployeeRequest,
)
from hr_hub.model.dto.ticket import TicketDTO, NewTicketRequest, UpdateTicketRequest
from hr_hub.model.dto.it_task import ITTaskDTO, NewITTaskRequest, UpdateITTaskRequest
from hr_hub.model.dto.prediction import AttritionFeaturesDTO, ScoreAllAttritionRequest
from hr_hub.model.dto.agent import AgentChatRequest, AgentChatResponse
from hr_hub.model.dto.response import APIResponse, Status


__all__ = [
    # Employee
    "Department",
    "Salary",
    "EmployeeDTO",
    "EmployeeEquipmentDTO",
    "EmployeeInfoDTO",
    "FullEmployeeDTO",
    "NewHireRequest",
    "UpdateEmployeeRequest",
    # Ticket
    "TicketDTO",
    "NewTicketRequest",
    "UpdateTicketRequest",
    # IT task
    "ITTaskDTO",
    "NewITTaskRequest",
    "UpdateITTaskRequest",
    # Prediction
    "AttritionFeaturesDTO",
    "ScoreAllAttritionRequest",
    # Agent
    "AgentChatRequest",
    "AgentChatResponse",
    # Shared response
    "APIResponse",
    "Status",
]
