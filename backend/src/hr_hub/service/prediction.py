"""Attrition prediction service.

The SOTA gradient-boosted pipeline (trained in
notebooks/employee_attrition/train_attrition_model.py) is loaded once at
application startup via `load_model()` and cached on ``app.state``.  All
inference requests receive the pipeline via dependency injection — no
module-level globals, no file I/O at request time.

Feature order and encoding MUST match the pipeline produced by the training
script.  The ColumnTransformer inside the pipeline handles all preprocessing,
so this module only needs to assemble a single-row DataFrame with the correct
column names.
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


# Minimum data for new employees used as fallback on null input
_FEATURE_DEFAULTS: dict[str, Any] = {
    "ActiveProjects": 1,
    "AvgMonthlyHours": 160,
    "YearsAtCompany": 1,
    "WorkAccidents": 0,
    "ReceivedPromotion": 0,
    "LastEvaluation": 0.75,
    "SatisfactionScore": 0.75,
}

_SALARY_ENCODING: dict[str, float] = {
    "low": 0.,
    "medium": 0.5,
    "high": 1.,
}


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

    Returns:
        Any | None: The loaded sklearn Pipeline, or None if unavailable.
    """
    return request.app.state.attrition_model


def load_model() -> Any | None:
    """Load the attrition pipeline from SOTA_PATH and return it.

    Called once during application startup (lifespan in main.py); the result
    is stored on ``app.state.attrition_model``.  Returns ``None`` if the
    env var is unset or the file is missing — requests will then return a 503.

    Returns:
        Any | None: The loaded sklearn Pipeline, or None on failure.
    """
    model_path = os.getenv("SOTA_PATH")
    if not model_path:
        LOGGER.warning("SOTA_PATH is not set; attrition prediction unavailable.")
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
        attrition_model (Any | None): Loaded sklearn Pipeline from ``app.state``. None produces a failure action.

    Returns:
        APIResponseDTO.Action: Action indicating success or failure of the scoring step.
    """
    if attrition_model is None:
        return APIResponseDTO.Action(
            action="score_attrition",
            success=False,
            details="Prediction model is not available. Check SOTA_PATH configuration.",
        )

    try:
        info: EmployeeInfo | None = (
            session.query(EmployeeInfo)
            .filter(EmployeeInfo.employee_id == employee_id)
            .first()
        )
    except Exception as e:
        LOGGER.error(f"DB error fetching EmployeeInfo for {employee_id}: {e}")
        return APIResponseDTO.Action(
            action="score_attrition",
            success=False,
            details=f"Database error: {e}",
        )

    if info is None:
        return APIResponseDTO.Action(
            action="score_attrition",
            success=False,
            details=f"Employee {employee_id!r} not found.",
        )

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
        return APIResponseDTO.Action(
            action="score_attrition",
            success=False,
            details=f"Inference error: {e}",
        )

    try:
        info.attrition_risk = risk
        session.flush()
    except Exception as e:
        LOGGER.error(f"Could not persist attrition_risk for {employee_id}: {e}")
        return APIResponseDTO.Action(
            action="score_attrition",
            success=False,
            details=f"Could not save attrition risk: {e}",
        )

    LOGGER.info(f"Scored employee {employee_id}: risk={risk:.4f}")
    return APIResponseDTO.Action(
        action="score_attrition",
        success=True,
        details=f"Attrition risk for {employee_id} persisted: {risk:.4f}.",
    )


def score_all_employees(
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
        attrition_model (Any | None): Loaded sklearn Pipeline from ``app.state``. None triggers a 503-style failure response.

    Returns:
        APIResponseDTO: Summary ``score_attrition`` action and
        ``batch_attrition_results`` containing one entry per scored employee.
    """
    if attrition_model is None:
        return _unavailable_response(request_id)

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
        return _error_response(request_id, f"Database error: {e}")

    if not rows:
        return _error_response(request_id, "No current employees found to score.")

    # ------------------------------------------------------------------
    # 2. Build a multi-row DataFrame and run vectorized inference.
    # ------------------------------------------------------------------
    try:
        records: list[dict[str, Any]] = [
            {
                "Department": row.department,
                "Salary": _SALARY_ENCODING[row.salary],
                "ActiveProjects": int(row.active_projects) if row.active_projects is not None else _FEATURE_DEFAULTS["ActiveProjects"],
                "AvgMonthlyHours": int(row.avg_monthly_hours) if row.avg_monthly_hours is not None else _FEATURE_DEFAULTS["AvgMonthlyHours"],
                "YearsAtCompany": int(row.years_at_company) if row.years_at_company is not None else _FEATURE_DEFAULTS["YearsAtCompany"],
                "WorkAccidents": int(row.work_accidents) if row.work_accidents is not None else _FEATURE_DEFAULTS["WorkAccidents"],
                "ReceivedPromotion": int(row.received_promotion) if row.received_promotion is not None else _FEATURE_DEFAULTS["ReceivedPromotion"],
                "LastEvaluation": float(row.last_evaluation) if row.last_evaluation is not None else _FEATURE_DEFAULTS["LastEvaluation"],
                "SatisfactionScore": float(row.satisfaction_score) if row.satisfaction_score is not None else _FEATURE_DEFAULTS["SatisfactionScore"],
            }
            for row in rows
        ]
        df = pd.DataFrame(records)
        # pandas 3.x infers Arrow-backed StringDtype for string columns, which
        # scikit-learn's transformers cannot handle — cast to object explicitly.
        df["Department"] = df["Department"].astype(object)
        probabilities: list[float] = [
            round(float(p), 4) for p in attrition_model.predict_proba(df)[:, 1]
        ]
    except Exception as e:
        LOGGER.error(f"Batch inference failed [{request_id}]: {e}")
        return _error_response(request_id, f"Inference error: {e}")

    # ------------------------------------------------------------------
    # 3. Persist updated risk scores.
    # ------------------------------------------------------------------
    try:
        for row, risk in zip(rows, probabilities):
            row.attrition_risk = risk
        session.flush()
    except Exception as e:
        LOGGER.error(f"Could not persist batch attrition scores [{request_id}]: {e}")
        return _error_response(request_id, f"Could not save attrition scores: {e}")

    scored = len(rows)
    LOGGER.info(f"Batch scoring complete [{request_id}]: {scored} employees scored")

    return APIResponseDTO(
        request_id=request_id,
        request_type="prediction",
        status="completed",
        actions=[
            APIResponseDTO.Action(
                action="score_attrition",
                success=True,
                details=f"Attrition risk persisted for {scored} employee(s).",
            )
        ],
    )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _run_inference(features: AttritionFeaturesDTO, pipeline: Any) -> float:
    """Build a single-row feature DataFrame and return the predicted attrition probability.

    Args:
        features (AttritionFeaturesDTO): Employee features to score.
        pipeline (Any): Loaded sklearn Pipeline.

    Returns:
        float: Predicted attrition probability rounded to 4 decimal places.
    """
    row: dict[str, Any] = {
        "Department": features.department,
        "Salary": _SALARY_ENCODING[features.salary],
        "ActiveProjects": (
            features.active_projects
            if features.active_projects is not None
            else _FEATURE_DEFAULTS["ActiveProjects"]
        ),
        "AvgMonthlyHours": (
            features.avg_monthly_hours
            if features.avg_monthly_hours is not None
            else _FEATURE_DEFAULTS["AvgMonthlyHours"]
        ),
        "YearsAtCompany": (
            features.years_at_company
            if features.years_at_company is not None
            else _FEATURE_DEFAULTS["YearsAtCompany"]
        ),
        "WorkAccidents": (
            int(features.work_accidents)
            if features.work_accidents is not None
            else _FEATURE_DEFAULTS["WorkAccidents"]
        ),
        "ReceivedPromotion": (
            int(features.received_promotion)
            if features.received_promotion is not None
            else _FEATURE_DEFAULTS["ReceivedPromotion"]
        ),
        "LastEvaluation": (
            features.last_evaluation
            if features.last_evaluation is not None
            else _FEATURE_DEFAULTS["LastEvaluation"]
        ),
        "SatisfactionScore": (
            features.satisfaction_score
            if features.satisfaction_score is not None
            else _FEATURE_DEFAULTS["SatisfactionScore"]
        ),
    }

    df = pd.DataFrame([row])
    prob: float = float(pipeline.predict_proba(df)[0, 1])
    return round(prob, 4)


def _unavailable_response(request_id: str) -> APIResponseDTO:
    return APIResponseDTO(
        request_id=request_id,
        request_type="prediction",
        status="failed",
        actions=[
            APIResponseDTO.Action(
                action="score_attrition",
                success=False,
                details="Prediction model is not available. Check SOTA_PATH configuration.",
            )
        ],
    )


def _error_response(request_id: str, message: str) -> APIResponseDTO:
    return APIResponseDTO(
        request_id=request_id,
        request_type="prediction",
        status="failed",
        actions=[
            APIResponseDTO.Action(
                action="score_attrition",
                success=False,
                details=message,
            )
        ],
    )
