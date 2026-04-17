"""Prediction schemas — attrition feature DTO and request envelopes."""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from hr_hub.model.dto.employee import Department, Salary


class AttritionFeaturesDTO(BaseModel):
    """Employee features required to compute attrition risk.

    All fields are optional; missing values are filled with dataset medians at
    inference time so partial records can still receive a score.

    Attributes:
        department (Department): Employee's department.
        salary (Salary): Salary tier.
        active_projects (int | None): Number of currently active projects.
        avg_monthly_hours (int | None): Average hours worked per month.
        years_at_company (int | None): Tenure in years.
        work_accidents (bool | None): Whether the employee has had a work accident.
        received_promotion (bool | None): Whether the employee received a promotion in the last 5 years.
        last_evaluation (float | None): Most recent performance score in [0, 1].
        satisfaction_score (float | None): Self-reported satisfaction score in [0, 1].
    """

    model_config = ConfigDict(from_attributes=True)

    department: Department
    salary: Salary
    active_projects: int | None = Field(default=None, ge=0)
    avg_monthly_hours: int | None = Field(default=None, ge=0)
    years_at_company: int | None = Field(default=None, ge=0)
    work_accidents: bool | None = None
    received_promotion: bool | None = None
    last_evaluation: float | None = Field(default=None, ge=0.0, le=1.0)
    satisfaction_score: float | None = Field(default=None, ge=0.0, le=1.0)


class ScoreAllAttritionRequest(BaseModel):
    """Request to re-score attrition risk for all current employees.

    Attributes:
        request_id (str): Unique identifier for the request (e.g., ``"req_002"``).
        request_type (Literal["prediction"]): Must be ``"prediction"``.
    """

    request_id: str
    request_type: Literal["prediction"]
