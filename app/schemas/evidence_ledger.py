from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EvidenceCreate(BaseModel):
    match_id: int | None = None
    player_id: int | None = None
    source_id: int

    fact_type: str
    fact_value: str

    unit: str | None = None
    time_window: str | None = None

    published_at: datetime | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None

    confidence_level: str | None = None
    used_by_engine: str | None = None
    effect_direction: str | None = None
    effect_strength: float | None = None

    notes: str | None = None


class EvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    evidence_id: str

    match_id: int | None
    player_id: int | None
    source_id: int | None

    fact_type: str
    fact_value: str
    unit: str | None
    time_window: str | None

    retrieved_at: datetime | None
    published_at: datetime | None
    valid_from: datetime | None
    valid_until: datetime | None

    confidence_level: str | None
    used_by_engine: str | None
    effect_direction: str | None
    effect_strength: float | None

    fact_status: str
    rejection_reason: str | None
    notes: str | None

    created_at: datetime