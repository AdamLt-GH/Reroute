from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_session
from app.repositories.preferences import PreferenceRepository
from app.services.preferences import PreferenceService


def get_preference_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PreferenceService:
    return PreferenceService(PreferenceRepository(session))
