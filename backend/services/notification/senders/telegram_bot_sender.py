from core.logger import get_logger
from services.notification.notification_data import NotificationData
from services.notification.senders.abstract_sender import (
    AbstractNotificationSender,
)
from utils.request_client import get_request_client
from utils.string_handler import escape_markdown

logger = get_logger(__name__)


class TelegramBotSender(AbstractNotificationSender):
    def __init__(self, token: str, admin_id: str):
        self.token = token
        self.admin_id = admin_id
        self.post_endpoint = "https://api.telegram.org/bot{token}/sendMessage"

    async def send(self, message: NotificationData):
        project_name = await escape_markdown(message.project_name)
        article_title = await escape_markdown(message.article_title)
        article_url = await escape_markdown(message.article_url)
        published_status = await escape_markdown(message.message)
        published_status_count = (
            f"✅ *DONE*: {message.done_status_count} / "
            f"🛑 *FAIL*: {message.fail_status_count}"
        )

        text = (
            f"{project_name}\n\n"
            f"[{article_title}]({article_url})\n\n"
            f"{published_status_count}\n\n"
            f"{published_status}"
        )

        data = {
            "chat_id": self.admin_id,
            "text": text,
            "parse_mode": "MarkdownV2",
        }

        async with await get_request_client() as client:
            response = await client.post(
                url=self.post_endpoint.format(token=self.token),
                data=data,
            )
            logger.debug(response.json())
