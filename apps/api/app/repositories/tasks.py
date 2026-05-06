from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskDependency


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_user(self, user_id: UUID) -> list[Task]:
        result = await self._session.scalars(
            select(Task).where(Task.user_id == user_id).order_by(Task.deadline)
        )
        return list(result)

    async def find_for_user(
        self,
        user_id: UUID,
        task_id: UUID,
    ) -> Task | None:
        return await self._session.scalar(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id,
            )
        )

    async def ids_for_user(self, user_id: UUID) -> set[UUID]:
        result = await self._session.scalars(
            select(Task.id).where(Task.user_id == user_id)
        )
        return set(result)

    async def add(self, task: Task) -> Task:
        self._session.add(task)
        await self._session.flush()
        await self._session.refresh(task)
        return task


class TaskDependencyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_user(
        self,
        user_id: UUID,
    ) -> list[TaskDependency]:
        owned_tasks = select(Task.id).where(Task.user_id == user_id)
        result = await self._session.scalars(
            select(TaskDependency)
            .where(
                TaskDependency.prerequisite_id.in_(owned_tasks),
                TaskDependency.dependent_id.in_(owned_tasks),
            )
            .order_by(TaskDependency.created_at)
        )
        return list(result)

    async def add(
        self,
        dependency: TaskDependency,
    ) -> TaskDependency:
        self._session.add(dependency)
        await self._session.flush()
        await self._session.refresh(dependency)
        return dependency

    async def delete_for_user(
        self,
        user_id: UUID,
        prerequisite_id: UUID,
        dependent_id: UUID,
    ) -> bool:
        owned_tasks = select(Task.id).where(Task.user_id == user_id)
        result = await self._session.scalar(
            delete(TaskDependency)
            .where(
                TaskDependency.prerequisite_id == prerequisite_id,
                TaskDependency.dependent_id == dependent_id,
                TaskDependency.prerequisite_id.in_(owned_tasks),
                TaskDependency.dependent_id.in_(owned_tasks),
            )
            .returning(TaskDependency.prerequisite_id)
        )
        return result is not None
