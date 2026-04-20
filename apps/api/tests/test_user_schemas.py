import pytest
from pydantic import ValidationError

from app.schemas.users import UserRegistration


def test_registration_normalises_the_email_address() -> None:
    request = UserRegistration(
        email="Adam@Example.COM",
        password="a useful password",
        display_name="Adam",
    )

    assert request.email == "Adam@example.com"


def test_registration_requires_a_display_name() -> None:
    with pytest.raises(ValidationError):
        UserRegistration(
            email="adam@example.com",
            password="a useful password",
            display_name="",
        )
