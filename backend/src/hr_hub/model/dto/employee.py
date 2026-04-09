"""Employee schema."""

from datetime import date
from pydantic import BaseModel, Field, EmailStr

class EmployeeDTO(BaseModel):
    """Employee details.

    Attributes:
        employee_id (str): Unique identifier for the employee (e.g., "emp_001")
        first_name  (str): Employee's first name
        last_name (str): Employee's last name
        gender (str): M or F, employee's gender
        email (EmailStr): Employee's email address
        manager_email (EmailStr): Employee's manager's email address
        start_date (Date): Employee's start date
    """

    employee_id: str | None = Field(
        default=None, validation_alias="id", serialization_alias="id"
    )
    first_name: str
    last_name: str
    gender: str
    email: EmailStr
    manager_email: EmailStr
    start_date: date


class EmployeeEquipmentDTO(BaseModel):
    """Employee equipment details.

    Attributes:
        laptop (str): Laptop model assigned to the employee
        monitor (bool): Whether a monitor is provided
        headset (bool): Whether a headset is provided
    """

    laptop: str
    monitor: bool
    headset: bool


class EmployeeInfoDTO(BaseModel):

    department: str
