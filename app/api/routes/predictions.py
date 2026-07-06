from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.match import Match
from app.models.player import Player
from app.models.prediction_case import PredictionCase
from app.schemas.prediction_case import PredictionCaseCreate, PredictionCaseRead

router = APIRouter(prefix="/predictions", tags=["predictions"])


def determine_predicted_loser_id(match: Match, predicted_winner_id: int) -> int:
    if match.player_a_id is None or match.player_b_id is None:
        raise HTTPException(
            status_code=400,
            detail="Match must have both player_a_id and player_b_id before a prediction can be created.",
        )

    allowed_player_ids = {match.player_a_id, match.player_b_id}

    if predicted_winner_id not in allowed_player_ids:
        raise HTTPException(
            status_code=400,
            detail="predicted_winner_id must be player_a_id or player_b_id of the match.",
        )

    if predicted_winner_id == match.player_a_id:
        return match.player_b_id

    return match.player_a_id


@router.post("", response_model=PredictionCaseRead)
def create_prediction_case(payload: PredictionCaseCreate, db: Session = Depends(get_db)):
    match = db.get(Match, payload.match_id)

    if not match:
        raise HTTPException(status_code=404, detail="Match not found.")

    predicted_winner = db.get(Player, payload.predicted_winner_id)

    if not predicted_winner:
        raise HTTPException(status_code=404, detail="Predicted winner not found.")

    predicted_loser_id = determine_predicted_loser_id(
        match=match,
        predicted_winner_id=payload.predicted_winner_id,
    )

    prediction_case = PredictionCase(
        match_id=match.id,
        player_a_id=match.player_a_id,
        player_b_id=match.player_b_id,
        predicted_winner_id=payload.predicted_winner_id,
        predicted_loser_id=predicted_loser_id,
        decision_type=payload.decision_type,
        data_quality=payload.data_quality,
        prediction_integrity_score=payload.prediction_integrity_score,
        certification_status=payload.certification_status,
        main_reasons=payload.main_reasons,
        main_risks=payload.main_risks,
        strongest_counterargument=payload.strongest_counterargument,
        engine_summary=payload.engine_summary,
        conflict_summary=payload.conflict_summary,
        missing_data_summary=payload.missing_data_summary,
        source_summary=payload.source_summary,
        model_version=payload.model_version,
        rule_version=payload.rule_version,
        deployment_version=payload.deployment_version,
    )

    db.add(prediction_case)
    db.commit()
    db.refresh(prediction_case)

    return prediction_case


@router.get("", response_model=list[PredictionCaseRead])
def list_prediction_cases(db: Session = Depends(get_db)):
    prediction_cases = db.scalars(
        select(PredictionCase).order_by(PredictionCase.id)
    ).all()

    return prediction_cases


@router.get("/{prediction_id}", response_model=PredictionCaseRead)
def get_prediction_case(prediction_id: int, db: Session = Depends(get_db)):
    prediction_case = db.get(PredictionCase, prediction_id)

    if not prediction_case:
        raise HTTPException(status_code=404, detail="Prediction case not found.")

    return prediction_case
