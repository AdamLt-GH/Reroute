from uuid import UUID

from app.models.task import Task
from app.repositories.tasks import TaskRepository
from app.schemas.tasks import TaskCreate


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def list(self, user_id: UUID) -> list[Task]:
        return await self._repository.list_for_user(user_id)

    async def create(
        self,
        user_id: UUID,
        request: TaskCreate,
    ) -> Task:
        values = request.model_dump()
        estimated_minutes = values["estimated_minutes"]
        return await self._repository.add(
            Task(
                user_id=user_id,
                **values,
                remaining_minutes=estimated_minutes,
                actual_minutes=0,
                status="backlog",
            )
        )
