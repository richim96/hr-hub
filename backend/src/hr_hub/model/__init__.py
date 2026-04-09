"""Models for HR Hub."""

from logging import Logger

from hr_hub.logger import get_logger
# from hr_hub.models.employee import Employee
from hr_hub.model.it_task import ITTask


LOGGER: Logger = get_logger("hr_hub.models")

__all__ = ["ITTask"]
