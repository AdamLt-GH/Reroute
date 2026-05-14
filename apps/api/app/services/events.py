from uuid import UUID, uuid4

from app.models.event import FixedEvent
from app.repositories.events import EventRepository
from app.scheduling.domain.events import (
    FixedEventWindow,
    events_overlap,
)
from app.schemas.events import FixedEventCreate


class EventConflictError(ValueError):
    pass


class EventNotFoundError(ValueError):
    pass


def to_event_window(event: FixedEvent) -> FixedEventWindow:
    return FixedEventWindow(
        id=event.id,
        title=event.title,
        start=event.start_at,
        end=event.end_at,
        travel_before_minutes=event.travel_before_minutes,
        travel_after_minutes=event.travel_after_minutes,
    )


class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self._repository = repository

    async def list(self, user_id: UUID) -> list[FixedEvent]:
        return await self._repository.list_for_user(user_id)

    async def create(
        self,
        user_id: UUID,
        request: FixedEventCreate,
    ) -> FixedEvent:
        candidate = FixedEvent(
            id=uuid4(),
            user_id=user_id,
            source="manual",
            **request.model_dump(),
        )
        candidate_window = to_event_window(candidate)

        for existing in await self._repository.list_for_user(user_id):
            if events_overlap(candidate_window, to_event_window(existing)):
                raise EventConflictError

        return await self._repository.add(candidate)

    async def update(
        self,
        user_id: UUID,
        event_id: UUID,
        request: FixedEventCreate,
    ) -> FixedEvent:
        event = await self._repository.find_for_user(user_id, event_id)
        if event is None:
            raise EventNotFoundError

        for field, value in request.model_dump().items():
            setattr(event, field, value)

        for existing in await self._repository.list_for_user(user_id):
            if existing.id != event_id and events_overlap(
                to_event_window(event),
                to_event_window(existing),
            ):
                raise EventConflictError

        return await self._repository.save(event)

    async def delete(self, user_id: UUID, event_id: UUID) -> None:
        if not await self._repository.delete_for_user(user_id, event_id):
            raise EventNotFoundError
