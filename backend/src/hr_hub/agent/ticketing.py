"""Ticketing classification agent submodule."""

from pydantic import BaseModel, Field
from pydantic_ai import Agent


class TicketClassification(BaseModel):
    """Structured output from the ticket classifier agent.

    Attributes:
        topics (list[str]): Up to 3 specific HR topics mentioned in the ticket text
            (e.g. ``["payroll", "overtime", "health_insurance"]``).
        summary (str): One-sentence description of what the ticket is about.
    """

    topics: list[str] = Field(description="Up to 3 specific HR topics mentioned in the ticket", max_length=3)
    summary: str = Field(description="One-sentence description of the ticket issue")


ticket_agent: Agent[None, TicketClassification] = Agent(
    name="HR Ticket Classifier",
    model="groq:llama-3.1-8b-instant",
    output_type=TicketClassification,
    system_prompt="""\
You are an HR ticket classifier for the HR Hub system.

Given the text of an HR support ticket, extract:
  • topics — 1 to 3 specific HR topics present in the ticket
    (e.g. 'payroll', 'overtime', 'health_insurance', 'remote_work').
    Never include more than 3.
  • summary — one clear sentence that explains what the employee is asking.

Respond only with the structured output — no extra commentary.
""",
)
