from sqlalchemy import Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    canonical_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    birth_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(100), nullable=True)
    handedness: Mapped[str | None] = mapped_column(String(50), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )