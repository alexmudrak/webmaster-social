from typing import Any

from services.social_networks.libs.abstract import SocialNetworkAbstract


class VkontakteLib(SocialNetworkAbstract):
    api_version = 5.199
    endpoint = "https://api.vk.com/method/wall.post"
    auth_enpoint = (
        "https://oauth.vk.com/authorize?client_id=%s&display=page"
        "&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,wall"
        f"&response_type=token&v={api_version}&state=123456"
    )

    @staticmethod
    async def config_validation(settings: Any):
        if not isinstance(settings, dict):
            raise ValueError("Invalid config format")

        required_keys = ["app_id", "group_id", "access_token"]

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
            "owner_id": self.config.settings.get("group_id"),
            "access_token": self.config.settings.get("access_token"),
            "from_group": 1,
            "v": self.api_version,
        }
        return config

    async def prepare_post(self) -> dict:
        message = self.article.body[:200]
        link = self.article.url

        post = {
            "message": f"{self.article.title}\n\n{message}",
            "attachments": link,
        }
        return post

    async def post(self):
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        message = await self.prepare_post()

        data = {**message, **config}

        response = await self.client.post(self.endpoint, data=data)

        if response.status_code != 200 or response.json().get("error"):
            raise ValueError(response.text)
