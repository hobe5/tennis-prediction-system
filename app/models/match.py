from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    external_match_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    tournament_name: Mapped[str] = mapped_column(String(255), nullable=False)
    round: Mapped[str | None] = mapped_column(String(100), nullable=True)
    surface: Mapped[str | None] = mapped_column(String(100), nullable=True)

    scheduled_start_time: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    timezone: Mapped[str | None] = mapped_column(String(100), nullable=True)

    player_a_id: Mapped[int | None] = mapped_column(ForeignKey("players.id"), nullable=True)
    player_b_id: Mapped[int | None] = mapped_column(ForeignKey("players.id"), nullable=True)
    winner_id: Mapped[int | None] = mapped_column(ForeignKey("players.id"), nullable=True)

    match_status: Mapped[str] = mapped_column(String(100), nullable=False, default="scheduled")

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )