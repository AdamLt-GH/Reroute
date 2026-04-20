from datetime import time

from app.models.user import User, UserSettings


def test_user_model_keeps_the_initial_sydney_timezone() -> None:
    timezone_column = User.__table__.c.timezone

    assert timezone_column.default is not None
    assert timezone_column.default.arg == "Australia/Sydney"


def test_user_email_is_unique_and_indexed() -> None:
    email_column = User.__table__.c.email

    assert email_column.unique
    assert email_column.index


def test_scheduling_settings_start_with_reasonable_defaults() -> None:
    table = UserSettings.__table__

    assert table.c.preferred_day_start.default.arg == time(8, 0)
    assert table.c.preferred_day_end.default.arg == time(21, 0)
    assert table.c.maximum_daily_work_minutes.default.arg == 480
    assert table.c.schedule_change_weight.default.arg == 1.0
