from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.scheduling.domain.tasks import (
    FlexibleTask,
    TaskDifficulty,
    TaskPriority,
    TaskStatus,
)


def test_task_classifications_use_stable_string_values() -> None:
    assert TaskStatus.IN_PROGRESS == "in_progress"
    assert TaskPriority.URGENT == "urgent"
    assert TaskDifficulty.HIGH == "high"


def test_flexible_task_keeps_the_solver_fields_together() -> None:
    start = datetime(2026, 4, 27, 18, 0, tzinfo=UTC)
    task = FlexibleTask(
        id=uuid4(),
        title="Finish report",
        estimated_minutes=180,
        remaining_minutes=180,
        earliest_start=start,
        deadline=start + timedelta(days=3),
        minimum_session_minutes=30,
        maximum_session_minutes=120,
        preferred_session_minutes=60,
        splittable=True,
    )

    assert task.remaining_minutes == 180
    assert task.priority == TaskPriority.MEDIUM
    assert task.status == TaskStatus.BACKLOG
