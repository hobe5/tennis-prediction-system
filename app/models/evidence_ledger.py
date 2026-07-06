from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EvidenceLedger(Base):
    __tablename__ = "evidence_ledger"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    evidence_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    match_id: Mapped[int | None] = mapped_column(ForeignKey("matches.id"), nullable=True)
    player_id: Mapped[int | None] = mapped_column(ForeignKey("players.id"), nullable=True)
    source_id: Mapped[int | None] = mapped_column(ForeignKey("source_registry.id"), nullable=True)

    fact_type: Mapped[str] = mapped_column(String(255), nullable=False)
    fact_value: Mapped[str] = mapped_column(Text, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(100), nullable=True)
    time_window: Mapped[str | None] = mapped_column(String(100), nullable=True)

    retrieved_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_from: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_until: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    confidence_level: Mapped[str | None] = mapped_column(String(100), nullable=True)
    used_by_engine: Mapped[str | None] = mapped_column(String(255), nullable=True)
    effect_direction: Mapped[str | None] = mapped_column(String(100), nullable=True)
    effect_strength: Mapped[float | None] = mapped_column(Float, nullable=True)

    fact_status: Mapped[str] = mapped_column(String(100), nullable=False, default="accepted")
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )