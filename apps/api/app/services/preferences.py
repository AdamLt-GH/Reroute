from uuid import UUID

from app.models.preference import SchedulingConstraint, SchedulingPreference
from app.repositories.preferences import PreferenceRepository
from app.schemas.preferences import ConstraintCreate, PreferenceCreate


class PreferenceItemNotFoundError(ValueError):
    pass


class PreferenceService:
    def __init__(self, repository: PreferenceRepository) -> None:
        self._repository = repository

    async def list_constraints(
        self,
        user_id: UUID,
    ) -> list[SchedulingConstraint]:
        return await self._repository.list_constraints(user_id)

    async def create_constraint(
        self,
        user_id: UUID,
        request: ConstraintCreate,
    ) -> SchedulingConstraint:
        return await self._repository.add_constraint(
            SchedulingConstraint(
                user_id=user_id,
                **request.model_dump(),
            )
        )

    async def delete_constraint(
        self,
        user_id: UUID,
        constraint_id: UUID,
    ) -> None:
        removed = await self._repository.delete_constraint(
            user_id,
            constraint_id,
        )
        if not removed:
            raise PreferenceItemNotFoundError

    async def list_preferences(
        self,
        user_id: UUID,
    ) -> list[SchedulingPreference]:
        return await self._repository.list_preferences(user_id)

    async def create_preference(
        self,
        user_id: UUID,
        request: PreferenceCreate,
    ) -> SchedulingPreference:
        return await self._repository.add_preference(
            SchedulingPreference(
                user_id=user_id,
                **request.model_dump(),
            )
        )

    async def delete_preference(
        self,
        user_id: UUID,
        preference_id: UUID,
    ) -> None:
        removed = await self._repository.delete_preference(
            user_id,
            preference_id,
        )
        if not removed:
            raise PreferenceItemNotFoundError
