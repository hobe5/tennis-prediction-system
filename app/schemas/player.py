from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class PlayerCreate(BaseModel):
    canonical_name: str
    birth_date: date | None = None
    nationality: str | None = None
    handedness: str | None = None


class PlayerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    canonical_name: str
    birth_date: date | None
    nationality: str | None
    handedness: str | None
    created_at: datetime