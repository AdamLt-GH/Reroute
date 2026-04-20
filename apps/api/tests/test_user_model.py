from app.models.user import User


def test_user_model_keeps_the_initial_sydney_timezone() -> None:
    timezone_column = User.__table__.c.timezone

    assert timezone_column.default is not None
    assert timezone_column.default.arg == "Australia/Sydney"


def test_user_email_is_unique_and_indexed() -> None:
    email_column = User.__table__.c.email

    assert email_column.unique
    assert email_column.index
