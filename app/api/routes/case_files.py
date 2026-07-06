from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.evidence_ledger import EvidenceLedger
from app.models.match import Match
from app.models.player import Player
from app.schemas.match_case_file import MatchCaseFileRead

router = APIRouter(prefix="/case-files", tags=["case-files"])


@router.get("/{match_id}", response_model=MatchCaseFileRead)
def get_match_case_file(match_id: int, db: Session = Depends(get_db)):
    match = db.get(Match, match_id)

    if not match:
        raise HTTPException(status_code=404, detail="Match not found.")

    player_a = None
    player_b = None

    if match.player_a_id is not None:
        player_a = db.get(Player, match.player_a_id)

    if match.player_b_id is not None:
        player_b = db.get(Player, match.player_b_id)

    evidence_items = db.scalars(
        select(EvidenceLedger)
        .where(EvidenceLedger.match_id == match.id)
        .order_by(EvidenceLedger.id)
    ).all()

    return {
        "match": match,
        "player_a": player_a,
        "player_b": player_b,
        "evidence": evidence_items,
    }