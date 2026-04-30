import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import AuthSession


def generate_session_token() -> str:
    return secrets.token_urlsafe(32)


def hash_session_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class SessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: UUID,
        *,
        lifetime: timedelta,
    ) -> tuple[AuthSession, str]:
        token = generate_session_token()
        now = datetime.now(UTC)
        auth_session = AuthSession(
            user_id=user_id,
            token_hash=hash_session_token(token),
            expires_at=now + lifetime,
            last_used_at=now,
        )
        self._session.add(auth_session)
        await self._session.flush()
        return auth_session, token

    async def find_active(self, token: str) -> AuthSession | None:
        statement = select(AuthSession).where(
            AuthSession.token_hash == hash_session_token(token),
            AuthSession.expires_at > datetime.now(UTC),
        )
        return await self._session.scalar(statement)

    async def delete(self, token: str) -> None:
        statement = delete(AuthSession).where(
            AuthSession.token_hash == hash_session_token(token)
        )
        await self._session.execute(statement)
