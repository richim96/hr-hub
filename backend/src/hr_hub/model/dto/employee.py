"""Employee schema."""

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

    employee_id: str | None = Field(
        default=None, validation_alias="id", serialization_alias="id"
    )
    first_name: str
    last_name: str
    gender: str
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

    laptop: str
    monitor: bool
    headset: bool


class EmployeeInfoDTO(BaseModel):
    """
    """
    model_config = ConfigDict(from_attributes=True)

    department: str
