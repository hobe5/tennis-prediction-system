from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.match import Match
from app.models.player import Player
from app.schemas.match import MatchCreate, MatchRead

router = APIRouter(prefix="/matches", tags=["matches"])


@router.post("", response_model=MatchRead)
def create_match(payload: MatchCreate, db: Session = Depends(get_db)):
    if payload.player_a_id == payload.player_b_id:
        raise HTTPException(
            status_code=400,
            detail="player_a_id and player_b_id must be different.",
        )

    player_a = db.get(Player, payload.player_a_id)
    player_b = db.get(Player, payload.player_b_id)

    if not player_a:
        raise HTTPException(status_code=404, detail="Player A not found.")

    if not player_b:
        raise HTTPException(status_code=404, detail="Player B not found.")

    match = Match(
        tournament_name=payload.tournament_name,
        round=payload.round,
        surface=payload.surface,
        scheduled_start_time=payload.scheduled_start_time,
        timezone=payload.timezone,
        player_a_id=payload.player_a_id,
        player_b_id=payload.player_b_id,
        match_status="scheduled",
    )

    db.add(match)
    db.commit()
    db.refresh(match)

    return match


@router.get("", response_model=list[MatchRead])
def list_matches(db: Session = Depends(get_db)):
    matches = db.scalars(
        select(Match).order_by(Match.id)
    ).all()

    return matches