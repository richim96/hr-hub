"""Employee schemas — identity, equipment, employment info, and request envelopes."""

from typing import Literal, TypeAlias
from uuid import uuid4
from pydantic import BaseModel, Field, EmailStr, ConfigDict

Department: TypeAlias = Literal[
    "accounting", "engineering", "hr", "IT", "management",
    "marketing", "product_management", "r&d", "sales", "support",
]
Salary: TypeAlias = Literal["low", "medium", "high"]


class EmployeeDTO(BaseModel):
    """Employee details.

    Attributes:
        employee_id (str): Unique identifier for the employee, generated as a UUID4 string.
        first_name (str): Employee's first name.
        last_name (str): Employee's last name.
        gender (str | None): M or F, employee's gender.
        email (EmailStr): Employee's email address.
        manager_email (EmailStr | None): Employee's manager's email address. Null for the top-level employee.
    """

    model_config = ConfigDict(from_attributes=True)

    employee_id: str = Field(default_factory=lambda: str(uuid4()))
    first_name: str
    last_name: str
    gender: str | None = None
    email: EmailStr
    manager_email: EmailStr | None = None


class EmployeeEquipmentDTO(BaseModel):
    """Employee equipment details.

    Attributes:
        laptop (str | None): Laptop model assigned to the employee.
        monitor (bool | None): Whether a monitor is provided.
        headset (bool | None): Whether a headset is provided.
    """

    model_config = ConfigDict(from_attributes=True)

    laptop: str | None = None
    monitor: bool | None = None
    headset: bool | None = None


class EmployeeInfoDTO(BaseModel):
    """Employment profile and attrition signals for an employee.

    Mirrors the ``employee_info`` ORM table. Optional fields reflect columns
    that are nullable in the database.

    Attributes:
        department (Department): Department the employee belongs to.
        salary (Salary): Salary tier of the employee.
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

    department: Department
    salary: Salary
    active_projects: int | None = Field(default=None, ge=0)
    avg_monthly_hours: int | None = Field(default=None, ge=0)
    years_at_company: int | None = Field(default=None, ge=0)
    work_accidents: bool | None = None
    received_promotion: bool | None = None
    last_evaluation: float | None = Field(default=None, ge=0.0, le=1.0)
    satisfaction_score: float | None = Field(default=None, ge=0.0, le=1.0)
    attrition: bool | None = None
    attrition_risk: float | None = Field(default=None, ge=0.0, le=1.0)


class FullEmployeeDTO(BaseModel):
    """Flat join of Employee, EmployeeEquipment, and EmployeeInfo — used for list responses.

    Attributes:
        employee_id (str): Unique identifier for the employee.
        first_name (str): Employee's first name.
        last_name (str): Employee's last name.
        gender (str | None): M or F.
        email (EmailStr): Employee's email address.
        manager_email (EmailStr | None): Manager's email address.
        laptop (str | None): Laptop model assigned.
        monitor (bool | None): Whether a monitor is provided.
        headset (bool | None): Whether a headset is provided.
        department (Department): Department the employee belongs to.
        salary (Salary): Salary tier.
        active_projects (int | None): Number of active projects.
        avg_monthly_hours (int | None): Average monthly hours worked.
        years_at_company (int | None): Years at the company.
        work_accidents (bool | None): Whether the employee has had a work accident.
        received_promotion (bool | None): Whether the employee received a promotion.
        last_evaluation (float | None): Last evaluation score in [0, 1].
        satisfaction_score (float | None): Satisfaction score in [0, 1].
        attrition (bool | None): Whether the employee has left.
        attrition_risk (float | None): Predicted attrition probability in [0, 1].
    """

    model_config = ConfigDict(from_attributes=True)

    # Identity
    employee_id: str
    first_name: str
    last_name: str
    gender: str | None = None
    email: EmailStr
    manager_email: EmailStr | None = None

    # Equipment
    laptop: str | None = None
    monitor: bool | None = None
    headset: bool | None = None

    # Employment info
    department: Department
    salary: Salary
    active_projects: int | None = Field(default=None, ge=0)
    avg_monthly_hours: int | None = Field(default=None, ge=0)
    years_at_company: int | None = Field(default=None, ge=0)
    work_accidents: bool | None = None
    received_promotion: bool | None = None
    last_evaluation: float | None = Field(default=None, ge=0.0, le=1.0)
    satisfaction_score: float | None = Field(default=None, ge=0.0, le=1.0)
    attrition: bool | None = None
    attrition_risk: float | None = Field(default=None, ge=0.0, le=1.0)


class NewHireRequest(BaseModel):
    """Inbound payload for onboarding a new employee.

    Attributes:
        request_id (str): Unique identifier for the request (e.g., ``"evt_001"``).
        request_type (Literal["new_hire"]): Must be ``"new_hire"``.
        employee (EmployeeDTO): Core identity fields.
        equipment (EmployeeEquipmentDTO): Equipment to provision.
        info (EmployeeInfoDTO): Employment profile.
    """

    request_id: str
    request_type: Literal["new_hire"]
    employee: EmployeeDTO
    equipment: EmployeeEquipmentDTO
    info: EmployeeInfoDTO


class UpdateEmployeeRequest(BaseModel):
    """Partial-update payload for an existing employee.

    All fields are optional — only non-None values are written to the database.

    Attributes:
        first_name (str | None): Updated first name.
        last_name (str | None): Updated last name.
        gender (Literal["M", "F"] | None): Updated gender.
        email (EmailStr | None): Updated email address.
        manager_email (EmailStr | None): Updated manager email.
        laptop (str | None): Updated laptop model.
        monitor (bool | None): Updated monitor flag.
        headset (bool | None): Updated headset flag.
        department (Department | None): Updated department.
        salary (Salary | None): Updated salary tier.
        active_projects (int | None): Updated active project count.
        avg_monthly_hours (int | None): Updated average monthly hours.
        years_at_company (int | None): Updated years at company.
        work_accidents (bool | None): Updated work accidents flag.
        received_promotion (bool | None): Updated promotion flag.
        last_evaluation (float | None): Updated last evaluation score in [0, 1].
        satisfaction_score (float | None): Updated satisfaction score in [0, 1].
        attrition (bool | None): Updated attrition flag.
        attrition_risk (float | None): Updated attrition risk score in [0, 1].
    """

    model_config = ConfigDict(from_attributes=True)

    # Identity
    first_name: str | None = None
    last_name: str | None = None
    gender: Literal["M", "F"] | None = None
    email: EmailStr | None = None
    manager_email: EmailStr | None = None

    # Equipment
    laptop: str | None = None
    monitor: bool | None = None
    headset: bool | None = None

    # Employment info
    department: Department | None = None
    salary: Salary | None = None
    active_projects: int | None = Field(default=None, ge=0)
    avg_monthly_hours: int | None = Field(default=None, ge=0)
    years_at_company: int | None = Field(default=None, ge=0)
    work_accidents: bool | None = None
    received_promotion: bool | None = None
    last_evaluation: float | None = Field(default=None, ge=0.0, le=1.0)
    satisfaction_score: float | None = Field(default=None, ge=0.0, le=1.0)
    attrition: bool | None = None
    attrition_risk: float | None = Field(default=None, ge=0.0, le=1.0)
