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


class TaskValidationError(ValueError):
    pass


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


def validate_task(task: FlexibleTask) -> FlexibleTask:
    if not task.title.strip():
        raise TaskValidationError("task title is required")
    if task.estimated_minutes <= 0:
        raise TaskValidationError("estimated duration must be positive")
    if not 0 <= task.remaining_minutes <= task.estimated_minutes:
        raise TaskValidationError("remaining duration is outside the estimate")
    if task.earliest_start.tzinfo is None or task.deadline.tzinfo is None:
        raise TaskValidationError("task times must include a timezone")
    if task.earliest_start >= task.deadline:
        raise TaskValidationError("deadline must be after the earliest start")
    if task.minimum_session_minutes <= 0:
        raise TaskValidationError("minimum session must be positive")
    if not (
        task.minimum_session_minutes
        <= task.preferred_session_minutes
        <= task.maximum_session_minutes
    ):
        raise TaskValidationError("session lengths are out of order")
    if not task.splittable and task.remaining_minutes > task.maximum_session_minutes:
        raise TaskValidationError("non-splittable task does not fit one session")

    return task
