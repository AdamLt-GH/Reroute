from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.preference import SchedulingConstraint, SchedulingPreference


class PreferenceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_constraints(
        self,
        user_id: UUID,
    ) -> list[SchedulingConstraint]:
        result = await self._session.scalars(
            select(SchedulingConstraint)
            .where(SchedulingConstraint.user_id == user_id)
            .order_by(SchedulingConstraint.created_at)
        )
        return list(result)

    async def add_constraint(
        self,
        constraint: SchedulingConstraint,
    ) -> SchedulingConstraint:
        self._session.add(constraint)
        await self._session.flush()
        await self._session.refresh(constraint)
        return constraint

    async def delete_constraint(
        self,
        user_id: UUID,
        constraint_id: UUID,
    ) -> bool:
        result = await self._session.scalar(
            delete(SchedulingConstraint)
            .where(
                SchedulingConstraint.id == constraint_id,
                SchedulingConstraint.user_id == user_id,
            )
            .returning(SchedulingConstraint.id)
        )
        return result is not None

    async def list_preferences(
        self,
        user_id: UUID,
    ) -> list[SchedulingPreference]:
        result = await self._session.scalars(
            select(SchedulingPreference)
            .where(SchedulingPreference.user_id == user_id)
            .order_by(SchedulingPreference.created_at)
        )
        return list(result)

    async def add_preference(
        self,
        preference: SchedulingPreference,
    ) -> SchedulingPreference:
        self._session.add(preference)
        await self._session.flush()
        await self._session.refresh(preference)
        return preference

    async def delete_preference(
        self,
        user_id: UUID,
        preference_id: UUID,
    ) -> bool:
        result = await self._session.scalar(
            delete(SchedulingPreference)
            .where(
                SchedulingPreference.id == preference_id,
                SchedulingPreference.user_id == user_id,
            )
            .returning(SchedulingPreference.id)
        )
        return result is not None
