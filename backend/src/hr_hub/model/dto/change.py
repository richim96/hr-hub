"""Schema for Change event."""

from pydantic import BaseModel, Field


class ChangeSchema(BaseModel):
    """Change details for a change event.

    Attributes:
        from_value (str): Original value before the change
        to (str): New value after the change
    """

    from_value: str = Field(alias="from")
    to: str
