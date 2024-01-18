import json
from typing import Any

from core.logger import get_logger
from services.social_networks.libs.abstract import SocialNetworkAbstract
from utils.string_handler import escape_markdown, truncate_text

logger = get_logger(__name__)


class TelegramGroupLib(SocialNetworkAbstract):
    POST_ENDPOINT = "https://api.telegram.org/bot{access_token}/sendMessage"
    AUTH_ENDPOINT = ""

    REQUIRED_CONFIG_KEYS = {
        "group_id",
        "access_token",
    }
    MAX_MESSAGE_LENGTH = 200

    async def auth(self):
        # TODO: Add implementation
        raise NotImplementedError

    async def config_validation(self, settings: dict[Any, Any] | None) -> None:
        if not isinstance(settings, dict):
            raise ValueError("Invalid config format")

        if not self.REQUIRED_CONFIG_KEYS.issubset(settings):
            missing_keys = self.REQUIRED_CONFIG_KEYS.difference(settings)
            raise ValueError(f"Missing required keys: {missing_keys}")

    async def get_config(self) -> dict[str, Any]:
        if not isinstance(self.config.settings, dict):
            raise ValueError("Invalid config format")

        return {
            key: self.config.settings.get(key)
            for key in self.REQUIRED_CONFIG_KEYS
        }

    async def prepare_post(self) -> dict[str, Any]:
        title = escape_markdown(self.article.title)
        message = escape_markdown(
            truncate_text(self.article.body, self.MAX_MESSAGE_LENGTH)
        )
        link = self.article.url

        post = {
            "title": title,
            "description": message,
            "link": link,
        }
        return post

    def extract_url(self, json: dict) -> str:
        result = json.get("result", {})
        message_id = result.get("message_id")
        chat = result.get("chat", {})
        chat_name = chat.get("username")
        chat_id = str(chat.get("id", ""))[4:]

        base_url = "https://t.me"
        return (
            f"{base_url}/{chat_name}/{message_id}"
            if chat_name
            else f"{base_url}/c/{chat_id}/{message_id}"
        )

    async def post(self) -> str:
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        message = await self.prepare_post()

        data = {
            "chat_id": config["group_id"],
            "parse_mode": "MarkdownV2",
            "reply_markup": json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {
                                "text": "Read 👁️",
                                "url": f"{message['link']}",
                            }
                        ]
                    ]
                }
            ),
            "text": (
                f"[{message['title']}]({message['link']})\n\n"
                f"{message['description']}"
            ),
        }

        logger.info(
            f"Try to send article - {self.article.title} for "
            f"{self.article.project.id}"
        )

        response = await self.client.post(
            self.POST_ENDPOINT.format(access_token=config["access_token"]),
            data=data,
        )

        logger.debug(
            f"Response for sent article - {self.article.title} for "
            f"{self.article.project.id}. {response.text}"
        )

        if response.json().get("ok") is False:
            raise ValueError(response.text)

        url = self.extract_url(response.json())

        logger.info(
            f"Success sent article - {self.article.title} for "
            f"{self.article.project.id}"
        )
        return url
