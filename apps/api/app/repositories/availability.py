from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.availability import AvailabilityWindow


class AvailabilityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_user(self, user_id: UUID) -> list[AvailabilityWindow]:
        statement = (
            select(AvailabilityWindow)
            .where(AvailabilityWindow.user_id == user_id)
            .order_by(
                AvailabilityWindow.day_of_week,
                AvailabilityWindow.start_time,
            )
        )
        result = await self._session.scalars(statement)
        return list(result)

    async def add(self, window: AvailabilityWindow) -> AvailabilityWindow:
        self._session.add(window)
        await self._session.flush()
        await self._session.refresh(window)
        return window

    async def delete_for_user(self, user_id: UUID, window_id: UUID) -> bool:
        statement = (
            delete(AvailabilityWindow)
            .where(
                AvailabilityWindow.id == window_id,
                AvailabilityWindow.user_id == user_id,
            )
            .returning(AvailabilityWindow.id)
        )
        result = await self._session.scalar(statement)
        return result is not None
