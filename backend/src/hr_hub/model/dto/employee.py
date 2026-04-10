"""Employee schema."""

from typing import Literal
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class EmployeeDTO(BaseModel):
    """Employee details.

    Attributes:
        employee_id (str): Unique identifier for the employee (e.g., "emp_001")
        first_name  (str): Employee's first name
        last_name (str): Employee's last name
        gender (str): M or F, employee's gender
        email (EmailStr): Employee's email address
        manager_email (EmailStr): Employee's manager's email address
    """
    model_config = ConfigDict(from_attributes=True)

    employee_id: str
    first_name: str
    last_name: str
    gender: str | None = None
    email: EmailStr
    manager_email: EmailStr


class EmployeeEquipmentDTO(BaseModel):
    """Employee equipment details.

    Attributes:
        laptop (str): Laptop model assigned to the employee
        monitor (bool): Whether a monitor is provided
        headset (bool): Whether a headset is provided
    """
    model_config = ConfigDict(from_attributes=True)

    laptop: str | None = None
    monitor: bool | None = None
    headset: bool | None = None


class EmployeeInfoDTO(BaseModel):
    """Employment profile and attrition signals for an employee.

    Mirrors the `employee_info` ORM table. Optional fields reflect columns
    that are nullable in the database.

    Attributes:
        department (Literal["sales", "engineering", "support", "IT", "product_management", "marketing", "r&d", "accounting", "hr", "management"]):
            Department the employee belongs to.
        salary (Literal["low", "medium", "high"]):
            Salary tier of the employee.
        active_projects (int | None): Number of active projects.
        avg_monthly_hours (int | None): Average monthly hours worked.
        years_at_company (int | None): Number of years at the company.
        work_accidents (bool | None): Whether the employee has had a work accident.
        received_promotion (bool | None): Whether the employee has received a promotion.
        last_evaluation (float | None): Last performance evaluation score in [0, 1].
        satisfaction_score (float | None): Employee satisfaction score in [0, 1].
        attrition (bool | None): Whether the employee has left the company.
        attrition_risk (float | None): Predicted probability of attrition in [0, 1].
    """
    model_config = ConfigDict(from_attributes=True)

    department: Literal[
        "sales",
        "engineering",
        "support",
        "IT",
        "product_management",
        "marketing",
        "r&d",
        "accounting",
        "hr",
        "management",
    ]
    salary: Literal["low", "medium", "high"] | None = None
    active_projects: int | None = Field(default=None, ge=0)
    avg_monthly_hours: int | None = Field(default=None, ge=0)
    years_at_company: int | None = Field(default=None, ge=0)
    work_accidents: bool | None = None
    received_promotion: bool | None = None
    last_evaluation: float | None = Field(default=None, ge=0.0, le=1.0)
    satisfaction_score: float | None = Field(default=None, ge=0.0, le=1.0)
    attrition: bool | None = None
    attrition_risk: float | None = Field(default=None, ge=0.0, le=1.0)
