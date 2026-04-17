from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError


class PasswordPolicyError(ValueError):
    pass


def validate_password(password: str) -> None:
    # keep this simple so the validation message is actually useful
    if len(password) < 10:
        raise PasswordPolicyError("password must be at least 10 characters")
    if len(password) > 128:
        raise PasswordPolicyError("password must be no more than 128 characters")
    if password.isspace():
        raise PasswordPolicyError("password cannot only contain spaces")


class PasswordService:
    def __init__(self) -> None:
        self._hasher = PasswordHasher()

    def hash(self, password: str) -> str:
        validate_password(password)
        return self._hasher.hash(password)

    def verify(self, password_hash: str, password: str) -> bool:
        try:
            return self._hasher.verify(password_hash, password)
        except (InvalidHashError, VerificationError):
            return False
