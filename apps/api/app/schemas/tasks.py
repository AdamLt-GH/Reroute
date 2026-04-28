from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.scheduling.domain.tasks import (
    TaskDifficulty,
    TaskPriority,
    TaskStatus,
)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    estimated_minutes: int = Field(gt=0)
    earliest_start: datetime
    deadline: datetime
    minimum_session_minutes: int = Field(default=30, gt=0)
    maximum_session_minutes: int = Field(default=120, gt=0)
    preferred_session_minutes: int = Field(default=60, gt=0)
    splittable: bool = True
    priority: TaskPriority = TaskPriority.MEDIUM
    difficulty: TaskDifficulty = TaskDifficulty.MEDIUM
    category: str | None = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_time_and_sessions(self) -> Self:
        if self.earliest_start.tzinfo is None or self.deadline.tzinfo is None:
            raise ValueError("task times must include a timezone")
        if self.earliest_start >= self.deadline:
            raise ValueError("deadline must be after the earliest start")
        if not (
            self.minimum_session_minutes
            <= self.preferred_session_minutes
            <= self.maximum_session_minutes
        ):
            raise ValueError("session lengths are out of order")
        if not self.splittable and (
            self.estimated_minutes > self.maximum_session_minutes
        ):
            raise ValueError("non-splittable task does not fit one session")
        return self


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    estimated_minutes: int
    remaining_minutes: int
    actual_minutes: int
    earliest_start: datetime
    deadline: datetime
    minimum_session_minutes: int
    maximum_session_minutes: int
    preferred_session_minutes: int
    splittable: bool
    priority: TaskPriority
    difficulty: TaskDifficulty
    category: str | None
    status: TaskStatus
