"""ORM models: internal object representation and db interaction."""

from sqlalchemy import (
    Column,
    String,
    Boolean,
    Float,
    SmallInteger,
    DateTime,
    JSON,
    Enum,
    CheckConstraint,
    ForeignKey
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Employee(Base):
    """Database model for employee.

    Attributes:
        employee_id (str): Unique identifier for the employee. Primary key, indexed.
        first_name (str): First name of the employee
        last_name (str): Last name of the employee
        gender (str): Gender of the employee
        email (str): Unique email address of the employee. Indexed.
        manager_email (str): Email of the employee's manager. Indexed.
        laptop (str): Laptop assigned to the employee
        monitor (bool): Whether the employee has a monitor
        headset (bool): Whether the employee has a headset
    """
    __tablename__ = "employee"

    employee_id = Column("EmployeeID", String, primary_key=True)
    first_name = Column("FirstName", String, nullable=False)
    last_name = Column("LastName", String, nullable=False)
    gender = Column("Gender", Enum("M", "F"))
    email = Column("Email", String, index=True, unique=True, nullable=False)
    manager_email = Column("ManagerEmail", String, index=True)
    laptop = Column("Laptop", String)
    monitor = Column("Monitor", Boolean)
    headset = Column("Headset", Boolean)

    info = relationship("EmployeeInfo", back_populates="employee")
    tasks = relationship("ITTask", back_populates="employee")


class EmployeeInfo(Base):
    """Database model for employee info.

    Attributes:
        employee_id (str): Foreign key referencing the employee. Primary key, indexed.
        department (str): Department the employee belongs to
        salary (str): Salary tier of the employee (e.g., "low", "medium", "high")
        active_projects (int): Number of active projects
        avg_monthly_hours (int): Average monthly hours worked
        years_at_company (int): Number of years at the company
        work_accidents (bool): Whether the employee has had a work accident
        received_promotion (bool): Whether the employee has received a promotion
        last_evaluation (float): Score of the last performance evaluation
        satisfaction_score (float): Employee satisfaction score
        attrition (bool): Whether the employee has left the company
        attrition_risk (float): Predicted probability of attrition
    """
    __tablename__ = "employee_info"

    employee_id = Column(
        "EmployeeID",
        String,
        ForeignKey("employee.EmployeeID"),
        primary_key=True,
        index=True,
    )
    department = Column(
        "Department",
        Enum(
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
        ),
        nullable=False
    )
    salary = Column("Salary", Enum("low", "medium", "high"))
    active_projects = Column("ActiveProjects", SmallInteger)
    avg_monthly_hours = Column("AvgMonthlyHours", SmallInteger)
    years_at_company = Column("YearsAtCompany", SmallInteger)
    work_accidents = Column("WorkAccidents", Boolean)
    received_promotion = Column("ReceivedPromotion", Boolean)
    last_evaluation = Column( # type: ignore
        "LastEvaluation",
        Float,
        CheckConstraint("LastEvaluation BETWEEN 0 AND 1")
    )
    satisfaction_score = Column( # type: ignore
        "SatisfactionScore",
        Float,
        CheckConstraint("SatisfactionScore BETWEEN 0 AND 1")
    )
    attrition = Column("Attrition", Boolean)
    attrition_risk = Column( # type: ignore
        "AttritionRisk",
        Float,
        CheckConstraint("AttritionRisk BETWEEN 0 AND 1")
    )

    employee = relationship("Employee", back_populates="info")


class ITTask(Base):
    """Database model for IT task.
    
    Attributes:
        task_id (str): Identifier for the task (e.g., "task_001"). Primary key
        employee_id (str): Foreign key referencing the employee. Indexed.
        title (str): Title of the task
        description (str): Detailed description of the task
        assignee (str): Email of the person or team assigned to the task
        due_date (DateTime | None): Optional due date for the task
        status (str): Current status of the task (e.g., "open", "in_progress", "closed")
        task_metadata (dict): Additional metadata related to the task
    """
    __tablename__ = "it_task"

    task_id = Column("TaskID", String, primary_key=True, index=True)
    employee_id = Column(
        "EmployeeID",
        String,
        ForeignKey("employee.EmployeeID"),
        index=True,
        nullable=False
    )
    title = Column("Title", String, nullable=False)
    description = Column("Description", String)
    assignee = Column("Assignee", String)
    due_date = Column("DueDate", DateTime)
    status = Column("Status", Enum("Pending", "Canceled", "Completed"))
    task_metadata = Column("Metadata", JSON)

    employee = relationship("Employee", back_populates="tasks")
