from typing import Any

from core.logger import get_logger
from services.social_networks.libs.abstract import SocialNetworkAbstract

logger = get_logger(__name__)


class MediumLib(SocialNetworkAbstract):
    POST_ENDPOINT = "https://api.medium.com/v1/users/{user_id}/posts"
    AUTH_ENDPOINT = ""

    REQUIRED_CONFIG_KEYS = {
        "user_id",
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
        title = self.article.title
        message = self.article.body
        link = self.article.url

        post = {
            "title": title,
            "content": f"{message}\n\n{link}",
            "tags": [],  # TODO: need to implement
            "link": link,
        }
        return post

    async def post(self):
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        message = await self.prepare_post()

        headers = {
            "Authorization": f"Bearer {config['access_token']}",
        }
        data = {
            "title": message["title"],
            "contentFormat": "markdown",
            "content": message["content"],
            "canonicalUrl": message["link"],
            "tags": message["tags"],
            "publishStatus": "public",
        }

        logger.info(
            f"Try to send article - {self.article.title} for "
            f"{self.article.project.id}"
        )
        response = await self.client.post(
            self.POST_ENDPOINT.format(user_id=config["user_id"]),
            data=data,
            headers=headers,
        )

        logger.debug(
            f"Response for sent article - {self.article.title} for "
            f"{self.article.project.id}. {response.text}"
        )

        if response.status_code != 201 or response.json().get("error"):
            raise ValueError(response.text)

        logger.info(
            f"Success sent article - {self.article.title} for "
            f"{self.article.project.id}"
        )
