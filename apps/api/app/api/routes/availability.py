from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.availability import get_availability_service
from app.models.user import User
from app.schemas.availability import AvailabilityCreate, AvailabilityResponse
from app.services.availability import (
    AvailabilityNotFoundError,
    AvailabilityService,
)

router = APIRouter(prefix="/api/availability", tags=["availability"])


@router.get("", response_model=list[AvailabilityResponse])
async def list_availability(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[
        AvailabilityService,
        Depends(get_availability_service),
    ],
) -> list[AvailabilityResponse]:
    windows = await service.list(user.id)
    return [AvailabilityResponse.model_validate(window) for window in windows]


@router.post(
    "",
    response_model=AvailabilityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_availability(
    request: AvailabilityCreate,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[
        AvailabilityService,
        Depends(get_availability_service),
    ],
) -> AvailabilityResponse:
    window = await service.create(user.id, request)
    return AvailabilityResponse.model_validate(window)


@router.delete("/{window_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_availability(
    window_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[
        AvailabilityService,
        Depends(get_availability_service),
    ],
) -> None:
    try:
        await service.delete(user.id, window_id)
    except AvailabilityNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="availability window not found",
        ) from error
