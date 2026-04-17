"""Attrition prediction service."""

import os
from typing import Any

import joblib # pyright: ignore[reportMissingTypeStubs]
import pandas as pd
from fastapi import Request
from sqlalchemy.orm import Session

from hr_hub.model import EmployeeInfo
from hr_hub.model.dto import APIResponse, AttritionFeaturesDTO
from hr_hub.service import LOGGER


_SALARY_ENCODING: dict[str, float] = {"low": 0., "medium": 0.5, "high": 1.}
_DEFAULTS: dict[str, Any] = {
    "ActiveProjects": 1,
    "AvgMonthlyHours": 160,
    "YearsAtCompany": 0,
    "WorkAccidents": 0,
    "ReceivedPromotion": 0,
    "LastEvaluation": 0.75,
    "SatisfactionScore": 0.75,
}


def get_attrition_model(request: Request) -> Any | None:
    """FastAPI dependency that returns the cached attrition prediction pipeline.

    Usage::

        @router.post("/score")
        def handler(attrition_model: Any | None = Depends(get_attrition_model)):
            ...

    Args:
        request (Request): The incoming FastAPI request (used to reach ``app.state``).
    """
    return request.app.state.attrition_model


def load_model() -> Any | None:
    """Load the attrition pipeline from SOTA_PATH and return it."""
    model_path = os.getenv("SOTA_PATH")
    if not model_path:
        LOGGER.warning("SOTA_PATH is not set; attrition modal unavailable.")
        return None

    try:
        attrition_model: Any = joblib.load(model_path) # pyright: ignore[reportUnknownMemberType]
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
) -> APIResponse.Action:
    """Score an existing employee and persist the updated attrition_risk to the DB.

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
) -> APIResponse:
    """Score attrition risk for all current employees (`attrition == False`)

    Args:
        session (Session): Active SQLAlchemy session. Caller owns commit/rollback.
        request_id (str): Identifier to embed in the response envelope.
        attrition_model (Any | None): Loaded sklearn Pipeline from ``app.state``.
    """
    if attrition_model is None:
        return _response(request_id, "Prediction model could not be loaded", False)

    try: # fetch employees
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

    try: # run model inference
        df: pd.DataFrame = pd.DataFrame([
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
            } for row in rows
        ])
        df["Department"] = df["Department"].astype(object) # scikit-learn's transformers cannot handle StringDtype from pandas 3.x.
        probabilities: list[float] = [
            float(p).__round__(4) for p in attrition_model.predict_proba(df)[:, 1]
        ]
    except Exception as e:
        LOGGER.error(f"Batch inference failed [{request_id}]: {e}")
        return _response(request_id, f"Inference error: {e}", False)

    try: # persist scores
        for row, risk in zip(rows, probabilities):
            row.attrition_risk = risk
        session.flush()
    except Exception as e:
        LOGGER.error(f"Could not persist batch attrition scores [{request_id}]: {e}")
        return _response(request_id, f"Could not save attrition scores: {e}", False)

    LOGGER.info(f"Full employee scoring complete [{request_id}].")
    return _response(request_id, f"Attrition risk persisted for all employees", True)


# ---------------------------------------------------------------------------
# Private functions
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


def _action(success: bool, msg: str) -> APIResponse.Action:
    """Helper to build a standardized APIResponseDTO.Action.
    
    Args:
        success (bool): Whether the action succeeded or failed.
        message (str): Detail message to include in the action details.
    """
    return APIResponse.Action(action="score_attrition", success=success, details=msg)


def _response(request_id: str, message: str, success: bool) -> APIResponse:
    """Helper to build a standardized APIResponseDTO.

    Args:
        request_id (str): Identifier to embed in the response envelope.
        message (str): Detail message to include in the action details.
        success (bool): Whether the action succeeded or failed.
    """
    return APIResponse(
        request_id=request_id,
        request_type="prediction",
        status="Completed" if success else "Canceled",
        actions=[_action(success, message)],
    )
