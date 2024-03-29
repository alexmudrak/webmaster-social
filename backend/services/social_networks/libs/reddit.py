from typing import Any

from core.logger import get_logger
from services.social_networks.libs.abstract import SocialNetworkAbstract

logger = get_logger(__name__)


class RedditLib(SocialNetworkAbstract):
    POST_ENDPOINT = "https://oauth.reddit.com/api/submit/"
    TOKEN_ENDPOINT = "https://www.reddit.com/api/v1/access_token"
    AUTH_ENDPOINT = ""

    REQUEST_HEADERS = {"User-Agent": "MyAPI/0.0.1"}
    REQUIRED_CONFIG_KEYS = {
        "client_id",
        "client_secret",
        "redirect_url",
        "sub_reddit",
        "refresh_token",
    }

    async def auth(self):
        # TODO: Add implementation
        raise NotImplementedError

    @staticmethod
    async def config_validation(settings: dict[Any, Any] | None) -> None:
        if not isinstance(settings, dict):
            raise ValueError("Invalid config format")

        if not RedditLib.REQUIRED_CONFIG_KEYS.issubset(settings):
            missing_keys = RedditLib.REQUIRED_CONFIG_KEYS.difference(settings)
            raise ValueError(f"Missing required keys: {missing_keys}")

    async def get_config(self) -> dict[str, Any]:
        if not isinstance(self.config.settings, dict):
            raise ValueError("Invalid config format")

        return {
            key: self.config.settings.get(key)
            for key in RedditLib.REQUIRED_CONFIG_KEYS
        }

    async def prepare_post(self) -> dict[str, Any]:
        title = self.article.title
        message = self.article.body
        link = self.article.url

        post = {
            "title": title,
            "content": f"{message}\n\n{link}",
        }
        return post

    async def get_access_token(self, config: dict) -> str:
        refresh_token = config["refresh_token"]
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        auth = (config["client_id"], config["client_secret"])

        response = await self.client.post(
            RedditLib.TOKEN_ENDPOINT,
            data=data,
            headers=RedditLib.REQUEST_HEADERS,
            auth=auth,
        )
        if (
            response.status_code != 200
            or "access_token" not in response.json()
        ):
            raise ValueError("Can't get access_token and refresh_token")

        return response.json()["access_token"]

    async def extract_url(self, json: dict) -> str:
        for item in json.get("jquery", []):
            if (
                isinstance(item[-1], list)
                and item[-1]
                and "http" in item[-1][0]
            ):
                return item[-1][0]
        return ""

    async def post(self) -> str:
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        message = await self.prepare_post()
        access_token = await self.get_access_token(config)

        headers = RedditLib.REQUEST_HEADERS
        headers.update(
            {
                "Authorization": f"bearer {access_token}",
            }
        )

        data = {
            "kind": "self",
            "sr": config["sub_reddit"],
            "title": message["title"],
            "text": message["content"],
        }

        logger.info(
            f"Try to send article - {self.article.title} for "
            f"{self.article.project.id}"
        )

        response = await self.client.post(
            RedditLib.POST_ENDPOINT,
            data=data,
            headers=headers,
        )

        logger.debug(
            f"Response for sent article - {self.article.title} for "
            f"{self.article.project.id}. {response.text}"
        )

        if not response.json().get("success"):
            raise ValueError(response.text)

        url = await self.extract_url(response.json())

        logger.info(
            f"Success sent article - {self.article.title} for "
            f"{self.article.project.id}"
        )
        return url
