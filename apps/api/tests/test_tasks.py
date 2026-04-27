from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.scheduling.domain.tasks import (
    FlexibleTask,
    TaskDifficulty,
    TaskPriority,
    TaskStatus,
    TaskValidationError,
    validate_task,
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


def build_task(**changes: object) -> FlexibleTask:
    start = datetime(2026, 4, 27, 18, 0, tzinfo=UTC)
    values = {
        "id": uuid4(),
        "title": "Finish report",
        "estimated_minutes": 180,
        "remaining_minutes": 180,
        "earliest_start": start,
        "deadline": start + timedelta(days=3),
        "minimum_session_minutes": 30,
        "maximum_session_minutes": 120,
        "preferred_session_minutes": 60,
        "splittable": True,
    }
    values.update(changes)
    return FlexibleTask(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"estimated_minutes": 0}, "must be positive"),
        ({"remaining_minutes": 181}, "outside the estimate"),
        ({"preferred_session_minutes": 20}, "out of order"),
        ({"splittable": False}, "does not fit one session"),
    ],
)
def test_invalid_task_rules_are_explained(
    changes: dict[str, object],
    message: str,
) -> None:
    with pytest.raises(TaskValidationError, match=message):
        validate_task(build_task(**changes))
