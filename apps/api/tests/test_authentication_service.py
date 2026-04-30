from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.auth.passwords import PasswordService
from app.models.user import User
from app.repositories.sessions import SessionRepository
from app.repositories.users import UserRepository
from app.services.authentication import (
    AuthenticationService,
    InvalidCredentialsError,
)


def auth_service(
    users: UserRepository,
    sessions: SessionRepository,
) -> AuthenticationService:
    return AuthenticationService(
        users,
        sessions,
        PasswordService(),
        session_days=30,
    )


@pytest.mark.asyncio
async def test_login_creates_a_session_for_valid_credentials() -> None:
    users = AsyncMock(spec=UserRepository)
    sessions = AsyncMock(spec=SessionRepository)
    password_hash = PasswordService().hash("a useful password")
    users.find_by_email.return_value = User(
        id=uuid4(),
        email="adam@example.com",
        password_hash=password_hash,
        display_name="Adam",
        timezone="Australia/Sydney",
        is_active=True,
    )
    sessions.create.return_value = (AsyncMock(), "raw session token")

    result = await auth_service(users, sessions).login(
        "adam@example.com",
        "a useful password",
    )

    assert result.token == "raw session token"
    sessions.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_login_hides_invalid_email_and_password_cases() -> None:
    users = AsyncMock(spec=UserRepository)
    sessions = AsyncMock(spec=SessionRepository)
    users.find_by_email.return_value = None

    with pytest.raises(InvalidCredentialsError):
        await auth_service(users, sessions).login(
            "missing@example.com",
            "a useful password",
        )

    sessions.create.assert_not_awaited()
