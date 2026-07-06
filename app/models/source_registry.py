from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SourceRegistry(Base):
    __tablename__ = "source_registry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    source_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False)
    priority_level: Mapped[str] = mapped_column(String(20), nullable=False)

    official_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    api_or_web: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reliability_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    license_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    rate_limits: Mapped[str | None] = mapped_column(Text, nullable=True)
    known_weaknesses: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )