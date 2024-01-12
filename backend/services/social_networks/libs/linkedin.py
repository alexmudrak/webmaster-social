import json
from typing import Any

from services.social_networks.libs.abstract import SocialNetworkAbstract


class LinkedinLib(SocialNetworkAbstract):
    post_endpoint = "https://api.linkedin.com/v2/shares"
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
        image_link = self.article.image_link

        post = {
            "content": {
                "contentEntities": [
                    {
                        "entityLocation": link,
                        "thumbnails": [{"resolvedUrl": image_link}],
                    }
                ],
                "title": title[:100],
            },
            "distribution": {"linkedInDistributionTarget": {}},
            "owner": "urn:li:person:" + config["user_id"],
            "subject": "\n\n",
            "text": {"text": message},
        }
        return post

    async def post(self):
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        message = await self.prepare_post(config)

        headers = {"Authorization": "Bearer " + config["access_token"]}

        data = json.dumps(message).encode("utf-8")

        response = await self.client.post(
            self.post_endpoint,
            data=data,
            headers=headers,
        )

        if response.status_code != 200 or response.json().get("error"):
            raise ValueError(response.text)
