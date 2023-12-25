from services.social_networks.libs.abstract import SocialNetworkAbstract


class VkontakteLib(SocialNetworkAbstract):
    endpoint = "https://api.vk.com/method/wall.post"
    auth_enpoint = (
        "https://oauth.vk.com/authorize?client_id=%s&display=page"
        "&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,wall"
        "&response_type=token&v=5.199&state=123456"
    )

    async def auth(self):
        # TODO: Add implementation
        raise NotImplementedError

    async def get_config(self) -> dict:
        if not isinstance(self.config.settings, dict):
            raise ValueError("Invalid config format")

        required_keys = ["app_id", "owner_id", "access_token"]

        for key in required_keys:
            if key not in self.config.settings:
                raise ValueError(f"Missing required key: {key}")

        config = {
            "app_id": self.config.settings.get("app_id"),
            "owner_id": self.config.settings.get("owner_id"),
            "access_token": self.config.settings.get("access_token"),
            "from_group": 1,
            "v": 5.199,
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
        message = await self.prepare_post()
        config = await self.get_config()

        data = {**message, **config}

        response = await self.client.post(self.endpoint, data=data)

        if response.status_code != 200 or response.json().get("error"):
            raise ValueError(response.text)
