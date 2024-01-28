from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from models.publish_article_status import PublishArticleStatus
from services.notification.notification_data import NotificationData
from services.notification.senders.telegram_bot_sender import TelegramBotSender


@pytest.fixture
def mock_request_client():
    with patch(
        "services.notification.senders.telegram_bot_sender.get_request_client"
    ) as mock:
        mock.return_value = AsyncMock()
        yield mock


@pytest.mark.asyncio
async def test_telegram_bot_sender_send(mock_request_client):
    token = "test_token"
    admin_id = "test_admin_id"
    sender = TelegramBotSender(token=token, admin_id=admin_id)

    message = NotificationData(
        project_name="Test Project",
        article_title="Test Article",
        article_url="http://testurl.com",
        message="Test Status Message",
        done_status_count=1,
        fail_status_count=0,
        publish_statuses={
            "network1": MagicMock(spec=PublishArticleStatus, status="DONE"),
            "network2": MagicMock(spec=PublishArticleStatus, status="FAIL"),
        },
    )

    await sender.send(message)

    expected_url = f"https://api.telegram.org/bot{token}/sendMessage"
    expected_data = {
        "chat_id": admin_id,
        "text": (
            "Test Project\n\n"
            "[Test Article](http://testurl\\.com)\n\n"
            "✅ *DONE*: 1 / 🛑 *FAIL*: 0\n\n"
            "Test Status Message"
        ),
        "parse_mode": "MarkdownV2",
    }

    mock_request_client.return_value.__aenter__.return_value.post.assert_awaited_once_with(
        url=expected_url, data=expected_data
    )
