from typing import Any

from services.social_networks.libs.abstract import SocialNetworkAbstract


class RedditLib(SocialNetworkAbstract):
    POST_ENDPOINT = "https://oauth.reddit.com/api/submit/"
    AUTH_ENDPOINT = ""

    REQUIRED_CONFIG_KEYS = {
        "client_id",
        "client_secret",
        "username",
        "password",
        "sub_reddit",
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
            # TODO: Add logger
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

    async def post(self):
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        message = await self.prepare_post()

        headers = {}
        data = {
            "api_type": "json",
            "kind": "self",
            "nsfw": False,
            "resubmit": True,
            "richtext_json": ...,
            "sendreplies": True,
            "spoiler": False,
            "sr": config["sub_reddit"],
            "title": message["title"],
            "validate_on_submit": True,
        }

        response = await self.client.post(
            RedditLib.POST_ENDPOINT,
            data=data,
            headers=headers,
        )

        if response.status_code != 201 or response.json().get("error"):
            raise ValueError(response.text)
