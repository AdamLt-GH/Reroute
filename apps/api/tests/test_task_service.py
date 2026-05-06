from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.repositories.tasks import TaskRepository
from app.schemas.tasks import TaskCreate
from app.services.tasks import TaskService


@pytest.mark.asyncio
async def test_task_service_sets_initial_progress() -> None:
    repository = AsyncMock(spec=TaskRepository)
    repository.add.side_effect = lambda task: task
    start = datetime(2026, 5, 6, 18, tzinfo=UTC)

    task = await TaskService(repository).create(
        uuid4(),
        TaskCreate(
            title="Finish report",
            estimated_minutes=180,
            earliest_start=start,
            deadline=start + timedelta(days=2),
        ),
    )

    assert task.remaining_minutes == 180
    assert task.actual_minutes == 0
    assert task.status == "backlog"
