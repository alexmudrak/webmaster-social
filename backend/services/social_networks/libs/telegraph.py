import json
from typing import Any

from services.social_networks.libs.abstract import SocialNetworkAbstract


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
            # TODO: Add logger
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

    async def post(self):
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

        response = await self.client.post(
            self.POST_ENDPOINT,
            data=message,
        )

        if response.json().get("ok") is False:
            raise ValueError(response.text)
