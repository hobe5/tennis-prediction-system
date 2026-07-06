from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PredictionCase(Base):
    __tablename__ = "prediction_cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), nullable=False, index=True)

    player_a_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    player_b_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)

    predicted_winner_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    predicted_loser_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)

    decision_type: Mapped[str] = mapped_column(String(100), nullable=False, default="manual")
    data_quality: Mapped[str] = mapped_column(String(100), nullable=False, default="unknown")

    prediction_integrity_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    certification_status: Mapped[str] = mapped_column(String(100), nullable=False, default="draft")

    main_reasons: Mapped[str | None] = mapped_column(Text, nullable=True)
    main_risks: Mapped[str | None] = mapped_column(Text, nullable=True)
    strongest_counterargument: Mapped[str | None] = mapped_column(Text, nullable=True)

    engine_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    conflict_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    missing_data_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    model_version: Mapped[str] = mapped_column(String(100), nullable=False, default="manual-v0")
    rule_version: Mapped[str] = mapped_column(String(100), nullable=False, default="rules-v0")
    deployment_version: Mapped[str] = mapped_column(String(100), nullable=False, default="local-dev")

    frozen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    immutable_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
