from typing import Any

from services.social_networks.libs.abstract import SocialNetworkAbstract


class FacebookLib(SocialNetworkAbstract):
    api_version = "v18.0"
    # TODO: Change format style to `.format`
    endpoint = f"https://graph.facebook.com/{api_version}/%s/feed"
    auth_endpoint = ""

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
            # TODO: Add logger
            raise ValueError("Invalid config format")

        config = {
            "page_id": self.config.settings.get("group_id"),
            "access_token": self.config.settings.get("access_token"),
        }
        return config

    async def prepare_post(self) -> dict:
        message = self.article.body[:200]
        link = self.article.url

        post = {
            "message": f"{self.article.title}\n\n{message}",
            "link": link,
        }
        return post

    async def post(self):
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        message = await self.prepare_post()

        data = {**message, **config}

        response = await self.client.post(
            self.endpoint % (config.get("page_id")),
            data=data,
            timeout=30,
        )

        if response.status_code != 200 or response.json().get("error"):
            raise ValueError(response.text)
