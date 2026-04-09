"""Agent for HR Hub."""

from logging import Logger

from hr_hub.logger import get_logger
from hr_hub.agent.agent import hr_agent

LOGGER: Logger = get_logger("hr_hub.agent")

__all__ = ["hr_agent"]
