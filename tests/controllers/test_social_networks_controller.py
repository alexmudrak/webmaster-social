from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from controllers.social_networks_controller import SocialNetworksController
from httpx import AsyncClient
from models.article import Article
from models.article_status import ArticleStatus
from models.setting import Setting
from services.notification.notification_service import NotificationSender
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
async def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    yield session


@pytest.fixture
def article():
    return MagicMock(spec=Article)


@pytest.fixture
def setting():
    return MagicMock(spec=Setting)


@pytest.fixture
def publish_article_status():
    return MagicMock(spec=ArticleStatus)


@pytest.mark.asyncio
async def test_run_task_send_article_to_networks(
    mock_async_session, article, setting
):
    with patch(
        "controllers.social_networks_controller.get_request_client"
    ) as mock_get_request_client, patch(
        "controllers.social_networks_controller.get_or_create",
        new_callable=AsyncMock,
    ) as mock_get_or_create, patch(
        "controllers.social_networks_controller.send_to_network",
        new_callable=AsyncMock,
    ) as mock_send_to_network, patch.object(
        NotificationSender, "send_message", new_callable=AsyncMock
    ) as mock_notification_sender:
        mock_get_request_client.return_value.__aenter__.return_value = (
            AsyncMock(spec=AsyncClient)
        )

        controller = SocialNetworksController(mock_async_session)
        await controller.run_task_send_article_to_networks(article, [setting])

        mock_get_request_client.assert_called_once()
        mock_get_or_create.assert_called()
        mock_send_to_network.assert_called()
        mock_notification_sender.assert_called_once()


@pytest.mark.asyncio
async def test_run_task_send_article_to_network(
    mock_async_session, article, setting
):
    with patch(
        "controllers.social_networks_controller.get_request_client"
    ) as mock_get_request_client, patch(
        "controllers.social_networks_controller.get_or_create",
        new_callable=AsyncMock,
    ) as mock_get_or_create, patch(
        "controllers.social_networks_controller.send_to_network",
        new_callable=AsyncMock,
    ) as mock_send_to_network, patch.object(
        NotificationSender, "send_message", new_callable=AsyncMock
    ) as mock_notification_sender:
        mock_get_request_client.return_value.__aenter__.return_value = (
            AsyncMock(spec=AsyncClient)
        )

        controller = SocialNetworksController(mock_async_session)
        await controller.run_task_send_article_to_network(article, setting)

        mock_get_request_client.assert_called_once()
        mock_get_or_create.assert_called()
        mock_send_to_network.assert_called()
        mock_notification_sender.assert_called_once()


@pytest.mark.asyncio
async def test_get_article_no_match():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_exec = MagicMock()
    mock_exec.unique.return_value.first.return_value = None
    mock_session.exec.return_value = mock_exec

    controller = SocialNetworksController(session=mock_session)

    article = await controller.get_article(
        project_id=1,
        networks_count=1,
    )

    assert article is None


@pytest.mark.asyncio
async def test_get_article_with_match():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_exec = MagicMock()
    mock_article = MagicMock(spec=Article)
    mock_exec.unique.return_value.first.return_value = mock_article
    mock_session.exec.return_value = mock_exec

    controller = SocialNetworksController(session=mock_session)

    article = await controller.get_article(
        project_id=1,
        networks_count=1,
    )

    assert article is mock_article


@pytest.mark.asyncio
async def test_get_article_with_setting_exists():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_exec = MagicMock()
    mock_article = MagicMock(spec=Article)
    mock_exec.unique.return_value.first.return_value = mock_article
    mock_session.exec.return_value = mock_exec

    controller = SocialNetworksController(session=mock_session)
    mock_setting = MagicMock(spec=Setting)
    mock_setting.id = 1

    article = await controller.get_article(
        project_id=1,
        networks_count=1,
        setting_exists=mock_setting,
    )

    assert article is mock_article


@pytest.mark.asyncio
async def test_get_networks_config_no_settings():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_exec = MagicMock()
    mock_exec.unique.return_value.all.return_value = []
    mock_session.exec.return_value = mock_exec

    controller = SocialNetworksController(session=mock_session)

    settings = await controller.get_networks_config(project_id=1)

    assert settings == []


@pytest.mark.asyncio
async def test_get_networks_config_with_settings():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_exec = MagicMock()
    mock_setting_1 = MagicMock(spec=Setting)
    mock_setting_2 = MagicMock(spec=Setting)
    mock_exec.unique.return_value.all.return_value = [
        mock_setting_1,
        mock_setting_2,
    ]
    mock_session.exec.return_value = mock_exec

    controller = SocialNetworksController(session=mock_session)

    settings = await controller.get_networks_config(project_id=1)

    assert settings == [mock_setting_1, mock_setting_2]


@pytest.mark.asyncio
async def test_create_network_tasks_no_network_name():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_send_to_single_network = AsyncMock()
    mock_setting = MagicMock(spec=Setting)
    mock_setting.id = 1
    mock_article = MagicMock(spec=Article)
    client = AsyncClient()

    controller = SocialNetworksController(session=mock_session)
    controller.send_to_single_network = mock_send_to_single_network

    tasks = controller.create_network_tasks(
        network_name=None,
        setting_exists=None,
        networks_config=[mock_setting],
        done_status=set(),
        client=client,
        article=mock_article,
    )

    assert len(tasks) == 1


@pytest.mark.asyncio
async def test_create_network_tasks_with_network_name_and_setting_exists():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_send_to_single_network = AsyncMock()
    mock_setting = MagicMock(spec=Setting)
    mock_setting.id = 1
    mock_article = MagicMock(spec=Article)
    client = AsyncClient()

    controller = SocialNetworksController(session=mock_session)
    controller.send_to_single_network = mock_send_to_single_network

    tasks = controller.create_network_tasks(
        network_name="TestNetwork",
        setting_exists=mock_setting,
        networks_config=[],
        done_status=set(),
        client=client,
        article=mock_article,
    )

    assert len(tasks) == 1


@pytest.mark.asyncio
async def test_get_setting_by_name_none():
    mock_session = AsyncMock(spec=AsyncSession)
    controller = SocialNetworksController(session=mock_session)
    mock_setting = MagicMock(spec=Setting)
    mock_setting.name = "TestNetwork"
    settings = [mock_setting]

    result = await controller.get_setting_by_name(
        settings,
        None,
    )
    assert result is None


@pytest.mark.asyncio
async def test_get_setting_by_name_exists():
    mock_session = AsyncMock(spec=AsyncSession)
    controller = SocialNetworksController(session=mock_session)
    mock_setting = MagicMock(spec=Setting)
    mock_setting.name = "TestNetwork"
    settings = [mock_setting]

    result = await controller.get_setting_by_name(
        settings,
        "TestNetwork",
    )
    assert result == mock_setting


@pytest.mark.asyncio
async def test_get_setting_by_name_not_exists():
    mock_session = AsyncMock(spec=AsyncSession)
    controller = SocialNetworksController(session=mock_session)
    mock_setting = MagicMock(spec=Setting)
    mock_setting.name = "TestNetwork"
    settings = [mock_setting]

    result = await controller.get_setting_by_name(
        settings,
        "OtherNetwork",
    )
    assert result is None


def test_get_done_status():
    mock_session = AsyncMock(spec=AsyncSession)
    controller = SocialNetworksController(session=mock_session)
    mock_article = MagicMock(spec=Article)
    mock_published_done = MagicMock(
        spec=ArticleStatus,
        status="DONE",
        try_count=1,
        setting_id=1,
    )
    mock_published_error = MagicMock(
        spec=ArticleStatus,
        status="ERROR",
        try_count=3,
        setting_id=2,
    )
    mock_published_retry = MagicMock(
        spec=ArticleStatus,
        status="ERROR",
        try_count=2,
        setting_id=3,
    )
    mock_article.published = [
        mock_published_done,
        mock_published_error,
        mock_published_retry,
    ]

    done_status = controller.get_done_status(mock_article)
    assert done_status == {1, 2}


@pytest.mark.asyncio
async def test_send_article_to_networks_no_network_name():
    mock_session = AsyncMock(spec=AsyncSession)
    controller = SocialNetworksController(session=mock_session)
    controller.get_networks_config = AsyncMock()
    controller.get_setting_by_name = AsyncMock(return_value=None)
    controller.get_article = AsyncMock()
    controller.get_done_status = MagicMock()
    controller.create_network_tasks = MagicMock()
    controller.send_notification = AsyncMock()
    controller.session.close = AsyncMock()
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch(
        "controllers.social_networks_controller.get_request_client",
        return_value=mock_client,
    ):
        await controller.send_article_to_networks(project_id=123)

    controller.get_networks_config.assert_awaited_once()
    controller.get_setting_by_name.assert_awaited_once()
    controller.get_article.assert_awaited_once()
    controller.session.close.assert_awaited()
