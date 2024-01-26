from io import BytesIO
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from core.database import AsyncSession
from httpx import AsyncClient
from models.setting import Setting
from PIL import Image
from services.social_networks.libs.instagram import InstagramLib


@pytest.fixture
def mock_session():
    return MagicMock(spec=AsyncSession)


@pytest.fixture
def mock_client():
    mock = AsyncMock(spec=AsyncClient)
    mock.post = AsyncMock()
    mock.get = AsyncMock()
    return mock


@pytest.fixture
def mock_config():
    return MagicMock(
        spec=Setting,
        settings={
            "username": "testuser",
            "cookies": "testcookies",
        },
    )


@pytest.fixture
def instagram_lib(
    mock_session,
    mock_client,
    mock_config,
    mock_article,
):
    return InstagramLib(
        session=mock_session,
        client=mock_client,
        config=mock_config,
        article=mock_article,
    )


@pytest.fixture
def config_settings():
    return {"username": "testuser", "cookies": "testcookies"}


@pytest.mark.asyncio
async def test_config_validation(instagram_lib, config_settings):
    with pytest.raises(ValueError):
        await instagram_lib.config_validation(None)

    with pytest.raises(ValueError):
        await instagram_lib.config_validation({"username": "testuser"})

    assert await instagram_lib.config_validation(config_settings) is None


@pytest.mark.asyncio
async def test_get_config(instagram_lib):
    config = await instagram_lib.get_config()
    assert config["username"] == "testuser"
    assert config["cookies"] == "testcookies"


@pytest.mark.asyncio
async def test_get_cookeis(instagram_lib, config_settings):
    cookies = await instagram_lib.get_cookies({"cookies": config_settings})
    assert cookies["cookies"] == "testcookies"


@pytest.mark.asyncio
async def test_get_config_invalid_format(instagram_lib):
    instagram_lib.config.settings = None

    with pytest.raises(ValueError) as exc_info:
        await instagram_lib.get_config()

    assert "Invalid config format" in str(exc_info.value)


@pytest.mark.asyncio
async def test_prepare_post(instagram_lib):
    truncate_text = (
        "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. "
        "Aeneancommodo ligula eget dolor. Aenean massa. Cum sociis "
        "natoquepenatibus et magnis dis parturient montes, nascetur "
        "ridiculus. Donec quam..."
    )
    expected_message = (
        f"{instagram_lib.article.title}\n\n"
        f"{truncate_text}\n\n"
        f"{instagram_lib.article.url}"
    )
    post = await instagram_lib.prepare_post()
    assert post["message"] == expected_message


@pytest.mark.asyncio
async def test_prepare_image_1_1(instagram_lib):
    red_image = Image.new("RGB", (1, 1), color="red")
    image_bytes = BytesIO()
    red_image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    instagram_lib.send_request = AsyncMock(
        return_value=type(
            "Response", (object,), {"content": image_bytes.read()}
        )
    )

    result_image = await instagram_lib.prepare_image()
    instagram_lib.send_request.assert_awaited_once_with(
        method="GET", url=instagram_lib.article.img_url
    )

    assert result_image.size == (1, 1)


@pytest.mark.asyncio
async def test_prepare_image_1_2(instagram_lib):
    red_image = Image.new("RGB", (1, 2), color="red")
    image_bytes = BytesIO()
    red_image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    instagram_lib.send_request = AsyncMock(
        return_value=type(
            "Response", (object,), {"content": image_bytes.read()}
        )
    )

    result_image = await instagram_lib.prepare_image()
    instagram_lib.send_request.assert_awaited_once_with(
        method="GET", url=instagram_lib.article.img_url
    )

    assert result_image.size == (1, 0)


@pytest.mark.asyncio
async def test_prepare_image_2_1(instagram_lib):
    red_image = Image.new("RGB", (2, 1), color="red")
    image_bytes = BytesIO()
    red_image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    instagram_lib.send_request = AsyncMock(
        return_value=type(
            "Response", (object,), {"content": image_bytes.read()}
        )
    )

    result_image = await instagram_lib.prepare_image()
    instagram_lib.send_request.assert_awaited_once_with(
        method="GET", url=instagram_lib.article.img_url
    )

    assert result_image.size == (0, 1)


@pytest.mark.asyncio
async def test_prepare_login_data(instagram_lib, config_settings):
    login_data = await instagram_lib.prepare_login_data(config_settings)
    assert login_data["username"] == config_settings["username"]


@pytest.mark.asyncio
async def test_generate_signature(instagram_lib):
    data = '{"test": "data"}'
    signature = await instagram_lib.generate_signature(data)
    assert signature.startswith("signed_body=")


@pytest.mark.asyncio
async def test_send_request(instagram_lib):
    instagram_lib.client.post.return_value = AsyncMock(
        status_code=200, json=lambda: {"test": "data"}
    )
    response = await instagram_lib.send_request(
        method="POST", url="http://test.com", data={"test": "data"}
    )
    assert response.status_code == 200
    assert response.json() == {"test": "data"}


@pytest.mark.asyncio
async def test_upload_image(instagram_lib):
    mock_image = MagicMock(spec=Image.Image)
    mock_response = MagicMock()

    with patch.object(
        instagram_lib,
        "send_request",
        new=AsyncMock(return_value=mock_response),
    ) as mock_send_request:
        response = await instagram_lib.upload_image(
            image=mock_image, cookies={"test": "cookie"}
        )
        mock_send_request.assert_awaited_once()
        _, kwargs = mock_send_request.call_args
        assert kwargs["method"] == "POST"
        assert kwargs["url"].startswith(instagram_lib.upload_photo_endpoint)
        assert "X-Instagram-Rupload-Params" in kwargs["headers"]
        assert "X_FB_PHOTO_WATERFALL_ID" in kwargs["headers"]
        assert kwargs["cookies"] == {"test": "cookie"}
        assert response == mock_response


@pytest.mark.asyncio
async def test_publish_post(instagram_lib):
    mock_image = MagicMock(spec=Image.Image)
    mock_image.size = (800, 600)
    mock_response = MagicMock()
    image_id = "test_image_id"
    post = {"message": "Test caption"}
    login_data = {"device_settings": "test_device", "uuid": "test_uuid"}
    cookies = {"ds_user_id": "test_user_id", "csrftoken": "test_token"}

    with patch.object(
        instagram_lib,
        "send_request",
        new=AsyncMock(return_value=mock_response),
    ) as mock_send_request:
        response = await instagram_lib.publish_post(
            image=mock_image,
            image_id=image_id,
            post=post,
            login_data=login_data,
            cookies=cookies,
        )
        mock_send_request.assert_awaited_once()
        _, kwargs = mock_send_request.call_args
        assert kwargs["method"] == "POST"
        assert kwargs["url"] == instagram_lib.post_endpoint
        assert kwargs["data"]["upload_id"] == image_id
        assert kwargs["data"]["caption"] == post.get("message")
        assert kwargs["data"]["device"] == login_data.get("device_settings")
        assert kwargs["data"]["_uuid"] == login_data.get("uuid")
        assert kwargs["data"]["_uid"] == cookies.get("ds_user_id")
        assert kwargs["data"]["_csrftoken"] == cookies.get("csrftoken")
        assert kwargs["cookies"] == cookies

        assert response == mock_response


@pytest.mark.asyncio
async def test_extract_url(instagram_lib):
    json_data = {"media": {"code": "test_post_id"}}
    expected_url = "https://www.instagram.com/p/test_post_id"

    result_url = await instagram_lib.extract_url(json=json_data)

    assert result_url == expected_url


@pytest.mark.asyncio
async def test_post_success(instagram_lib):
    with patch.object(
        InstagramLib, "config_validation", new=AsyncMock()
    ) as mock_config_validation, patch.object(
        InstagramLib, "get_config", new=AsyncMock(return_value="config")
    ) as mock_get_config, patch.object(
        InstagramLib, "prepare_post", new=AsyncMock(return_value="post")
    ) as mock_prepare_post, patch.object(
        InstagramLib, "prepare_image", new=AsyncMock(return_value="image")
    ) as mock_prepare_image, patch.object(
        InstagramLib,
        "prepare_login_data",
        new=AsyncMock(return_value="login_data"),
    ) as mock_prepare_login_data, patch.object(
        InstagramLib, "get_cookies", new=AsyncMock(return_value="cookies")
    ) as mock_get_cookies, patch.object(
        InstagramLib, "upload_image", new=AsyncMock()
    ) as mock_upload_image, patch.object(
        InstagramLib, "publish_post", new=AsyncMock()
    ) as mock_publish_post, patch.object(
        InstagramLib, "extract_url", new=AsyncMock(return_value="url")
    ) as mock_extract_url, patch(
        "asyncio.sleep", new=AsyncMock()
    ) as mock_sleep:
        mock_upload_image.return_value.status_code = 200
        mock_upload_image.return_value.json = MagicMock(
            return_value={"upload_id": "123"}
        )
        mock_publish_post.return_value.status_code = 200
        mock_publish_post.return_value.json = MagicMock(return_value={})

        result = await instagram_lib.post()

        mock_config_validation.assert_awaited_once()
        mock_get_config.assert_awaited_once()
        mock_prepare_post.assert_awaited_once()
        mock_prepare_image.assert_awaited_once()
        mock_prepare_login_data.assert_awaited_once()
        mock_get_cookies.assert_awaited_once()
        mock_upload_image.assert_awaited_once()
        mock_publish_post.assert_awaited_once()
        mock_extract_url.assert_awaited_once()
        mock_sleep.assert_awaited_once()

        assert result == "url"
