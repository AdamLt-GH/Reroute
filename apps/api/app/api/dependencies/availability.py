from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_session
from app.repositories.availability import AvailabilityRepository
from app.services.availability import AvailabilityService


def get_availability_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AvailabilityService:
    return AvailabilityService(AvailabilityRepository(session))
