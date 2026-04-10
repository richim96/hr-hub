"""Schema for Change event."""

from pydantic import BaseModel, Field, ConfigDict


class ChangeDTO(BaseModel):
    """Change details for a change request.

    Attributes:
        from_value (str): Original value before the change
        to (str): New value after the change
    """

    from_value: str = Field(alias="from")
    to: str

    model_config = ConfigDict(from_attributes=True)
