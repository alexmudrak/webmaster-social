import json
from typing import Any
from urllib import parse

from core.logger import get_logger
from services.social_networks.libs.abstract import SocialNetworkAbstract
from utils.string_handler import truncate_text

logger = get_logger(__name__)


class PinterestLib(SocialNetworkAbstract):
    # TODO: Refactor CONST case
    post_endpoint = "https://www.pinterest.com/resource/PinResource/create/"
    pin_url = "https://ru.pinterest.com/pin/{pin_id}/"
    auth_endpoint = ""

    headers = {
        "Referer": "https://www.pinterest.com/",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        ),
    }

    max_message_length = 200

    @staticmethod
    async def config_validation(settings: Any):
        if not isinstance(settings, dict):
            raise ValueError("Invalid config format")

        required_keys = ["cookies", "board_id"]

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
            "board_id": self.config.settings.get("board_id"),
            "cookies": self.config.settings.get("cookies"),
        }
        return config

    async def prepare_post(self) -> dict:
        message = truncate_text(self.article.body, self.max_message_length)
        link = self.article.url

        post = {
            "image": self.article.img_url,
            "title": self.article.title,
            "message": message,
            "link": link,
        }
        return post

    async def data_encode(self, query: str | dict) -> str:
        if isinstance(query, str):
            query = parse.quote_plus(query)
        else:
            query = parse.urlencode(query)

        query = query.replace("+", "%20")
        return query

    async def post(self) -> str:
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        post = await self.prepare_post()

        headers = self.headers
        headers.update(
            {"X-CSRFToken": config["cookies"].get("csrftoken")},
        )

        data_options = {
            "board_id": config["board_id"],
            "image_url": post["image"],
            "description": post["message"],
            "link": post["link"],
            "scrape_metric": {"source": "www_url_scrape"},
            "method": "scraped",
            "title": post["title"],
            "section": None,
        }
        encoded_source_url = await self.data_encode(post["image"])
        data = await self.data_encode(
            {
                "source_url": f"/pin/find/?url={encoded_source_url}",
                "data": json.dumps({"options": data_options, "context": None}),
            }
        )

        logger.info(
            f"Try to send article - {self.article.title} for "
            f"{self.article.project.id}"
        )

        response = await self.client.post(
            self.post_endpoint,
            content=data,
            headers=headers,
            cookies=config["cookies"],
        )

        logger.debug(
            f"Response for sent article - {self.article.title} for "
            f"{self.article.project.id}. {response.text}"
        )

        if response.status_code != 200 or response.json().get("error"):
            raise ValueError(response.text)

        pin_id = response.json().get("resource_response")["data"]["id"]
        url = self.pin_url.format(pin_id=pin_id)

        logger.info(
            f"Success sent article - {self.article.title} for "
            f"{self.article.project.id}"
        )
        return url
