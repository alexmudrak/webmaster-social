from typing import Any

from core.logger import get_logger
from services.social_networks.libs.abstract import SocialNetworkAbstract
from utils.string_handler import truncate_text

logger = get_logger(__name__)


class FacebookLib(SocialNetworkAbstract):
    api_version = "v18.0"
    # TODO: Change format style to `.format`
    endpoint = f"https://graph.facebook.com/{api_version}/%s/feed?fields=permalink_url"
    auth_endpoint = ""

    max_message_length = 200

    @staticmethod
    async def config_validation(settings: Any):
        if not isinstance(settings, dict):
            raise ValueError("Invalid config format")

        required_keys = ["group_id", "access_token"]

        for key in required_keys:
            if key not in settings:
                raise ValueError(f"Missing required key: {key}")

    async def auth(self):
        # TODO: Add implementation
        raise NotImplementedError

    async def get_config(self) -> dict:
        if not isinstance(self.config.settings, dict):
            raise ValueError("Invalid config format")

        config = {
            "page_id": self.config.settings.get("group_id"),
            "access_token": self.config.settings.get("access_token"),
        }
        return config

    async def prepare_post(self) -> dict:
        message = truncate_text(self.article.body, self.max_message_length)
        link = self.article.url

        post = {
            "message": f"{self.article.title}\n\n{message}",
            "link": link,
        }
        return post

    async def post(self) -> str:
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        message = await self.prepare_post()

        data = {**message, **config}

        logger.info(
            f"Try to send article - {self.article.title} for "
            f"{self.article.project.id}"
        )

        response = await self.client.post(
            self.endpoint % (config.get("page_id")),
            data=data,
            timeout=30,
        )

        logger.debug(
            f"Response for sent article - {self.article.title} for "
            f"{self.article.project.id}. {response.text}"
        )

        if response.status_code != 200 or response.json().get("error"):
            raise ValueError(response.text)

        url = response.json().get("permalink_url")

        logger.info(
            f"Success sent article - {self.article.title} for "
            f"{self.article.project.id}"
        )
        return url
