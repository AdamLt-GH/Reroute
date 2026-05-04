from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_session
from app.repositories.events import EventRepository
from app.services.events import EventService


def get_event_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EventService:
    return EventService(EventRepository(session))
