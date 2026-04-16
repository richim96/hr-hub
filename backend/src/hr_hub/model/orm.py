"""ORM models: internal object representation and db interaction."""

from datetime import datetime, timezone
from typing import Any, Literal

from sqlalchemy import (
    CheckConstraint,
    Enum,
    ForeignKey,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean, DateTime, Float, JSON, SmallInteger


class Base(DeclarativeBase):
    pass


class Employee(Base):
    """Database model for employee.

    Attributes:
        employee_id (str): Unique identifier for the employee. Primary key.
        first_name (str): First name of the employee.
        last_name (str): Last name of the employee.
        gender (str | None): Gender of the employee.
        email (str): Unique email address of the employee. Indexed.
        manager_email (str | None): Email of the employee's manager. Null for the top-level employee. Indexed.
        laptop (str | None): Laptop model assigned to the employee.
        monitor (bool | None): Whether the employee has a monitor.
        headset (bool | None): Whether the employee has a headset.
    """
    __tablename__ = "employee"

    employee_id: Mapped[str] = mapped_column("EmployeeID", String, primary_key=True)
    first_name: Mapped[str] = mapped_column("FirstName", String, nullable=False)
    last_name: Mapped[str] = mapped_column("LastName", String, nullable=False)
    gender: Mapped[Literal["M", "F"] | None] = mapped_column("Gender", Enum("M", "F"))
    email: Mapped[str] = mapped_column("Email", String, index=True, unique=True, nullable=False)
    manager_email: Mapped[str | None] = mapped_column("ManagerEmail", String, index=True)
    laptop: Mapped[str | None] = mapped_column("Laptop", String)
    monitor: Mapped[bool | None] = mapped_column("Monitor", Boolean)
    headset: Mapped[bool | None] = mapped_column("Headset", Boolean)

    info: Mapped[list["EmployeeInfo"]] = relationship("EmployeeInfo", back_populates="employee")
    tasks: Mapped[list["ITTask"]] = relationship("ITTask", back_populates="employee")


class EmployeeInfo(Base):
    """Database model for employee info.

    Attributes:
        employee_id (str): Foreign key referencing the employee. Primary key, indexed.
        department (str): Department the employee belongs to.
        salary (str | None): Salary tier of the employee — "low", "medium", or "high".
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
    __tablename__ = "employee_info"

    employee_id: Mapped[str] = mapped_column(
        "EmployeeID",
        String,
        ForeignKey("employee.EmployeeID"),
        primary_key=True,
        index=True,
    )
    department: Mapped[Literal[
        "accounting", "engineering", "hr", "IT", "management",
        "marketing", "product_management", "r&d", "sales", "support",
    ]] = mapped_column(
        "Department",
        Enum(
            "accounting", "engineering", "hr", "IT", "management",
            "marketing", "product_management", "r&d", "sales", "support",
        ),
        nullable=False,
    )
    salary: Mapped[Literal["low", "medium", "high"]] = mapped_column("Salary", Enum("low", "medium", "high"))
    active_projects: Mapped[int | None] = mapped_column("ActiveProjects", SmallInteger)
    avg_monthly_hours: Mapped[int | None] = mapped_column("AvgMonthlyHours", SmallInteger)
    years_at_company: Mapped[int | None] = mapped_column("YearsAtCompany", SmallInteger)
    work_accidents: Mapped[bool | None] = mapped_column("WorkAccidents", Boolean)
    received_promotion: Mapped[bool | None] = mapped_column("ReceivedPromotion", Boolean)
    last_evaluation: Mapped[float | None] = mapped_column(
        "LastEvaluation",
        Float,
        CheckConstraint("LastEvaluation BETWEEN 0 AND 1"),
    )
    satisfaction_score: Mapped[float | None] = mapped_column(
        "SatisfactionScore",
        Float,
        CheckConstraint("SatisfactionScore BETWEEN 0 AND 1"),
    )
    attrition: Mapped[bool | None] = mapped_column("Attrition", Boolean)
    attrition_risk: Mapped[float | None] = mapped_column(
        "AttritionRisk",
        Float,
        CheckConstraint("AttritionRisk BETWEEN 0 AND 1"),
    )

    employee: Mapped["Employee"] = relationship("Employee", back_populates="info")


class ITTask(Base):
    """Database model for IT task.

    Attributes:
        task_id (str): Identifier for the task. Primary key, indexed.
        employee_id (str): Foreign key referencing the employee. Indexed.
        employee_email (str | None): Email address of the employee.
        title (str): Title of the task.
        description (str | None): Detailed description of the task.
        assignee (str | None): Email of the person or team assigned to the task.
        due_date (datetime | None): Optional due date for the task.
        status (str | None): Current status — "Pending", "Completed", or "Canceled".
        task_metadata (dict[str, Any] | None): Additional metadata related to the task.
    """
    __tablename__ = "it_task"

    task_id: Mapped[str] = mapped_column("TaskID", String, primary_key=True, index=True)
    employee_id: Mapped[str] = mapped_column(
        "EmployeeID",
        String,
        ForeignKey("employee.EmployeeID"),
        index=True,
        nullable=False,
    )
    employee_email: Mapped[str | None] = mapped_column("EmployeeEmail", String, index=True)
    title: Mapped[str] = mapped_column("Title", String, nullable=False)
    description: Mapped[str | None] = mapped_column("Description", String)
    assignee: Mapped[str | None] = mapped_column("Assignee", String)
    due_date: Mapped[datetime | None] = mapped_column("DueDate", DateTime)
    status: Mapped[Literal["Pending", "Canceled", "Completed"] | None] = mapped_column("Status", Enum("Pending", "Canceled", "Completed"))
    task_metadata: Mapped[dict[str, Any] | None] = mapped_column("Metadata", JSON)

    employee: Mapped["Employee"] = relationship("Employee", back_populates="tasks")


class Ticket(Base):
    """Database model for people-team tickets.

    Attributes:
        request_id (str): Unique identifier for the ticket. Primary key.
        request_type (str): Always ``"people_ticket"``.
        status (str): Processing status — one of ``"completed"``, ``"pending"``, ``"failed"``.
        submitted_by (str): Email of the person who submitted the ticket. Indexed.
        subject (str): Subject line of the ticket.
        text (str): Full description of the ticket issue.
        actions (list[dict[str, Any]]): JSON-serialized list of Action dicts from the processing workflow.
        llm_result (dict[str, Any] | None): JSON-serialized LLMResult, populated once the agent runs.
        created_at (datetime): UTC timestamp when the ticket was created.
    """
    __tablename__ = "ticket"

    request_id: Mapped[str] = mapped_column("RequestID", String, primary_key=True)
    request_type: Mapped[str] = mapped_column("RequestType", String, nullable=False)
    status: Mapped[Literal["completed", "pending", "failed"]] = mapped_column(
        "Status",
        Enum("completed", "pending", "failed"),
        nullable=False,
    )
    submitted_by: Mapped[str] = mapped_column("SubmittedBy", String, index=True, nullable=False)
    subject: Mapped[str] = mapped_column("Subject", String, nullable=False)
    text: Mapped[str] = mapped_column("Text", String, nullable=False)
    actions: Mapped[list[dict[str, Any]]] = mapped_column("Actions", JSON, nullable=False)
    llm_result: Mapped[dict[str, Any] | None] = mapped_column("LLMResult", JSON)
    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt", DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
