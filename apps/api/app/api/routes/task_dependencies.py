from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.tasks import get_task_dependency_service
from app.models.user import User
from app.scheduling.domain.dependencies import DependencyError
from app.schemas.tasks import TaskDependencyCreate, TaskDependencyResponse
from app.services.task_dependencies import (
    TaskDependencyExistsError,
    TaskDependencyNotFoundError,
    TaskDependencyService,
)

router = APIRouter(
    prefix="/api/task-dependencies",
    tags=["task dependencies"],
)


@router.get("", response_model=list[TaskDependencyResponse])
async def list_task_dependencies(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[
        TaskDependencyService,
        Depends(get_task_dependency_service),
    ],
) -> list[TaskDependencyResponse]:
    dependencies = await service.list(user.id)
    return [
        TaskDependencyResponse.model_validate(dependency) for dependency in dependencies
    ]


@router.post(
    "",
    response_model=TaskDependencyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_dependency(
    request: TaskDependencyCreate,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[
        TaskDependencyService,
        Depends(get_task_dependency_service),
    ],
) -> TaskDependencyResponse:
    try:
        dependency = await service.create(
            user.id,
            request.prerequisite_id,
            request.dependent_id,
        )
    except TaskDependencyNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found",
        ) from error
    except TaskDependencyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="task dependency already exists",
        ) from error
    except DependencyError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error

    return TaskDependencyResponse.model_validate(dependency)


@router.delete(
    "/{prerequisite_id}/{dependent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task_dependency(
    prerequisite_id: UUID,
    dependent_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[
        TaskDependencyService,
        Depends(get_task_dependency_service),
    ],
) -> None:
    try:
        await service.delete(
            user.id,
            prerequisite_id,
            dependent_id,
        )
    except TaskDependencyNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task dependency not found",
        ) from error
