from datetime import datetime, time
from uuid import UUID

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, UuidPrimaryKeyMixin


class User(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(100))
    timezone: Mapped[str] = mapped_column(
        String(64),
        default="Australia/Sydney",
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    settings: Mapped["UserSettings"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    sessions: Mapped[list["AuthSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class UserSettings(TimestampMixin, Base):
    __tablename__ = "user_settings"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    preferred_day_start: Mapped[time] = mapped_column(
        Time,
        default=time(8, 0),
    )
    preferred_day_end: Mapped[time] = mapped_column(
        Time,
        default=time(21, 0),
    )
    maximum_daily_work_minutes: Mapped[int] = mapped_column(
        Integer,
        default=480,
    )
    schedule_change_weight: Mapped[float] = mapped_column(
        Float,
        default=1.0,
    )
    user: Mapped[User] = relationship(back_populates="settings")


class AuthSession(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "auth_sessions"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )
    expires_at: Mapped[datetime] = mapped_column(
        nullable=False,
        index=True,
    )
    last_used_at: Mapped[datetime | None] = mapped_column(nullable=True)
    user: Mapped[User] = relationship(back_populates="sessions")
