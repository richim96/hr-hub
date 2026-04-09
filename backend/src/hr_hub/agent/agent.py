"""HR Hub Agent."""

from dotenv import load_dotenv, find_dotenv
from pydantic_ai import Agent

from backend.src.hr_hub.agent.tools.employee import *


load_dotenv(find_dotenv())

# Create a simple agent
hr_agent = Agent(
    "openai:gpt-5.2",
    system_prompt="You are in charge of handling back office tasks for the HR team.",
    name="HR Agent",
    tools=[],
)
