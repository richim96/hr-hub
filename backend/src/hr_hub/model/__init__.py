"""Models for HR Hub."""

from logging import Logger

from hr_hub.logger import get_logger
from hr_hub.model.orm import Base, Employee, EmployeeInfo, ITTask, Ticket


LOGGER: Logger = get_logger("hr_hub.models")

__all__ = ["Base", "Employee", "EmployeeInfo", "ITTask", "Ticket"]
