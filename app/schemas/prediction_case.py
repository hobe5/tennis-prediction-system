from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PredictionCaseCreate(BaseModel):
    match_id: int
    predicted_winner_id: int

    decision_type: str = "manual"
    data_quality: str = "unknown"
    prediction_integrity_score: float | None = None
    certification_status: str = "draft"

    main_reasons: str | None = None
    main_risks: str | None = None
    strongest_counterargument: str | None = None

    engine_summary: str | None = None
    conflict_summary: str | None = None
    missing_data_summary: str | None = None
    source_summary: str | None = None

    model_version: str = "manual-v0"
    rule_version: str = "rules-v0"
    deployment_version: str = "local-dev"


class PredictionCaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    match_id: int

    player_a_id: int
    player_b_id: int

    predicted_winner_id: int
    predicted_loser_id: int

    decision_type: str
    data_quality: str
    prediction_integrity_score: float | None
    certification_status: str

    main_reasons: str | None
    main_risks: str | None
    strongest_counterargument: str | None

    engine_summary: str | None
    conflict_summary: str | None
    missing_data_summary: str | None
    source_summary: str | None

    model_version: str
    rule_version: str
    deployment_version: str

    frozen_at: datetime | None
    immutable_hash: str | None
    created_at: datetime
