from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class TaskStatus(StrEnum):
    BACKLOG = "backlog"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskDifficulty(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class FlexibleTask:
    id: UUID
    title: str
    estimated_minutes: int
    remaining_minutes: int
    deadline: datetime
    earliest_start: datetime
    minimum_session_minutes: int
    maximum_session_minutes: int
    preferred_session_minutes: int
    splittable: bool
    priority: TaskPriority = TaskPriority.MEDIUM
    difficulty: TaskDifficulty = TaskDifficulty.MEDIUM
    status: TaskStatus = TaskStatus.BACKLOG
