---
description: Rules for working in src/hr_hub/model/ (ORM layer, orm.py)
---

# Model Module Rules

`model/orm.py` contains the SQLAlchemy ORM definitions. This is the authoritative source of truth for the database schema.

## ORM conventions

- All ORM classes inherit from `Base` (`DeclarativeBase`) defined in `orm.py`.
- Table names use snake_case singular (`employee`, `employee_info`, `it_task`).
- Column names use PascalCase string aliases (e.g., `Column("EmployeeID", ...)`). The Python attribute name uses snake_case.
- Foreign keys reference the `<table>.<column alias>` string (e.g., `ForeignKey("employee.EmployeeID")`).
- `Enum` column values must be defined as explicit string literals in the `Column(...)` call.
- Float columns representing scores or probabilities (0–1 range) must include a `CheckConstraint`.

## Relationships

- Define bidirectional relationships with `relationship(..., back_populates=...)` on both sides.
- `Employee` is the parent; `EmployeeInfo` and `ITTask` are children.

## Exporting

Export ORM classes through `model/__init__.py`. Do not import from `model/orm.py` directly outside of `model/` and `alembic/env.py`.

## What does NOT belong here

- No Pydantic models — those live in `model/dto/`.
- No business logic or query helpers — those belong in `db/` or `service/`.
