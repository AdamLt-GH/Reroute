from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.tasks import get_task_service
from app.models.user import User
from app.schemas.tasks import TaskCreate, TaskResponse
from app.services.tasks import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskResponse]:
    tasks = await service.list(user.id)
    return [TaskResponse.model_validate(task) for task in tasks]


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    request: TaskCreate,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskResponse:
    task = await service.create(user.id, request)
    return TaskResponse.model_validate(task)
