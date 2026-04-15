"""API connecting to the attrition prediction model."""

from typing import Any

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from hr_hub.api import LOGGER
from hr_hub.db import get_session
from hr_hub.model.dto import ScoreAllAttritionRequest, APIResponseDTO
from hr_hub.service.prediction import score_all_employees, get_attrition_model


prediction_router: APIRouter = APIRouter(prefix="/prediction", tags=["Prediction"])


@prediction_router.post("/attrition/score-all", response_model=APIResponseDTO)
async def predict_all_attrition(
    request: ScoreAllAttritionRequest,
    session: Session = Depends(get_session),
    attrition_model: Any | None = Depends(get_attrition_model),
) -> APIResponseDTO:
    """Re-score attrition risk for all current (non-attrited) employees.

    Employees who have already left (``attrition == True``) are skipped.

    Args:
        request (ScoreAllRequestDTO): Score-all request carrying the trace identifier.
        session (Session): SQLAlchemy session — injected by FastAPI.
        attrition_model (Any | None): Attrition prediction model — injected by FastAPI.
    """
    LOGGER.info(f"Score-all attrition request [ {request.request_id} ]")
    return score_all_employees(session, request.request_id, attrition_model)
