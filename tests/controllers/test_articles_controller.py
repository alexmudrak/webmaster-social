from unittest.mock import AsyncMock, patch

import pytest
from controllers.articles_controller import ArticlesController
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def mock_articles_repo():
    with patch("controllers.articles_controller.ArticlesRepository") as mock:
        mock.return_value.retrieve_all_articles = AsyncMock(return_value=[])
        mock.return_value.retrieve_article_by_id = AsyncMock()
        yield mock


@pytest.fixture
def mock_settings_repo():
    with patch("controllers.articles_controller.SettingsRepository") as mock:
        mock.return_value.retrieve_settings_by_project_id = AsyncMock()
        mock.return_value.retrieve_setting_by_project_id_and_network_name = (
            AsyncMock()
        )
        yield mock


@pytest.fixture
def mock_social_networks_controller():
    with patch(
        "controllers.articles_controller.SocialNetworksController"
    ) as mock:
        mock.return_value.run_task_send_article_to_networks = AsyncMock()
        mock.return_value.run_task_send_article_to_network = AsyncMock()
        yield mock


@pytest.fixture
def mock_async_session():
    return AsyncMock(spec=AsyncSession)


@pytest.mark.asyncio
async def test_get_all_objects(mock_async_session, mock_articles_repo):
    controller = ArticlesController(mock_async_session)
    result = await controller.get_all_objects()
    assert result == []
    mock_articles_repo.return_value.retrieve_all_articles.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_article_to_networks(
    mock_async_session,
    mock_articles_repo,
    mock_settings_repo,
    mock_social_networks_controller,
):
    _ = mock_articles_repo, mock_settings_repo
    controller = ArticlesController(mock_async_session)
    await controller.send_article_to_networks(1)
    task_run = mock_social_networks_controller.return_value
    task_run.run_task_send_article_to_networks.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_article_to_network(
    mock_async_session,
    mock_articles_repo,
    mock_settings_repo,
    mock_social_networks_controller,
):
    _ = mock_articles_repo, mock_settings_repo
    controller = ArticlesController(mock_async_session)
    await controller.send_article_to_network(1, "network_name")
    task_run = mock_social_networks_controller.return_value
    task_run.run_task_send_article_to_network.assert_awaited_once()
