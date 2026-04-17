"""Shared response envelope for all synchronous HR Hub endpoints."""

from typing import Literal, TypeAlias

from pydantic import BaseModel, ConfigDict

Status: TypeAlias = Literal["Completed", "Pending", "Canceled"]


class APIResponse(BaseModel):
    """Universal response wrapper returned by employee, ticket, and prediction endpoints.

    Attributes:
        request_id (str): Unique identifier for the processed request (e.g., ``"evt_002"``).
        request_type (Literal["new_hire", "employee_change", "prediction"]):
            Type of the request processed.
        status (Status): Processing status.
        actions (list[APIResponse.Action]): Per-step actions taken during processing.
    """

    model_config = ConfigDict(from_attributes=True)

    class Action(BaseModel):
        """A discrete step recorded during request processing.

        Attributes:
            action (Literal[...]): Name of the action taken.
            success (bool): Whether the action succeeded.
            details (str): Human-readable detail or error message.
        """

        action: Literal[
            "create_employee",
            "update_employee",
            "delete_employee",
            "create_task",
            "create_ticket",
            "update_ticket",
            "close_ticket",
            "delete_ticket",
            "score_attrition",
        ]
        success: bool
        details: str

    request_id: str
    request_type: Literal["new_hire", "employee_change", "prediction"]
    status: Status
    actions: list[Action]
