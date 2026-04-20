from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.passwords import PasswordService
from app.database.dependencies import get_session
from app.repositories.users import UserRepository
from app.services.users import RegistrationService


def get_registration_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RegistrationService:
    return RegistrationService(
        UserRepository(session),
        PasswordService(),
    )
