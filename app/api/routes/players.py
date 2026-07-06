from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerRead

router = APIRouter(prefix="/players", tags=["players"])


@router.post("", response_model=PlayerRead)
def create_player(payload: PlayerCreate, db: Session = Depends(get_db)):
    existing_player = db.scalar(
        select(Player).where(Player.canonical_name == payload.canonical_name)
    )

    if existing_player:
        raise HTTPException(
            status_code=409,
            detail="Player with this canonical_name already exists.",
        )

    player = Player(
        canonical_name=payload.canonical_name,
        birth_date=payload.birth_date,
        nationality=payload.nationality,
        handedness=payload.handedness,
    )

    db.add(player)
    db.commit()
    db.refresh(player)

    return player


@router.get("", response_model=list[PlayerRead])
def list_players(db: Session = Depends(get_db)):
    players = db.scalars(
        select(Player).order_by(Player.id)
    ).all()

    return players