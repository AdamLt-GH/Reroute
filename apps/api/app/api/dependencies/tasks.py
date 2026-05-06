from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_session
from app.repositories.tasks import TaskDependencyRepository, TaskRepository
from app.services.task_dependencies import TaskDependencyService
from app.services.tasks import TaskService


def get_task_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskService:
    return TaskService(TaskRepository(session))


def get_task_dependency_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskDependencyService:
    return TaskDependencyService(
        TaskRepository(session),
        TaskDependencyRepository(session),
    )
