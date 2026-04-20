from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.users import UserRepository, normalise_email


def test_email_normalisation_is_consistent() -> None:
    assert normalise_email("  Adam@Example.COM ") == "adam@example.com"


@pytest.mark.asyncio
async def test_missing_user_returns_none() -> None:
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = None

    user = await UserRepository(session).find_by_email("adam@example.com")

    assert user is None
    session.scalar.assert_awaited_once()
