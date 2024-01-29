from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from models.article_status import ArticleStatus
from services.notification.notification_data import NotificationData
from services.notification.notification_service import NotificationSender
from services.notification.senders.telegram_bot_sender import TelegramBotSender


@pytest.fixture
def mock_telegram_bot_send():
    with patch.object(
        TelegramBotSender, "send", new_callable=AsyncMock
    ) as mock_send:
        yield mock_send


@pytest.fixture
def notification_sender(mock_telegram_bot_send):
    _ = mock_telegram_bot_send
    with patch(
        "services.notification.notification_service.Settings"
    ) as mock_settings:
        mock_variables = MagicMock()
        mock_variables.TELEGRAM_ADMIN_ID = "admin_id"
        mock_variables.TELEGRAM_BOT_TOKEN = "token"
        mock_settings.return_value = mock_variables
        yield NotificationSender()


@pytest.mark.asyncio
async def test_prepare_message(notification_sender):
    data = NotificationData(
        project_name="",
        article_title="",
        article_url="",
        message="",
        publish_statuses={
            "network1": MagicMock(spec=ArticleStatus, status="DONE"),
            "network2": MagicMock(spec=ArticleStatus, status="FAIL"),
        },
    )

    result = await notification_sender.prepare_message(data)

    assert result.message == "\t- network1 - DONE\n\t- network2 - FAIL"
    assert result.done_status_count == 1
    assert result.fail_status_count == 1


@pytest.mark.asyncio
async def test_send_message(
    notification_sender,
    mock_telegram_bot_send,
):
    data = NotificationData(
        project_name="",
        article_title="",
        article_url="",
        message="",
        publish_statuses={
            "network1": AsyncMock(spec=ArticleStatus, status="DONE"),
            "network2": AsyncMock(spec=ArticleStatus, status="FAIL"),
        },
    )

    prepared_data = await notification_sender.prepare_message(data)

    await notification_sender.send_message(prepared_data)

    mock_telegram_bot_send.assert_awaited_with(prepared_data)
