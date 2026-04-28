from uuid import UUID

from sqlalchemy import JSON, Boolean, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.mixins import TimestampMixin, UuidPrimaryKeyMixin


class SchedulingPreference(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "scheduling_preferences"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    kind: Mapped[str] = mapped_column(String(50))
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    settings: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class SchedulingConstraint(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "scheduling_constraints"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    kind: Mapped[str] = mapped_column(String(50))
    settings: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
