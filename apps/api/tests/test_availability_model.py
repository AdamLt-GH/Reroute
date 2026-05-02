from app.models.availability import AvailabilityWindow


def test_availability_window_tracks_a_local_weekday_and_time() -> None:
    columns = AvailabilityWindow.__table__.c

    assert "day_of_week" in columns
    assert "start_time" in columns
    assert "end_time" in columns


def test_availability_window_can_have_an_effective_date_range() -> None:
    columns = AvailabilityWindow.__table__.c

    assert columns.effective_from.nullable
    assert columns.effective_until.nullable
