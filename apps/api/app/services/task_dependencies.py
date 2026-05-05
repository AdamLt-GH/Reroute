from uuid import UUID

from app.models.task import TaskDependency
from app.repositories.tasks import TaskDependencyRepository, TaskRepository
from app.scheduling.domain.dependencies import (
    Dependency,
    build_dependency_graph,
    validate_acyclic,
)


class TaskDependencyNotFoundError(ValueError):
    pass


class TaskDependencyExistsError(ValueError):
    pass


class TaskDependencyService:
    def __init__(
        self,
        tasks: TaskRepository,
        dependencies: TaskDependencyRepository,
    ) -> None:
        self._tasks = tasks
        self._dependencies = dependencies

    async def list(self, user_id: UUID) -> list[TaskDependency]:
        return await self._dependencies.list_for_user(user_id)

    async def create(
        self,
        user_id: UUID,
        prerequisite_id: UUID,
        dependent_id: UUID,
    ) -> TaskDependency:
        task_ids = await self._tasks.ids_for_user(user_id)
        if prerequisite_id not in task_ids or dependent_id not in task_ids:
            raise TaskDependencyNotFoundError

        existing = await self._dependencies.list_for_user(user_id)
        if any(
            item.prerequisite_id == prerequisite_id
            and item.dependent_id == dependent_id
            for item in existing
        ):
            raise TaskDependencyExistsError

        all_dependencies = [
            Dependency(item.prerequisite_id, item.dependent_id) for item in existing
        ]
        all_dependencies.append(Dependency(prerequisite_id, dependent_id))
        graph = build_dependency_graph(task_ids, all_dependencies)
        validate_acyclic(graph)

        return await self._dependencies.add(
            TaskDependency(
                prerequisite_id=prerequisite_id,
                dependent_id=dependent_id,
            )
        )

    async def delete(
        self,
        user_id: UUID,
        prerequisite_id: UUID,
        dependent_id: UUID,
    ) -> None:
        removed = await self._dependencies.delete_for_user(
            user_id,
            prerequisite_id,
            dependent_id,
        )
        if not removed:
            raise TaskDependencyNotFoundError
