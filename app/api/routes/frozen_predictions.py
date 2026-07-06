import hashlib
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.evidence_ledger import EvidenceLedger
from app.models.frozen_prediction import FrozenPrediction
from app.models.match import Match
from app.models.prediction_case import PredictionCase
from app.schemas.frozen_prediction import FrozenPredictionRead

router = APIRouter(tags=["frozen-predictions"])


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def build_frozen_payload(
    prediction_case: PredictionCase,
    match: Match,
    evidence_items: list[EvidenceLedger],
    freeze_timestamp: datetime,
) -> dict:
    return {
        "freeze_version": "freeze-v1",
        "frozen_at": freeze_timestamp.isoformat(),
        "prediction_case": {
            "id": prediction_case.id,
            "match_id": prediction_case.match_id,
            "player_a_id": prediction_case.player_a_id,
            "player_b_id": prediction_case.player_b_id,
            "predicted_winner_id": prediction_case.predicted_winner_id,
            "predicted_loser_id": prediction_case.predicted_loser_id,
            "decision_type": prediction_case.decision_type,
            "data_quality": prediction_case.data_quality,
            "prediction_integrity_score": prediction_case.prediction_integrity_score,
            "certification_status": prediction_case.certification_status,
            "main_reasons": prediction_case.main_reasons,
            "main_risks": prediction_case.main_risks,
            "strongest_counterargument": prediction_case.strongest_counterargument,
            "engine_summary": prediction_case.engine_summary,
            "conflict_summary": prediction_case.conflict_summary,
            "missing_data_summary": prediction_case.missing_data_summary,
            "source_summary": prediction_case.source_summary,
            "model_version": prediction_case.model_version,
            "rule_version": prediction_case.rule_version,
            "deployment_version": prediction_case.deployment_version,
            "created_at": prediction_case.created_at.isoformat() if prediction_case.created_at else None,
        },
        "match": {
            "id": match.id,
            "external_match_id": match.external_match_id,
            "tournament_name": match.tournament_name,
            "round": match.round,
            "surface": match.surface,
            "scheduled_start_time": match.scheduled_start_time.isoformat() if match.scheduled_start_time else None,
            "timezone": match.timezone,
            "player_a_id": match.player_a_id,
            "player_b_id": match.player_b_id,
            "winner_id": match.winner_id,
            "match_status": match.match_status,
            "created_at": match.created_at.isoformat() if match.created_at else None,
        },
        "evidence": [
            {
                "id": evidence.id,
                "evidence_id": evidence.evidence_id,
                "match_id": evidence.match_id,
                "player_id": evidence.player_id,
                "source_id": evidence.source_id,
                "fact_type": evidence.fact_type,
                "fact_value": evidence.fact_value,
                "unit": evidence.unit,
                "time_window": evidence.time_window,
                "retrieved_at": evidence.retrieved_at.isoformat() if evidence.retrieved_at else None,
                "published_at": evidence.published_at.isoformat() if evidence.published_at else None,
                "valid_from": evidence.valid_from.isoformat() if evidence.valid_from else None,
                "valid_until": evidence.valid_until.isoformat() if evidence.valid_until else None,
                "confidence_level": evidence.confidence_level,
                "used_by_engine": evidence.used_by_engine,
                "effect_direction": evidence.effect_direction,
                "effect_strength": evidence.effect_strength,
                "fact_status": evidence.fact_status,
                "rejection_reason": evidence.rejection_reason,
                "notes": evidence.notes,
                "created_at": evidence.created_at.isoformat() if evidence.created_at else None,
            }
            for evidence in evidence_items
        ],
    }


def canonical_json(payload: dict) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def sha256_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@router.post("/predictions/{prediction_id}/freeze", response_model=FrozenPredictionRead)
def freeze_prediction(prediction_id: int, db: Session = Depends(get_db)):
    prediction_case = db.get(PredictionCase, prediction_id)

    if not prediction_case:
        raise HTTPException(status_code=404, detail="Prediction case not found.")

    existing_frozen_prediction = db.scalars(
        select(FrozenPrediction).where(FrozenPrediction.prediction_case_id == prediction_case.id)
    ).first()

    if existing_frozen_prediction:
        raise HTTPException(
            status_code=400,
            detail="Prediction case is already frozen.",
        )

    match = db.get(Match, prediction_case.match_id)

    if not match:
        raise HTTPException(status_code=404, detail="Match not found.")

    freeze_timestamp = utc_now()

    if match.scheduled_start_time is not None:
        scheduled_start_time = match.scheduled_start_time

        if scheduled_start_time.tzinfo is None:
            scheduled_start_time = scheduled_start_time.replace(tzinfo=timezone.utc)

        if freeze_timestamp >= scheduled_start_time:
            raise HTTPException(
                status_code=400,
                detail="Prediction cannot be frozen after scheduled match start time.",
            )

    allowed_player_ids = {match.player_a_id, match.player_b_id}

    if prediction_case.predicted_winner_id not in allowed_player_ids:
        raise HTTPException(
            status_code=400,
            detail="Predicted winner is not part of the match.",
        )

    if prediction_case.predicted_loser_id not in allowed_player_ids:
        raise HTTPException(
            status_code=400,
            detail="Predicted loser is not part of the match.",
        )

    if prediction_case.predicted_winner_id == prediction_case.predicted_loser_id:
        raise HTTPException(
            status_code=400,
            detail="Predicted winner and loser must be different.",
        )

    evidence_items = db.scalars(
        select(EvidenceLedger)
        .where(EvidenceLedger.match_id == match.id)
        .order_by(EvidenceLedger.id)
    ).all()

    for evidence in evidence_items:
        if evidence.retrieved_at is not None:
            retrieved_at = evidence.retrieved_at

            if retrieved_at.tzinfo is None:
                retrieved_at = retrieved_at.replace(tzinfo=timezone.utc)

            if retrieved_at > freeze_timestamp:
                raise HTTPException(
                    status_code=400,
                    detail=f"Evidence item {evidence.evidence_id} was retrieved after freeze timestamp.",
                )

    payload = build_frozen_payload(
        prediction_case=prediction_case,
        match=match,
        evidence_items=evidence_items,
        freeze_timestamp=freeze_timestamp,
    )

    frozen_payload = canonical_json(payload)
    immutable_hash = sha256_hash(frozen_payload)

    frozen_prediction = FrozenPrediction(
        prediction_case_id=prediction_case.id,
        match_id=match.id,
        predicted_winner_id=prediction_case.predicted_winner_id,
        predicted_loser_id=prediction_case.predicted_loser_id,
        frozen_payload=frozen_payload,
        immutable_hash=immutable_hash,
        frozen_at=freeze_timestamp,
    )

    prediction_case.frozen_at = freeze_timestamp
    prediction_case.immutable_hash = immutable_hash
    prediction_case.certification_status = "frozen"

    db.add(frozen_prediction)
    db.commit()
    db.refresh(frozen_prediction)

    return frozen_prediction


@router.get("/frozen-predictions", response_model=list[FrozenPredictionRead])
def list_frozen_predictions(db: Session = Depends(get_db)):
    frozen_predictions = db.scalars(
        select(FrozenPrediction).order_by(FrozenPrediction.id)
    ).all()

    return frozen_predictions


@router.get("/frozen-predictions/{frozen_prediction_id}", response_model=FrozenPredictionRead)
def get_frozen_prediction(frozen_prediction_id: int, db: Session = Depends(get_db)):
    frozen_prediction = db.get(FrozenPrediction, frozen_prediction_id)

    if not frozen_prediction:
        raise HTTPException(status_code=404, detail="Frozen prediction not found.")

    return frozen_prediction
