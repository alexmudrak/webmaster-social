import asyncio
import hashlib
import hmac
import json
import random
import time
import uuid
from io import BytesIO
from math import ceil
from typing import Any
from urllib import parse

from core.logger import get_logger
from httpx import Response
from PIL import Image
from services.social_networks.libs.abstract import SocialNetworkAbstract

logger = get_logger(__name__)


class InstagramLib(SocialNetworkAbstract):
    post_endpoint = "https://i.instagram.com/api/v1/media/configure/?"
    upload_photo_endpoint = "https://i.instagram.com/rupload_igphoto/"
    request_headers = {
        "X-IG-App-Locale": "en_US",
        "X-IG-Device-Locale": "en_US",
        "X-Pigeon-Session-Id": "21aa671b-a5f3-4093-8ec2-0c98420675e1",
        "X-Pigeon-Rawclienttime": str(round(time.time() * 1000)),
        "X-IG-Connection-Speed": "-1kbps",
        "X-IG-Bandwidth-Speed-KBPS": str(random.randint(7000, 10000)),
        "X-IG-Bandwidth-TotalBytes-B": str(random.randint(500000, 900000)),
        "X-IG-Bandwidth-TotalTime-MS": str(random.randint(50, 150)),
        "X-IG-Prefetch-Request": "foreground",
        "X-Bloks-Version-Id": (
            "0a3ae4c88248863609c67e278f34af44673cff300bc76add965a9fb036bd3ca3"
        ),
        "X-IG-WWW-Claim": "0",
        "X-MID": "XkAyKQABAAHizpYQvHzNeBo4E9nm",
        "X-Bloks-Is-Layout-RTL": "false",
        "X-Bloks-Enable-RenderCore": "false",
        "X-IG-Connection-Type": "WIFI",
        "X-IG-Capabilities": "3brTvwE=",
        "X-IG-App-ID": "567067343352427",
        "X-IG-App-Startup-Country": "US",
        "Accept-Language": "en-US",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate",
        "Host": "i.instagram.com",
        "X-FB-HTTP-Engine": "Liger",
        "Connection": "close",
    }
    ig_sig_key = (
        "a86109795736d73c9a94172cd9b736917d7d94ca61c9101164894b3f0d43bef4"
    )
    sig_key_version = "4"

    @staticmethod
    async def config_validation(settings: Any):
        if not isinstance(settings, dict):
            raise ValueError("Invalid config format")

        required_keys = ["username", "password", "cookies"]

        for key in required_keys:
            if key not in settings:
                raise ValueError(f"Missing required key: {key}")

    async def generate_signature(self, data) -> str:
        # TODO: Add documentation
        # TODO: Need to refactor
        body = (
            hmac.new(
                self.ig_sig_key.encode("utf-8"),
                data.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            + "."
            + parse.quote(data)
        )
        signature = "signed_body={body}&ig_sig_key_version={sig_key}"

        return signature.format(sig_key=self.sig_key_version, body=body)

    async def send_request(
        self,
        method: str,
        url: str,
        headers: dict | None = None,
        data: str | dict | bytes | None = None,
        login_data: dict | None = None,
        cookies: dict | None = None,
        signature: bool = False,
    ) -> Response:
        # TODO: Add documentation
        # TODO: Need to refactor
        headers = headers or self.request_headers

        if login_data:
            headers["User-Agent"] = login_data["user_agent"]

        if signature:
            data = await self.generate_signature(json.dumps(data))

        match method:
            case "POST":
                response = await self.client.post(
                    url,
                    data=data,
                    headers=headers,
                    cookies=cookies,
                )
            case "GET":
                response = await self.client.get(url)
            case _:
                raise NotImplementedError(
                    f"Request method `{method}` - not implemented."
                )
        return response

    async def auth(self, login_data: dict) -> dict:
        # TODO: Add implementation
        raise NotImplementedError

    async def get_config(self) -> dict:
        if not isinstance(self.config.settings, dict):
            raise ValueError("Invalid config format")

        config = {
            "username": self.config.settings.get("username"),
            "password": self.config.settings.get("password"),
            "cookies": self.config.settings.get("cookies"),
        }
        return config

    async def prepare_post(self) -> dict:
        title = self.article.title
        message = self.article.body[:200]
        link = self.article.url

        post = {
            "message": f"{title}\n\n{message}\n\n{link}",
        }
        return post

    async def prepare_login_data(self, config: dict) -> dict:
        # TODO: Add documentation
        # TODO: Update device info
        device_settings = {
            "app_version": "117.0.0.28.123",
            "android_version": "28",
            "android_release": "9.0",
            "dpi": "420dpi",
            "resolution": "1080x1920",
            "manufacturer": "OnePlus",
            "device": "ONEPLUS A3003",
            "model": "OnePlus3",
            "cpu": "qcom",
            "version_code": "180322800",
        }

        user_agent_template = (
            "Instagram {app_version} "
            "Android ({android_version}/{android_release}; "
            "{dpi}; {resolution}; {manufacturer}; "
            "{device}; {model}; {cpu}; en_US; {version_code})"
        )

        # TODO: Add to dataclass
        login_data = {
            "cookies": config.get("cookies"),
            "username": config.get("username"),
            "password": config.get("password"),
            "device_settings": device_settings,
            "user_agent": user_agent_template.format(**device_settings),
            "phone_id": str(uuid.uuid4()),
            "uuid": str(uuid.uuid4()),
            "client_session_id": str(uuid.uuid4()),
            "advertising_id": str(uuid.uuid4()),
            "device_id": "android-%s"
            % hashlib.sha256(str(time.time()).encode()).hexdigest()[:16],
        }
        return login_data

    async def get_cookies(self, login_data: dict) -> dict:
        cookies = login_data["cookies"]

        if not cookies:
            cookies = await self.auth(login_data)

        return cookies

    async def resize_image(self, image: Image.Image) -> Image.Image:
        # TODO: Add documentation
        # TODO: Need to refactor
        h_lim = {"w": 90.0, "h": 47.0}
        v_lim = {"w": 4.0, "h": 5.0}

        img = image
        width, height = img.size
        img = img.convert("RGBA")
        ratio = width * 1.0 / height * 1.0

        if width > height:
            # Horizontal image
            if ratio > (h_lim["w"] / h_lim["h"]):
                cut = int(ceil((width - height * h_lim["w"] / h_lim["h"]) / 2))
                left = cut
                right = width - cut
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))
                width, height = img.size
            if width > 1080:
                nw = 1080
                nh = int(ceil(1080.0 * height / width))
                img = img.resize((nw, nh), Image.LANCZOS)
        elif width < height:
            # Vertical image
            if ratio < (v_lim["w"] / v_lim["h"]):
                cut = int(ceil((height - width * v_lim["h"] / v_lim["w"]) / 2))
                left = 0
                right = width
                top = cut
                bottom = height - cut
                img = img.crop((left, top, right, bottom))
                width, height = img.size
            if height > 1080:
                nw = int(ceil(1080.0 * width / height))
                nh = 1080
                img = img.resize((nw, nh), Image.LANCZOS)
        else:
            # Square image
            if width > 1080:
                img = img.resize((1080, 1080), Image.LANCZOS)
        # Convert tot RGB
        # TODO: Are we need it?
        img2 = Image.new("RGB", img.size, (255, 255, 255))
        img2.paste(img, (0, 0), img)
        img = img2
        return img

    async def prepare_image(self) -> Image.Image:
        # TODO: Add documentation
        img_url = self.article.img_url
        response = await self.send_request(method="GET", url=img_url)
        image_bytes = BytesIO(response.content)
        image = Image.open(image_bytes)
        image = await self.resize_image(image)
        return image

    async def upload_image(
        self, image: Image.Image, cookies: dict
    ) -> Response:
        # TODO: Add documentation
        tmp_bytes = BytesIO()
        image.save(tmp_bytes, "JPEG")

        image_id = str(int(time.time() * 1000))
        image_type = "image/jpeg"
        image_name = f"{image_id}_0_{random.randint(1000000000, 9999999999)}"
        image_len = len(tmp_bytes.getvalue())
        waterfall_id = str(uuid.uuid4())

        image_params = {
            "retry_context": json.dumps(
                {
                    "num_step_auto_retry": 0,
                    "num_reupload": 0,
                    "num_step_manual_retry": 0,
                }
            ),
            "media_type": "1",
            "xsharing_user_ids": "[]",
            "upload_id": image_id,
            "image_compression": json.dumps(
                {
                    "lib_name": "moz",
                    "lib_version": "3.1.m",
                    "quality": "80",
                }
            ),
        }
        image_request_headers = {
            "Accept-Encoding": "gzip",
            "X-Instagram-Rupload-Params": json.dumps(image_params),
            "X_FB_PHOTO_WATERFALL_ID": waterfall_id,
            "X-Entity-Type": image_type,
            "Offset": "0",
            "X-Entity-Name": image_name,
            "X-Entity-Length": str(image_len),
            "Content-Type": "application/octet-stream",
            "Content-Length": str(image_len),
        }
        response = await self.send_request(
            method="POST",
            url=f"{self.upload_photo_endpoint}{image_name}",
            headers=image_request_headers,
            data=tmp_bytes.getvalue(),
            cookies=cookies,
        )
        return response

    async def publish_post(
        self,
        image: Image.Image,
        image_id: str,
        post: dict,
        login_data: dict,
        cookies: dict,
    ) -> Response:
        # TODO: Add documentation
        # TODO: Need to refactor
        width, height = image.size
        data = {
            "media_folder": "Instagram",
            "source_type": 4,
            "caption": post.get("message"),
            "upload_id": image_id,
            "device": login_data.get("device_settings"),
            "edits": {
                "crop_original_size": [width * 1.0, height * 1.0],
                "crop_center": [0.0, 0.0],
                "crop_zoom": 1.0,
            },
            "extra": {"source_width": width, "source_height": height},
            "_uuid": login_data.get("uuid"),
            "_uid": cookies.get("ds_user_id"),
            "_csrftoken": cookies.get("csrftoken"),
        }
        response = await self.send_request(
            method="POST",
            url=self.post_endpoint,
            data=data,
            login_data=login_data,
            cookies=cookies,
            signature=True,
        )
        return response

    async def post(self):
        await self.config_validation(self.config.settings)

        config = await self.get_config()
        post = await self.prepare_post()
        image = await self.prepare_image()
        login_data = await self.prepare_login_data(config)
        cookies = await self.get_cookies(login_data)

        upload_photo_response = await self.upload_image(image, cookies)
        if upload_photo_response.status_code != 200:
            raise ValueError(
                f"Can not upload image. {upload_photo_response.content}"
            )
        image_id = upload_photo_response.json().get("upload_id")

        await asyncio.sleep(3)

        logger.info(
            f"Try to send article - {self.article.title} for "
            f"{self.article.project.id}"
        )

        response = await self.publish_post(
            image=image,
            image_id=image_id,
            post=post,
            login_data=login_data,
            cookies=cookies,
        )

        logger.debug(
            f"Response for sent article - {self.article.title} for "
            f"{self.article.project.id}. {response.text}"
        )

        if response.status_code != 200 or response.json().get("error"):
            raise ValueError(response.text)

        logger.info(
            f"Success sent article - {self.article.title} for "
            f"{self.article.project.id}"
        )
