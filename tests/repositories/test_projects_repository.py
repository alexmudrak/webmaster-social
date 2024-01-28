from unittest.mock import AsyncMock, MagicMock

import pytest
from models.project import Project
from repositories.projects_repository import ProjectsRepository
from schemas.project_schema import ProjectRead
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def projects_repository(mock_async_session):
    return ProjectsRepository(mock_async_session)


@pytest.mark.asyncio
async def test_retrieve_all_project_objects(
    projects_repository, mock_async_session
):
    test_projects = [
        ProjectRead.model_validate(
            Project(
                id=1,
                name="Test Project 1",
                url="http://example-1",
            )
        ),
        ProjectRead.model_validate(
            Project(
                id=2,
                name="Test Project 2",
                url="http://example-2",
            )
        ),
    ]
    mock_exec = MagicMock()
    mock_exec.unique.return_value.all.return_value = test_projects
    mock_async_session.exec.return_value = mock_exec

    result = await projects_repository.retrieve_all_project_objects()

    assert result == test_projects
    mock_async_session.exec.assert_awaited_once()
