from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from app.models.task import TaskDependency
from app.repositories.tasks import TaskDependencyRepository, TaskRepository
from app.scheduling.domain.dependencies import DependencyCycleError
from app.services.task_dependencies import (
    TaskDependencyNotFoundError,
    TaskDependencyService,
)


def build_service(
    task_ids: set[UUID],
    existing: list[TaskDependency] | None = None,
) -> tuple[TaskDependencyService, AsyncMock]:
    tasks = AsyncMock(spec=TaskRepository)
    tasks.ids_for_user.return_value = task_ids
    dependencies = AsyncMock(spec=TaskDependencyRepository)
    dependencies.list_for_user.return_value = existing or []
    dependencies.add.side_effect = lambda dependency: dependency
    return TaskDependencyService(tasks, dependencies), dependencies


@pytest.mark.asyncio
async def test_dependency_service_adds_a_valid_owned_link() -> None:
    first_id = uuid4()
    second_id = uuid4()
    service, repository = build_service({first_id, second_id})

    dependency = await service.create(
        uuid4(),
        first_id,
        second_id,
    )

    assert dependency.prerequisite_id == first_id
    assert dependency.dependent_id == second_id
    repository.add.assert_awaited_once()


@pytest.mark.asyncio
async def test_dependency_service_rejects_tasks_owned_by_someone_else() -> None:
    owned_id = uuid4()
    service, repository = build_service({owned_id})

    with pytest.raises(TaskDependencyNotFoundError):
        await service.create(
            uuid4(),
            owned_id,
            uuid4(),
        )

    repository.add.assert_not_awaited()


@pytest.mark.asyncio
async def test_dependency_service_rejects_a_cycle() -> None:
    first_id = uuid4()
    second_id = uuid4()
    third_id = uuid4()
    service, repository = build_service(
        {first_id, second_id, third_id},
        [
            TaskDependency(
                prerequisite_id=first_id,
                dependent_id=second_id,
            ),
            TaskDependency(
                prerequisite_id=second_id,
                dependent_id=third_id,
            ),
        ],
    )

    with pytest.raises(DependencyCycleError):
        await service.create(
            uuid4(),
            third_id,
            first_id,
        )

    repository.add.assert_not_awaited()
