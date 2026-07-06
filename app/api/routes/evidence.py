from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.evidence_ledger import EvidenceLedger
from app.models.match import Match
from app.models.player import Player
from app.models.source_registry import SourceRegistry
from app.schemas.evidence_ledger import EvidenceCreate, EvidenceRead

router = APIRouter(prefix="/evidence", tags=["evidence"])


@router.post("", response_model=EvidenceRead)
def create_evidence(payload: EvidenceCreate, db: Session = Depends(get_db)):
    source = db.get(SourceRegistry, payload.source_id)

    if not source:
        raise HTTPException(status_code=404, detail="Source not found.")

    if payload.match_id is not None:
        match = db.get(Match, payload.match_id)

        if not match:
            raise HTTPException(status_code=404, detail="Match not found.")

    if payload.player_id is not None:
        player = db.get(Player, payload.player_id)

        if not player:
            raise HTTPException(status_code=404, detail="Player not found.")

    evidence = EvidenceLedger(
        evidence_id=f"EV-{uuid4()}",
        match_id=payload.match_id,
        player_id=payload.player_id,
        source_id=payload.source_id,
        fact_type=payload.fact_type,
        fact_value=payload.fact_value,
        unit=payload.unit,
        time_window=payload.time_window,
        retrieved_at=datetime.now(UTC),
        published_at=payload.published_at,
        valid_from=payload.valid_from,
        valid_until=payload.valid_until,
        confidence_level=payload.confidence_level,
        used_by_engine=payload.used_by_engine,
        effect_direction=payload.effect_direction,
        effect_strength=payload.effect_strength,
        fact_status="accepted",
        notes=payload.notes,
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return evidence


@router.get("", response_model=list[EvidenceRead])
def list_evidence(db: Session = Depends(get_db)):
    evidence_items = db.scalars(
        select(EvidenceLedger).order_by(EvidenceLedger.id)
    ).all()

    return evidence_items