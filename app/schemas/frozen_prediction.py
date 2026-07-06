from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FrozenPredictionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prediction_case_id: int
    match_id: int

    predicted_winner_id: int
    predicted_loser_id: int

    frozen_payload: str
    immutable_hash: str

    frozen_at: datetime
    created_at: datetime
