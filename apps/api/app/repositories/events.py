from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import FixedEvent


class EventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_user(self, user_id: UUID) -> list[FixedEvent]:
        statement = (
            select(FixedEvent)
            .where(FixedEvent.user_id == user_id)
            .order_by(FixedEvent.start_at)
        )
        result = await self._session.scalars(statement)
        return list(result)

    async def add(self, event: FixedEvent) -> FixedEvent:
        self._session.add(event)
        await self._session.flush()
        await self._session.refresh(event)
        return event

    async def delete_for_user(self, user_id: UUID, event_id: UUID) -> bool:
        statement = (
            delete(FixedEvent)
            .where(
                FixedEvent.id == event_id,
                FixedEvent.user_id == user_id,
            )
            .returning(FixedEvent.id)
        )
        result = await self._session.scalar(statement)
        return result is not None
