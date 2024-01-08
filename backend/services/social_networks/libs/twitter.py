from typing import Any

import httpx
from authlib.integrations.requests_client import OAuth2Session
from services.social_networks.libs.abstract import SocialNetworkAbstract


class TwitterLib(SocialNetworkAbstract):
    auth_endpoint = "https://twitter.com/i/oauth2/authorize"
    token_endpoint = "https://api.twitter.com/2/oauth2/token"
    tweet_endpoint = "https://api.twitter.com/2/tweets"
    scopes = ["tweet.write", "users.read", "tweet.read", "offline.access"]

    @staticmethod
    async def config_validation(settings: Any):
        if not isinstance(settings, dict):
            raise ValueError("Invalid config format")

        required_keys = [
            "client_id",
            "client_secret",
            "refresh_token",
            "redirect_uri",
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
            "client_id": self.config.settings.get("client_id"),
            "client_secret": self.config.settings.get("client_secret"),
            "refresh_token": self.config.settings.get("refresh_token"),
            "redirect_uri": self.config.settings.get("redirect_uri"),
        }
        return config

    async def get_client(self, config: dict) -> OAuth2Session:
        # TODO: Add async session
        return OAuth2Session(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            redirect_uri=config["redirect_uri"],
            scope=self.scopes,
            code_challenge_method="S256",
        )

    async def get_updated_token(
        self, client: OAuth2Session, config: dict
    ) -> dict:
        # TODO: Change to async session
        new_token = client.refresh_token(
            url=self.token_endpoint,
            refresh_token=config["refresh_token"],
        )
        config["refresh_token"] = new_token["refresh_token"]
        self.config.settings = config

        self.session.add(self.config)
        await self.session.commit()

        return new_token

    async def prepare_post(self) -> dict:
        link = self.article.url

        post = {
            "message": f"{self.article.title}\n\n{link}",
        }
        return post

    async def post(self):
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        client = await self.get_client(config)
        token = await self.get_updated_token(client, config)
        message = await self.prepare_post()

        response = httpx.post(
            self.tweet_endpoint,
            json={"text": message["message"]},
            headers={
                "Authorization": f"Bearer {token['access_token']}",
                "Content-Type": "application/json",
            },
        )

        if response.status_code != 201 or response.json().get("error"):
            raise ValueError(response.text)
