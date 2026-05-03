from datetime import date, time
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AvailabilityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    effective_from: date | None = None
    effective_until: date | None = None

    @model_validator(mode="after")
    def validate_range(self) -> Self:
        if self.start_time >= self.end_time:
            raise ValueError("availability start must be before its end")
        if (
            self.effective_from
            and self.effective_until
            and self.effective_from > self.effective_until
        ):
            raise ValueError("availability date range is reversed")
        return self


class AvailabilityResponse(AvailabilityCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
