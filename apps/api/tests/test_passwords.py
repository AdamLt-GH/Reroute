import pytest

from app.auth.passwords import PasswordPolicyError, PasswordService


def test_password_hashes_do_not_contain_the_original_password() -> None:
    service = PasswordService()

    password_hash = service.hash("correct horse battery staple")

    assert "correct horse battery staple" not in password_hash
    assert service.verify(password_hash, "correct horse battery staple")


def test_incorrect_and_invalid_passwords_are_rejected() -> None:
    service = PasswordService()
    password_hash = service.hash("the actual password")

    assert not service.verify(password_hash, "something else")
    assert not service.verify("not an argon hash", "the actual password")


@pytest.mark.parametrize(
    ("password", "message"),
    [
        ("short", "at least 10 characters"),
        (" " * 12, "cannot only contain spaces"),
        ("a" * 129, "no more than 128 characters"),
    ],
)
def test_password_policy_rejects_unhelpful_passwords(
    password: str,
    message: str,
) -> None:
    with pytest.raises(PasswordPolicyError, match=message):
        PasswordService().hash(password)
