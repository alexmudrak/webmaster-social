import json
from typing import Any

from core.logger import get_logger
from services.social_networks.libs.abstract import SocialNetworkAbstract
from utils.string_handler import escape_markdown

logger = get_logger(__name__)


class TelegramGroupLib(SocialNetworkAbstract):
    POST_ENDPOINT = "https://api.telegram.org/bot{access_token}/sendMessage"
    AUTH_ENDPOINT = ""

    REQUIRED_CONFIG_KEYS = {
        "group_id",
        "access_token",
    }

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
        message = escape_markdown(self.article.body[:200])
        link = self.article.url

        post = {
            "title": title,
            "description": message,
            "link": link,
        }
        return post

    async def post(self):
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

        logger.info(
            f"Success sent article - {self.article.title} for "
            f"{self.article.project.id}"
        )
