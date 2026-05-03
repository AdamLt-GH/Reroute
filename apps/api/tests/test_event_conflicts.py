from datetime import UTC, datetime
from uuid import uuid4

from app.scheduling.domain.events import (
    FixedEventWindow,
    events_overlap,
    find_event_conflicts,
)


def event(
    start_hour: int,
    end_hour: int,
    *,
    travel_before: int = 0,
    travel_after: int = 0,
) -> FixedEventWindow:
    return FixedEventWindow(
        id=uuid4(),
        title="Commitment",
        start=datetime(2026, 5, 3, start_hour, tzinfo=UTC),
        end=datetime(2026, 5, 3, end_hour, tzinfo=UTC),
        travel_before_minutes=travel_before,
        travel_after_minutes=travel_after,
    )


def test_adjacent_events_do_not_overlap() -> None:
    assert not events_overlap(event(9, 10), event(10, 11))


def test_travel_time_can_create_a_conflict() -> None:
    first = event(9, 10, travel_after=30)
    second = event(10, 11)

    assert events_overlap(first, second)
    assert find_event_conflicts([first, second]) == [(first.id, second.id)]
