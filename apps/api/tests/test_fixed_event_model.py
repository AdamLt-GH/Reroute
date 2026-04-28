from app.models.event import FixedEvent


def test_fixed_event_keeps_travel_time_separate() -> None:
    columns = FixedEvent.__table__.c

    assert "travel_before_minutes" in columns
    assert "travel_after_minutes" in columns


def test_fixed_event_is_locked_by_default() -> None:
    locked = FixedEvent.__table__.c.locked

    assert locked.default is not None
    assert locked.default.arg is True
