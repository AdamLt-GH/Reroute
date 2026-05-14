from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.models.event import FixedEvent
from app.repositories.events import EventRepository
from app.schemas.events import FixedEventCreate
from app.services.events import EventConflictError, EventService


def event_request(start_hour: int, end_hour: int) -> FixedEventCreate:
    return FixedEventCreate(
        title="Commitment",
        start_at=datetime(2026, 5, 5, start_hour, tzinfo=UTC),
        end_at=datetime(2026, 5, 5, end_hour, tzinfo=UTC),
    )


@pytest.mark.asyncio
async def test_event_service_creates_a_non_conflicting_event() -> None:
    repository = AsyncMock(spec=EventRepository)
    repository.list_for_user.return_value = []
    repository.add.side_effect = lambda event: event

    event = await EventService(repository).create(
        uuid4(),
        event_request(9, 10),
    )

    assert event.source == "manual"
    repository.add.assert_awaited_once()


@pytest.mark.asyncio
async def test_event_service_rejects_a_conflicting_event() -> None:
    repository = AsyncMock(spec=EventRepository)
    repository.list_for_user.return_value = [
        FixedEvent(
            id=uuid4(),
            user_id=uuid4(),
            title="Existing event",
            start_at=datetime(2026, 5, 5, 9, tzinfo=UTC),
            end_at=datetime(2026, 5, 5, 10, tzinfo=UTC),
            travel_before_minutes=0,
            travel_after_minutes=0,
        )
    ]

    with pytest.raises(EventConflictError):
        await EventService(repository).create(
            uuid4(),
            event_request(9, 11),
        )


@pytest.mark.asyncio
async def test_event_service_updates_an_owned_event() -> None:
    user_id = uuid4()
    event = FixedEvent(
        id=uuid4(),
        user_id=user_id,
        title="Old title",
        start_at=datetime(2026, 5, 5, 9, tzinfo=UTC),
        end_at=datetime(2026, 5, 5, 10, tzinfo=UTC),
        travel_before_minutes=0,
        travel_after_minutes=0,
    )
    repository = AsyncMock(spec=EventRepository)
    repository.find_for_user.return_value = event
    repository.list_for_user.return_value = [event]
    repository.save.side_effect = lambda saved: saved

    updated = await EventService(repository).update(
        user_id,
        event.id,
        event_request(11, 12),
    )

    assert updated.title == "Commitment"
    assert updated.start_at.hour == 11
