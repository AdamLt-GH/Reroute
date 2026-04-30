from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.passwords import PasswordService
from app.core.config import Settings, get_settings
from app.database.dependencies import get_session
from app.models.user import User
from app.repositories.sessions import SessionRepository
from app.repositories.users import UserRepository
from app.services.authentication import AuthenticationService

SESSION_COOKIE = "reroute_session"


def get_authentication_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AuthenticationService:
    return AuthenticationService(
        UserRepository(session),
        SessionRepository(session),
        PasswordService(),
        session_days=settings.session_days,
    )


async def get_current_user(
    service: Annotated[
        AuthenticationService,
        Depends(get_authentication_service),
    ],
    token: Annotated[str | None, Cookie(alias=SESSION_COOKIE)] = None,
) -> User:
    user = await service.current_user(token) if token else None

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="authentication required",
        )

    return user
