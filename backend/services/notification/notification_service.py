import asyncio

from core.settings import Settings
from services.notification.notification_data import NotificationData
from services.notification.senders.telegram_bot_sender import TelegramBotSender


class NotificationSender:
    """
    This class is responsible for sending notifications through various
    configured services. It currently supports sending notifications via
    Telegram if the necessary settings are provided.
    """

    def __init__(self):
        self.senders = []
        self.settings = Settings()

        if (
            self.settings.TELEGRAM_ADMIN_ID
            and self.settings.TELEGRAM_BOT_TOKEN
        ):
            self.senders.append(
                TelegramBotSender(
                    token=self.settings.TELEGRAM_BOT_TOKEN,
                    admin_id=self.settings.TELEGRAM_ADMIN_ID,
                )
            )

    async def prepare_message(
        self, data: NotificationData
    ) -> NotificationData:
        statuses = [
            (
                f"\t- {network_name} - "
                f"{'DONE' if status.status == 'DONE' else 'FAIL'}"
            )
            for network_name, status in data.publish_statuses.items()
        ]

        data.message = "\n".join(statuses)
        data.done_status_count = sum(
            1
            for status in data.publish_statuses.values()
            if status.status == "DONE"
        )
        data.fail_status_count = (
            len(data.publish_statuses) - data.done_status_count
        )
        return data

    async def send_message(self, data: NotificationData) -> None:
        message = await self.prepare_message(data)
        tasks = [
            asyncio.create_task(sender.send(message))
            for sender in self.senders
        ]
        await asyncio.gather(*tasks)
