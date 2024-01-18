import json
from typing import Any

from core.logger import get_logger
from services.social_networks.libs.abstract import SocialNetworkAbstract

logger = get_logger(__name__)


class TelegraphLib(SocialNetworkAbstract):
    POST_ENDPOINT = "https://api.telegra.ph/createPage"
    AUTH_ENDPOINT = ""

    REQUIRED_CONFIG_KEYS = {
        "access_token",
        "author_name",
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
        title = self.article.title
        message = self.article.body
        link = self.article.url
        image = self.article.img_url

        post = {
            "title": title,
            "content": json.dumps(
                [
                    {"tag": "img", "attrs": {"src": image}},
                    {"tag": "p", "children": [f"{message}\n\n{link}"]},
                ]
            ),
            "return_content": False,
        }
        return post

    async def post(self) -> str:
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        message = await self.prepare_post()

        message.update(
            {
                "access_token": config["access_token"],
                "author_name": config["author_name"],
                "author_url": self.config.project.url,
            }
        )

        logger.info(
            f"Try to send article - {self.article.title} for "
            f"{self.article.project.id}"
        )

        response = await self.client.post(
            self.POST_ENDPOINT,
            data=message,
        )

        logger.debug(
            f"Response for sent article - {self.article.title} for "
            f"{self.article.project.id}. {response.text}"
        )

        if response.json().get("ok") is False:
            raise ValueError(response.text)

        url = response.json().get("result", {}).get("url", "")

        logger.info(
            f"Success sent article - {self.article.title} for "
            f"{self.article.project.id}"
        )
        return url
