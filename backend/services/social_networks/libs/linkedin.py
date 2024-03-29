import json
from typing import Any

from core.logger import get_logger
from services.social_networks.libs.abstract import SocialNetworkAbstract
from utils.string_handler import truncate_text

logger = get_logger(__name__)


class LinkedinLib(SocialNetworkAbstract):
    post_endpoint = "https://api.linkedin.com/v2/ugcPosts"
    auth_endpoint = ""

    max_message_length = 200

    @staticmethod
    async def config_validation(settings: Any):
        if not isinstance(settings, dict):
            raise ValueError("Invalid config format")

        required_keys = [
            "access_token",
            "user_id",
            "client_id",
            "client_secret",
        ]

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
            "access_token": self.config.settings.get("access_token"),
            "user_id": self.config.settings.get("user_id"),
            "client_id": self.config.settings.get("client_id"),
            "client_secret": self.config.settings.get("client_secret"),
        }
        return config

    async def prepare_post(self, config: dict) -> dict:
        title = self.article.title
        message = truncate_text(self.article.body, self.max_message_length)
        link = self.article.url

        post = {
            "author": "urn:li:person:" + config["user_id"],
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": message},
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {"text": message},
                            "originalUrl": link,
                            "title": {"text": title},
                        }
                    ],
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }
        return post

    async def extract_url(self, json: dict) -> str:
        post_id = json.get("id")
        url = f"https://www.linkedin.com/feed/update/{post_id}/"
        return url

    async def post(self) -> str:
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        message = await self.prepare_post(config)

        headers = {
            "X-Restli-Protocol-Version": "2.0.0",
            "Authorization": "Bearer " + config["access_token"],
            "Content-Type": "application/json",
        }

        data = json.dumps(message).encode("utf-8")

        logger.info(
            f"Try to send article - {self.article.title} for "
            f"{self.article.project.id}"
        )

        response = await self.client.post(
            self.post_endpoint,
            content=data,
            headers=headers,
        )

        logger.debug(
            f"Response for sent article - {self.article.title} for "
            f"{self.article.project.id}. {response.text}"
        )

        if response.status_code != 201 or response.json().get("error"):
            raise ValueError(response.text)

        url = await self.extract_url(response.json())

        logger.info(
            f"Success sent article - {self.article.title} for "
            f"{self.article.project.id}"
        )
        return url
