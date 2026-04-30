from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status

from app.api.dependencies.authentication import (
    SESSION_COOKIE,
    get_authentication_service,
    get_current_user,
)
from app.core.config import Settings, get_settings
from app.models.user import User
from app.schemas.authentication import LoginRequest
from app.schemas.users import UserResponse
from app.services.authentication import (
    AuthenticationService,
    InvalidCredentialsError,
)

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/login", response_model=UserResponse)
async def login(
    request: LoginRequest,
    response: Response,
    service: Annotated[
        AuthenticationService,
        Depends(get_authentication_service),
    ],
    settings: Annotated[Settings, Depends(get_settings)],
) -> UserResponse:
    try:
        result = await service.login(str(request.email), request.password)
    except InvalidCredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid email or password",
        ) from error

    response.set_cookie(
        SESSION_COOKIE,
        result.token,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
        max_age=settings.session_days * 24 * 60 * 60,
    )
    return UserResponse.model_validate(result.user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    response: Response,
    service: Annotated[
        AuthenticationService,
        Depends(get_authentication_service),
    ],
    token: Annotated[str | None, Cookie(alias=SESSION_COOKIE)] = None,
) -> None:
    if token:
        await service.logout(token)
    response.delete_cookie(SESSION_COOKIE)


@router.get("/me", response_model=UserResponse)
async def current_user(
    user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    return UserResponse.model_validate(user)
