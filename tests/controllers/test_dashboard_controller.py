from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from controllers.dashboard_controller import DashboardController
from schemas.dashboard_schema import (
    DashboardCardData,
    DashboardNetworkStatusesData,
    DashboardStatusesData,
)
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    return session


class MockArticle:
    def __init__(self, network_statuses):
        self.network_statuses = network_statuses


class MockNetworkStatus:
    def __init__(self, status):
        self.status = status


articles = [
    MockArticle(network_statuses=[MockNetworkStatus(status="DONE")]),
]
projects = [...]
settings = [...]


@pytest.mark.asyncio
async def test_get_cards_data(mock_async_session):
    with patch(
        "controllers.dashboard_controller.ArticlesRepository"
    ) as mock_articles_repo, patch(
        "controllers.dashboard_controller.ProjectsRepository"
    ) as mock_projects_repo, patch(
        "controllers.dashboard_controller.SettingsRepository"
    ) as mock_settings_repo:
        mock_articles_repo.return_value.retrieve_all_articles = AsyncMock(
            return_value=articles
        )

        mock_projects_repo.return_value.retrieve_all_project_objects = (
            AsyncMock(return_value=projects)
        )

        mock_settings_repo.return_value.retrieve_unique_settings = AsyncMock(
            return_value=settings
        )

        dashboard_controller = DashboardController(
            db_manager=mock_async_session
        )
        result = await dashboard_controller.get_cards_data()

        assert isinstance(result, DashboardCardData)
        assert result.articles.total == len(articles)


@pytest.mark.asyncio
async def test_get_statuses_data(mock_async_session):
    mock_ids = [1, 2, 3, 4, 5]

    project = MagicMock()
    project.name = "Project mock"

    networks_setting = MagicMock
    networks_setting.name = "Network mock"

    mock_articles = [
        MagicMock(
            spec=DashboardStatusesData,
            id=i,
            title=f"Article {i}",
            project=project,
            published=[
                MagicMock(
                    spec=DashboardNetworkStatusesData,
                    id=j,
                    created=datetime.now(),
                    networks_setting=networks_setting,
                    status="Status",
                    status_text="Status Text",
                )
                for j in range(5)
            ],
        )
        for i in mock_ids
    ]

    with patch(
        "controllers.dashboard_controller.ArticlesStatusesRepository.retrieve_last_5_id_articles_statuses",
        new_callable=AsyncMock,
        return_value=mock_ids,
    ), patch(
        "controllers.dashboard_controller.ArticlesRepository.retrieve_article_by_list_id",
        new_callable=AsyncMock,
        return_value=mock_articles,
    ):
        dashboard_controller = DashboardController(
            db_manager=mock_async_session
        )

        results = await dashboard_controller.get_statuses_data()

        assert isinstance(results, list)
        assert all(isinstance(item, DashboardStatusesData) for item in results)
        assert len(results) == len(mock_articles)
        assert results == sorted(results, key=lambda x: x.date, reverse=True)
