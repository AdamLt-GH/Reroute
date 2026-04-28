from app.models.task import Task


def test_task_model_indexes_owner_and_deadline() -> None:
    table = Task.__table__

    assert table.c.user_id.index
    assert table.c.deadline.index


def test_task_model_keeps_planned_and_actual_time_separate() -> None:
    columns = Task.__table__.c

    assert "estimated_minutes" in columns
    assert "remaining_minutes" in columns
    assert "actual_minutes" in columns
