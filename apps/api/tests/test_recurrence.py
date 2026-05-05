from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.scheduling.domain.events import FixedEventWindow
from app.scheduling.domain.recurrence import RecurrenceError, expand_recurrence


def make_event() -> FixedEventWindow:
    return FixedEventWindow(
        id=uuid4(),
        title="Class",
        start=datetime(2026, 5, 4, 9, tzinfo=UTC),
        end=datetime(2026, 5, 4, 11, tzinfo=UTC),
    )


def test_weekly_event_expands_only_inside_the_horizon() -> None:
    occurrences = expand_recurrence(
        make_event(),
        "FREQ=WEEKLY;COUNT=4",
        horizon_start=datetime(2026, 5, 1, tzinfo=UTC),
        horizon_end=datetime(2026, 5, 20, tzinfo=UTC),
    )

    assert [item.start.day for item in occurrences] == [4, 11, 18]
    assert all((item.end - item.start).seconds == 7200 for item in occurrences)


def test_recurrence_stops_rules_that_create_too_many_events() -> None:
    with pytest.raises(
        RecurrenceError,
        match="recurrence creates too many events",
    ):
        expand_recurrence(
            make_event(),
            "FREQ=MINUTELY",
            horizon_start=datetime(2026, 5, 4, tzinfo=UTC),
            horizon_end=datetime(2026, 5, 5, tzinfo=UTC),
            maximum_occurrences=20,
        )


def test_recurrence_rejects_an_invalid_occurrence_limit() -> None:
    with pytest.raises(
        RecurrenceError,
        match="maximum occurrences must be positive",
    ):
        expand_recurrence(
            make_event(),
            "FREQ=WEEKLY",
            horizon_start=datetime(2026, 5, 1, tzinfo=UTC),
            horizon_end=datetime(2026, 5, 20, tzinfo=UTC),
            maximum_occurrences=0,
        )
