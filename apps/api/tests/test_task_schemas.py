from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.tasks import TaskCreate


def valid_task_request(**changes: object) -> dict[str, object]:
    start = datetime(2026, 4, 28, 18, 0, tzinfo=UTC)
    values: dict[str, object] = {
        "title": "Finish report",
        "estimated_minutes": 180,
        "earliest_start": start,
        "deadline": start + timedelta(days=2),
        "minimum_session_minutes": 30,
        "maximum_session_minutes": 120,
        "preferred_session_minutes": 60,
        "splittable": True,
    }
    values.update(changes)
    return values


def test_task_request_accepts_a_valid_split_task() -> None:
    request = TaskCreate.model_validate(valid_task_request())

    assert request.estimated_minutes == 180
    assert request.preferred_session_minutes == 60


@pytest.mark.parametrize(
    "changes",
    [
        {"deadline": datetime(2026, 4, 27, 18, 0, tzinfo=UTC)},
        {"preferred_session_minutes": 20},
        {"splittable": False},
    ],
)
def test_task_request_rejects_conflicting_rules(
    changes: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        TaskCreate.model_validate(valid_task_request(**changes))
