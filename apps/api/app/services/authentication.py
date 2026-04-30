from dataclasses import dataclass
from datetime import timedelta

from app.auth.passwords import PasswordService
from app.models.user import User
from app.repositories.sessions import SessionRepository
from app.repositories.users import UserRepository


class InvalidCredentialsError(ValueError):
    pass


@dataclass(frozen=True)
class LoginResult:
    user: User
    token: str


class AuthenticationService:
    def __init__(
        self,
        users: UserRepository,
        sessions: SessionRepository,
        passwords: PasswordService,
        *,
        session_days: int,
    ) -> None:
        self._users = users
        self._sessions = sessions
        self._passwords = passwords
        self._session_lifetime = timedelta(days=session_days)

    async def login(self, email: str, password: str) -> LoginResult:
        user = await self._users.find_by_email(email)

        if user is None or not self._passwords.verify(user.password_hash, password):
            raise InvalidCredentialsError
        if not user.is_active:
            raise InvalidCredentialsError

        _, token = await self._sessions.create(
            user.id,
            lifetime=self._session_lifetime,
        )
        return LoginResult(user=user, token=token)

    async def current_user(self, token: str) -> User | None:
        return await self._sessions.find_user(token)

    async def logout(self, token: str) -> None:
        await self._sessions.delete(token)
