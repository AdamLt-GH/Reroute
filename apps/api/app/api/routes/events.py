from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.events import get_event_service
from app.models.user import User
from app.schemas.events import FixedEventCreate, FixedEventResponse
from app.services.events import (
    EventConflictError,
    EventNotFoundError,
    EventService,
)

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=list[FixedEventResponse])
async def list_events(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[EventService, Depends(get_event_service)],
) -> list[FixedEventResponse]:
    events = await service.list(user.id)
    return [FixedEventResponse.model_validate(event) for event in events]


@router.post(
    "",
    response_model=FixedEventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    request: FixedEventCreate,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[EventService, Depends(get_event_service)],
) -> FixedEventResponse:
    try:
        event = await service.create(user.id, request)
    except EventConflictError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="fixed event conflicts with an existing commitment",
        ) from error
    return FixedEventResponse.model_validate(event)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[EventService, Depends(get_event_service)],
) -> None:
    try:
        await service.delete(user.id, event_id)
    except EventNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="fixed event not found",
        ) from error
