from datetime import UTC, datetime
from uuid import uuid4

from app.scheduling.domain.events import FixedEventWindow
from app.scheduling.domain.recurrence import expand_recurrence


def test_weekly_event_expands_only_inside_the_horizon() -> None:
    event = FixedEventWindow(
        id=uuid4(),
        title="Class",
        start=datetime(2026, 5, 4, 9, tzinfo=UTC),
        end=datetime(2026, 5, 4, 11, tzinfo=UTC),
    )

    occurrences = expand_recurrence(
        event,
        "FREQ=WEEKLY;COUNT=4",
        horizon_start=datetime(2026, 5, 1, tzinfo=UTC),
        horizon_end=datetime(2026, 5, 20, tzinfo=UTC),
    )

    assert [item.start.day for item in occurrences] == [4, 11, 18]
    assert all((item.end - item.start).seconds == 7200 for item in occurrences)
