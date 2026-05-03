from uuid import UUID

from app.models.availability import AvailabilityWindow
from app.repositories.availability import AvailabilityRepository
from app.schemas.availability import AvailabilityCreate


class AvailabilityNotFoundError(ValueError):
    pass


class AvailabilityService:
    def __init__(self, repository: AvailabilityRepository) -> None:
        self._repository = repository

    async def list(self, user_id: UUID) -> list[AvailabilityWindow]:
        return await self._repository.list_for_user(user_id)

    async def create(
        self,
        user_id: UUID,
        request: AvailabilityCreate,
    ) -> AvailabilityWindow:
        return await self._repository.add(
            AvailabilityWindow(
                user_id=user_id,
                **request.model_dump(),
            )
        )

    async def delete(self, user_id: UUID, window_id: UUID) -> None:
        if not await self._repository.delete_for_user(user_id, window_id):
            raise AvailabilityNotFoundError
