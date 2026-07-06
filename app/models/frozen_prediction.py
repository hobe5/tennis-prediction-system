from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class FrozenPrediction(Base):
    __tablename__ = "frozen_predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    prediction_case_id: Mapped[int] = mapped_column(
        ForeignKey("prediction_cases.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), nullable=False, index=True)

    predicted_winner_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    predicted_loser_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)

    frozen_payload: Mapped[str] = mapped_column(Text, nullable=False)
    immutable_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    frozen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
