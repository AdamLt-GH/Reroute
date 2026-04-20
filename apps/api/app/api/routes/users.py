from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.users import get_registration_service
from app.schemas.users import UserRegistration, UserResponse
from app.services.users import EmailAlreadyRegisteredError, RegistrationService

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: UserRegistration,
    service: Annotated[RegistrationService, Depends(get_registration_service)],
) -> UserResponse:
    try:
        user = await service.register(request)
    except EmailAlreadyRegisteredError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email is already registered",
        ) from error

    return UserResponse.model_validate(user)
