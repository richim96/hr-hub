"""Attrition prediction service.

The SOTA gradient-boosted pipeline is loaded once at application startup
via `load_model()` and cached on ``app.state``. All inference requests receive
the pipeline via dependency injection.
"""

import os
from typing import Any

import joblib
import pandas as pd
from fastapi import Request
from sqlalchemy.orm import Session

from hr_hub.model import EmployeeInfo
from hr_hub.model.dto import APIResponseDTO, AttritionFeaturesDTO
from hr_hub.service import LOGGER


_SALARY_ENCODING: dict[str, float] = {"low": 0., "medium": 0.5, "high": 1.}
_DEFAULTS: dict[str, Any] = {
    "ActiveProjects": 1,
    "AvgMonthlyHours": 160,
    "YearsAtCompany": 1,
    "WorkAccidents": 0,
    "ReceivedPromotion": 0,
    "LastEvaluation": 0.75,
    "SatisfactionScore": 0.75,
} # Base data for new employees used as fallback on null input


def get_attrition_model(request: Request) -> Any | None:
    """FastAPI dependency that returns the cached attrition prediction pipeline.

    Reads the attrition model stored on ``app.state.attrition_model`` at startup.
    Returns ``None`` if the model was not loaded (e.g. ``SOTA_PATH`` unset or
    file missing); service functions receiving ``None`` return a failure response.

    Usage::

        @router.post("/score")
        def handler(attrition_model: Any | None = Depends(get_attrition_model)):
            ...

    Args:
        request (Request): The incoming FastAPI request (used to reach ``app.state``).
    """
    return request.app.state.attrition_model


def load_model() -> Any | None:
    """Load the attrition pipeline from SOTA_PATH and return it.

    Called once during application startup (lifespan in main.py); the result
    is stored on ``app.state.attrition_model``.
    """
    model_path = os.getenv("SOTA_PATH")
    if not model_path:
        LOGGER.warning("SOTA_PATH is not set; attrition modal unavailable.")
        return None

    try:
        attrition_model: Any = joblib.load(model_path)
        LOGGER.info(f"Attrition model loaded from {model_path}")
        return attrition_model
    except Exception as e:
        LOGGER.error(f"Failed to load attrition model from {model_path}: {e}")
        return None


# ---------------------------------------------------------------------------
# Public service functions
# ---------------------------------------------------------------------------

def score_employee(
    employee_id: str,
    session: Session,
    attrition_model: Any | None,
) -> APIResponseDTO.Action:
    """Score an existing employee and persist the updated attrition_risk to the DB.

    Fetches the employee's ``EmployeeInfo`` row, runs the attrition model,
    and writes the resulting risk score back to the database.

    Args:
        employee_id (str): Primary key of the employee to score.
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.
        attrition_model (Any | None): Loaded sklearn Pipeline from ``app.state``.
    """
    if attrition_model is None:
        return _action(False, "Prediction model is not available. Check path config.")

    try:
        info: EmployeeInfo | None = (
            session.query(EmployeeInfo)
            .filter(EmployeeInfo.employee_id == employee_id)
            .first()
        )
    except Exception as e:
        LOGGER.error(f"DB error fetching EmployeeInfo for {employee_id}: {e}")
        return _action(False, f"Database error: {e}")

    if info is None:
        return _action(False, f"Employee {employee_id!r} not found.")
    
    features = AttritionFeaturesDTO(
        department=info.department,
        salary=info.salary,
        active_projects=info.active_projects,
        avg_monthly_hours=info.avg_monthly_hours,
        years_at_company=info.years_at_company,
        work_accidents=info.work_accidents,
        received_promotion=info.received_promotion,
        last_evaluation=info.last_evaluation,
        satisfaction_score=info.satisfaction_score,
    )

    try:
        risk = _run_inference(features, attrition_model)
    except Exception as e:
        LOGGER.error(f"Inference failed for employee {employee_id}: {e}")
        return _action(False, f"Inference error: {e}")

    try:
        info.attrition_risk = risk
        session.flush()
    except Exception as e:
        LOGGER.error(f"Could not persist attrition_risk for {employee_id}: {e}")
        return _action(False, f"Could not save attrition risk: {e}")

    LOGGER.info(f"Scored employee {employee_id}: risk={risk:.4f}")
    return _action(True, f"Attrition risk for {employee_id} persisted: {risk:.4f}.")


def score_all(
    session: Session,
    request_id: str,
    attrition_model: Any | None,
) -> APIResponseDTO:
    """Score attrition risk for all current employees.

    Employees with ``attrition == True`` are excluded — they have already left
    and their risk score is not actionable.  All remaining employees are fetched
    in a single query and scored in one vectorized attrition model call, then their
    ``attrition_risk`` columns are updated in bulk before a single flush.

    Args:
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.
        request_id (str): Identifier to embed in the response envelope.
        attrition_model (Any | None): Loaded sklearn Pipeline from ``app.state``.
    """
    if attrition_model is None:
        return _response(request_id, "Prediction model could not be loaded", False)

    # ------------------------------------------------------------------
    # 1. Fetch current employees only (attrition is False or unset).
    # ------------------------------------------------------------------
    try:
        rows: list[EmployeeInfo] = (
            session.query(EmployeeInfo)
            .filter(EmployeeInfo.attrition.isnot(True))
            .all()
        )
    except Exception as e:
        LOGGER.error(f"DB error fetching employees for batch scoring [{request_id}]: {e}")
        return _response(request_id, f"Database error: {e}", False)

    if not rows:
        return _response(request_id, "No current employees found to score.", False)

    # ------------------------------------------------------------------
    # 2. Build a multi-row DataFrame and run vectorized inference.
    # ------------------------------------------------------------------
    try:
        records: list[dict[str, Any]] = [
            {
                "Department": row.department,
                "Salary": _SALARY_ENCODING[row.salary],
                "ActiveProjects": row.active_projects if row.active_projects is not None else _DEFAULTS["ActiveProjects"],
                "AvgMonthlyHours": row.avg_monthly_hours if row.avg_monthly_hours is not None else _DEFAULTS["AvgMonthlyHours"],
                "YearsAtCompany": row.years_at_company if row.years_at_company is not None else _DEFAULTS["YearsAtCompany"],
                "WorkAccidents": row.work_accidents if row.work_accidents is not None else _DEFAULTS["WorkAccidents"],
                "ReceivedPromotion": row.received_promotion if row.received_promotion is not None else _DEFAULTS["ReceivedPromotion"],
                "LastEvaluation": row.last_evaluation if row.last_evaluation is not None else _DEFAULTS["LastEvaluation"],
                "SatisfactionScore": row.satisfaction_score if row.satisfaction_score is not None else _DEFAULTS["SatisfactionScore"],
            }
            for row in rows
        ]
        df = pd.DataFrame(records)
        # pandas 3.x infers Arrow-backed StringDtype for string columns, which
        # scikit-learn's transformers cannot handle — cast to object explicitly.
        df["Department"] = df["Department"].astype(object)
        probabilities: list[float] = [
            float(p).__round__(4) for p in attrition_model.predict_proba(df)[:, 1]
        ]
    except Exception as e:
        LOGGER.error(f"Batch inference failed [{request_id}]: {e}")
        return _response(request_id, f"Inference error: {e}", False)

    # ------------------------------------------------------------------
    # 3. Persist updated risk scores.
    # ------------------------------------------------------------------
    try:
        for row, risk in zip(rows, probabilities):
            row.attrition_risk = risk
        session.flush()
    except Exception as e:
        LOGGER.error(f"Could not persist batch attrition scores [{request_id}]: {e}")
        return _response(request_id, f"Could not save attrition scores: {e}", False)

    LOGGER.info(f"Full employee scoring complete [{request_id}].")
    return _response(request_id, f"Attrition risk persisted for all employees", True)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _run_inference(features: AttritionFeaturesDTO, attrition_model: Any) -> float:
    """Build a single-row feature DataFrame and return the predicted attrition probability.

    Args:
        features (AttritionFeaturesDTO): Employee features to score.
        attrition_model (Any): Loaded sklearn Pipeline.
    """
    df = pd.DataFrame([{
        "Department": features.department,
        "Salary": _SALARY_ENCODING[features.salary],
        "ActiveProjects": features.active_projects if features.active_projects is not None else _DEFAULTS["ActiveProjects"],
        "AvgMonthlyHours": features.avg_monthly_hours if features.avg_monthly_hours is not None else _DEFAULTS["AvgMonthlyHours"],
        "YearsAtCompany": features.years_at_company if features.years_at_company is not None else _DEFAULTS["YearsAtCompany"],
        "WorkAccidents": int(features.work_accidents) if features.work_accidents is not None else _DEFAULTS["WorkAccidents"],
        "ReceivedPromotion": int(features.received_promotion) if features.received_promotion is not None else _DEFAULTS["ReceivedPromotion"],
        "LastEvaluation": features.last_evaluation if features.last_evaluation is not None else _DEFAULTS["LastEvaluation"],
        "SatisfactionScore": features.satisfaction_score if features.satisfaction_score is not None else _DEFAULTS["SatisfactionScore"],
    }])

    return float(attrition_model.predict_proba(df)[0, 1]).__round__(4)


def _action(success: bool, msg: str) -> APIResponseDTO.Action:
    """Helper to build a standardized APIResponseDTO.Action.
    
    Args:
        success (bool): Whether the action succeeded or failed.
        message (str): Detail message to include in the action details.
    """
    return APIResponseDTO.Action(action="score_attrition", success=success, details=msg)


def _response(request_id: str, message: str, success: bool) -> APIResponseDTO:
    """Helper to build a standardized APIResponseDTO.

    Args:
        request_id (str): Identifier to embed in the response envelope.
        message (str): Detail message to include in the action details.
        success (bool): Whether the action succeeded or failed.
    """
    return APIResponseDTO(
        request_id=request_id,
        request_type="prediction",
        status="completed" if success else "failed",
        actions=[_action(success, message)],
    )
