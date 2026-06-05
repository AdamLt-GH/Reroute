from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator


class ScheduleGenerateRequest(BaseModel):
    horizon_start: datetime
    horizon_end: datetime

    @model_validator(mode="after")
    def validate_horizon(self) -> Self:
        if self.horizon_start.tzinfo is None or self.horizon_end.tzinfo is None:
            raise ValueError("schedule horizon must include a timezone")
        if self.horizon_start >= self.horizon_end:
            raise ValueError("schedule horizon is reversed")
        return self


class ScheduleBlockResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    task_id: UUID | None
    title: str
    start_at: datetime
    end_at: datetime
    locked: bool
    completed: bool


class ScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    horizon_start: datetime
    horizon_end: datetime
    status: str
    source: str
    parent_schedule_id: UUID | None
    unscheduled_task_ids: list[str]
    blocks: list[ScheduleBlockResponse]
