from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, UuidPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class FixedEvent(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "fixed_events"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
    )
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    location: Mapped[str | None] = mapped_column(String(300), nullable=True)
    travel_before_minutes: Mapped[int] = mapped_column(Integer, default=0)
    travel_after_minutes: Mapped[int] = mapped_column(Integer, default=0)
    recurrence_rule: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    locked: Mapped[bool] = mapped_column(Boolean, default=True)
    source: Mapped[str] = mapped_column(String(50), default="manual")
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    user: Mapped[User] = relationship(back_populates="fixed_events")
