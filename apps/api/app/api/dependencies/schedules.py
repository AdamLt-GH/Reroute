from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_session
from app.services.schedules import ScheduleService


def get_schedule_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ScheduleService:
    return ScheduleService(session)
