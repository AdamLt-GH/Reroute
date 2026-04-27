from app.scheduling.domain.tasks import (
    TaskDifficulty,
    TaskPriority,
    TaskStatus,
)


def test_task_classifications_use_stable_string_values() -> None:
    assert TaskStatus.IN_PROGRESS == "in_progress"
    assert TaskPriority.URGENT == "urgent"
    assert TaskDifficulty.HIGH == "high"
