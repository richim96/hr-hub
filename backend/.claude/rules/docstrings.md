---
description: Docstring style rules for all Python modules in this project
---

# Docstring Rules

This project uses **Google-style docstrings** throughout. The rules below apply to every function, method, and class.

## Format

```python
def some_function(employee_id: str, session: Session) -> APIResponseDTO:
    """One-line summary.

    Optional extended description that explains context, caveats, or
    multi-step behaviour.

    Args:
        employee_id (str): Primary key of the employee to look up.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.

    Returns:
        APIResponseDTO: Status and per-step actions describing what happened.

    Raises:
        RuntimeError: If a required environment variable is missing.
    """
```

## Rules

### Types are mandatory for every argument and attribute

Every entry in `Args:`, `Attributes:`, `Yields:`, and `Returns:` **must** include the type in parentheses immediately after the name:

```
name (type): description
```

Never omit the type:

```python
# Wrong — missing type
employee_id: Primary key of the employee.

# Correct
employee_id (str): Primary key of the employee.
```

This applies even when the type is already visible in the function signature or class body — the docstring is the canonical human-readable contract.

### Use exact types, not aliases or synonyms

The type must match the actual Python type used in the signature or field definition:

- Use `NewHireRequestDTO`, not `NewHireRequest` or `NewHireEvent`.
- Use `APIResponseDTO.Action`, not `Action`.
- Use `list[str] | None`, not `Optional[list[str]]`.
- For complex `Literal` types, write them out in full: `Literal["low", "medium", "high"]`.

### Returns section

Document the return value with its type:

```python
Returns:
    APIResponseDTO: Status and per-step actions describing what happened.
```

For generator functions, use `Yields:` instead of `Returns:`.

### Raises section

Document only exceptions that are deliberately raised by the function (not every possible exception). Omit the section entirely if the function does not raise.

### One-liners

Functions with obvious behaviour and no arguments worth documenting may use a single-line docstring without sections:

```python
def is_model_loaded() -> bool:
    """Return True if the prediction pipeline is available."""
```
