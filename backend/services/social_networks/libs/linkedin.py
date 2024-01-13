import json
from typing import Any

from services.social_networks.libs.abstract import SocialNetworkAbstract


class LinkedinLib(SocialNetworkAbstract):
    post_endpoint = "https://api.linkedin.com/v2/ugcPosts"
    auth_enpoint = ""

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
            # TODO: Add logger
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
        message = self.article.body[:200]
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

    async def post(self):
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        message = await self.prepare_post(config)

        headers = {
            "X-Restli-Protocol-Version": "2.0.0",
            "Authorization": "Bearer " + config["access_token"],
            "Content-Type": "application/json",
        }

        data = json.dumps(message).encode("utf-8")

        response = await self.client.post(
            self.post_endpoint,
            content=data,
            headers=headers,
        )

        if response.status_code != 201 or response.json().get("error"):
            raise ValueError(response.text)
