from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FixedEventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    start_at: datetime
    end_at: datetime
    location: str | None = Field(default=None, max_length=300)
    travel_before_minutes: int = Field(default=0, ge=0, le=1440)
    travel_after_minutes: int = Field(default=0, ge=0, le=1440)
    recurrence_rule: str | None = Field(default=None, max_length=500)
    locked: bool = True
    category: str | None = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_times(self) -> Self:
        if self.start_at.tzinfo is None or self.end_at.tzinfo is None:
            raise ValueError("event times must include a timezone")
        if self.start_at >= self.end_at:
            raise ValueError("event end must be after its start")
        return self


class FixedEventResponse(FixedEventCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source: str
