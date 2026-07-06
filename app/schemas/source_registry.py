from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SourceCreate(BaseModel):
    source_name: str
    source_type: str
    priority_level: str

    official_status: str | None = None
    api_or_web: str | None = None
    reliability_score: float | None = None

    license_status: str | None = None
    rate_limits: str | None = None
    known_weaknesses: str | None = None


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_name: str
    source_type: str
    priority_level: str

    official_status: str | None
    api_or_web: str | None
    reliability_score: float | None

    license_status: str | None
    rate_limits: str | None
    known_weaknesses: str | None

    created_at: datetime