from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.preferences import get_preference_service
from app.models.user import User
from app.schemas.preferences import (
    ConstraintCreate,
    ConstraintResponse,
    PreferenceCreate,
    PreferenceResponse,
)
from app.services.preferences import (
    PreferenceItemNotFoundError,
    PreferenceService,
)

router = APIRouter(
    prefix="/api/scheduling",
    tags=["scheduling preferences"],
)


@router.get(
    "/constraints",
    response_model=list[ConstraintResponse],
)
async def list_constraints(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> list[ConstraintResponse]:
    constraints = await service.list_constraints(user.id)
    return [ConstraintResponse.model_validate(constraint) for constraint in constraints]


@router.post(
    "/constraints",
    response_model=ConstraintResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_constraint(
    request: ConstraintCreate,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> ConstraintResponse:
    constraint = await service.create_constraint(user.id, request)
    return ConstraintResponse.model_validate(constraint)


@router.delete(
    "/constraints/{constraint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_constraint(
    constraint_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> None:
    try:
        await service.delete_constraint(user.id, constraint_id)
    except PreferenceItemNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="scheduling constraint not found",
        ) from error


@router.get(
    "/preferences",
    response_model=list[PreferenceResponse],
)
async def list_preferences(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> list[PreferenceResponse]:
    preferences = await service.list_preferences(user.id)
    return [PreferenceResponse.model_validate(preference) for preference in preferences]


@router.post(
    "/preferences",
    response_model=PreferenceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_preference(
    request: PreferenceCreate,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> PreferenceResponse:
    preference = await service.create_preference(user.id, request)
    return PreferenceResponse.model_validate(preference)


@router.delete(
    "/preferences/{preference_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_preference(
    preference_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> None:
    try:
        await service.delete_preference(user.id, preference_id)
    except PreferenceItemNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="scheduling preference not found",
        ) from error
