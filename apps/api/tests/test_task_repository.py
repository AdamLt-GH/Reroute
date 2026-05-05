from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import TaskDependency
from app.repositories.tasks import TaskDependencyRepository


@pytest.mark.asyncio
async def test_dependency_repository_flushes_new_links() -> None:
    session = AsyncMock(spec=AsyncSession)
    dependency = TaskDependency(
        prerequisite_id=uuid4(),
        dependent_id=uuid4(),
    )

    result = await TaskDependencyRepository(session).add(dependency)

    assert result is dependency
    session.add.assert_called_once_with(dependency)
    session.flush.assert_awaited_once()
    session.refresh.assert_awaited_once_with(dependency)
