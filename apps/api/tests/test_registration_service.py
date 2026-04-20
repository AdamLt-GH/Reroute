from unittest.mock import AsyncMock

import pytest

from app.auth.passwords import PasswordService
from app.models.user import User
from app.repositories.users import UserRepository
from app.schemas.users import UserRegistration
from app.services.users import EmailAlreadyRegisteredError, RegistrationService


def registration_request() -> UserRegistration:
    return UserRegistration(
        email="Adam@Example.com",
        password="a useful password",
        display_name="Adam",
    )


@pytest.mark.asyncio
async def test_registration_builds_a_user_with_a_hashed_password() -> None:
    repository = AsyncMock(spec=UserRepository)
    repository.find_by_email.return_value = None
    repository.add.side_effect = lambda user: user

    user = await RegistrationService(
        repository,
        PasswordService(),
    ).register(registration_request())

    assert user.email == "adam@example.com"
    assert user.password_hash != "a useful password"
    assert user.timezone == "Australia/Sydney"


@pytest.mark.asyncio
async def test_registration_rejects_an_existing_email() -> None:
    repository = AsyncMock(spec=UserRepository)
    repository.find_by_email.return_value = User()

    with pytest.raises(EmailAlreadyRegisteredError):
        await RegistrationService(
            repository,
            PasswordService(),
        ).register(registration_request())

    repository.add.assert_not_awaited()
