from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MatchCreate(BaseModel):
    tournament_name: str
    round: str | None = None
    surface: str | None = None
    scheduled_start_time: datetime | None = None
    timezone: str | None = None
    player_a_id: int
    player_b_id: int


class MatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_match_id: str | None
    tournament_name: str
    round: str | None
    surface: str | None
    scheduled_start_time: datetime | None
    timezone: str | None
    player_a_id: int | None
    player_b_id: int | None
    winner_id: int | None
    match_status: str
    created_at: datetime