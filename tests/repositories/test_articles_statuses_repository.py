from unittest.mock import AsyncMock, MagicMock

import pytest
from repositories.articles_statuses_repository import (
    ArticlesStatusesRepository,
)
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def mock_async_session():
    # TODO: Move to conftest file and refactor each other
    #       tests
    session = AsyncMock(spec=AsyncSession)
    session.exec.return_value = MagicMock()
    return session


@pytest.fixture
def articles_statuses_repository(mock_async_session):
    return ArticlesStatusesRepository(mock_async_session)


@pytest.mark.asyncio
async def test_retrieve_last_5_id_articles_statuses(
    articles_statuses_repository,
    mock_async_session,
):
    test_article_ids = [
        5,
        4,
        3,
        2,
        1,
    ]
    session = mock_async_session.exec.return_value.unique
    session.return_value.all.return_value = test_article_ids + [
        0,
        -1,
    ]

    repo = articles_statuses_repository.retrieve_last_5_id_articles_statuses

    result = await repo()

    assert result == test_article_ids
    mock_async_session.exec.assert_awaited_once()
