from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.schedules import get_schedule_service
from app.models.user import User
from app.schemas.schedules import (
    ScheduleGenerateRequest,
    ScheduleRecalculateRequest,
    ScheduleResponse,
)
from app.services.schedules import ScheduleNotFoundError, ScheduleService

router = APIRouter(prefix="/api/schedules", tags=["schedules"])


@router.get("", response_model=list[ScheduleResponse])
async def list_schedules(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ScheduleService, Depends(get_schedule_service)],
) -> list[ScheduleResponse]:
    schedules = await service.list(user.id)
    return [ScheduleResponse.model_validate(item) for item in schedules]


@router.post(
    "/generate",
    response_model=ScheduleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_schedule(
    request: ScheduleGenerateRequest,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ScheduleService, Depends(get_schedule_service)],
) -> ScheduleResponse:
    schedule = await service.generate(user, request)
    return ScheduleResponse.model_validate(schedule)


@router.post("/{schedule_id}/accept", response_model=ScheduleResponse)
async def accept_schedule(
    schedule_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ScheduleService, Depends(get_schedule_service)],
) -> ScheduleResponse:
    try:
        schedule = await service.accept(user.id, schedule_id)
    except ScheduleNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="schedule not found",
        ) from error
    return ScheduleResponse.model_validate(schedule)


@router.post(
    "/{schedule_id}/recalculate",
    response_model=ScheduleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def recalculate_schedule(
    schedule_id: UUID,
    request: ScheduleRecalculateRequest,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ScheduleService, Depends(get_schedule_service)],
) -> ScheduleResponse:
    try:
        schedule = await service.recalculate(user, schedule_id, request)
    except ScheduleNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="schedule not found",
        ) from error
    return ScheduleResponse.model_validate(schedule)
