from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.source_registry import SourceRegistry
from app.schemas.source_registry import SourceCreate, SourceRead

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("", response_model=SourceRead)
def create_source(payload: SourceCreate, db: Session = Depends(get_db)):
    existing_source = db.scalar(
        select(SourceRegistry).where(SourceRegistry.source_name == payload.source_name)
    )

    if existing_source:
        raise HTTPException(
            status_code=409,
            detail="Source with this source_name already exists.",
        )

    source = SourceRegistry(
        source_name=payload.source_name,
        source_type=payload.source_type,
        priority_level=payload.priority_level,
        official_status=payload.official_status,
        api_or_web=payload.api_or_web,
        reliability_score=payload.reliability_score,
        license_status=payload.license_status,
        rate_limits=payload.rate_limits,
        known_weaknesses=payload.known_weaknesses,
    )

    db.add(source)
    db.commit()
    db.refresh(source)

    return source


@router.get("", response_model=list[SourceRead])
def list_sources(db: Session = Depends(get_db)):
    sources = db.scalars(
        select(SourceRegistry).order_by(SourceRegistry.id)
    ).all()

    return sources