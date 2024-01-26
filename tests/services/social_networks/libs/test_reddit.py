from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from core.database import AsyncSession
from httpx import AsyncClient
from models.setting import Setting
from services.social_networks.libs.reddit import RedditLib


@pytest.fixture
def mock_session():
    return MagicMock(spec=AsyncSession)


@pytest.fixture
def config_settings():
    return {
        "client_id": "testclient",
        "client_secret": "testclientsecret",
        "redirect_url": "testurlredirect",
        "sub_reddit": "testsubreddit",
        "refresh_token": "testtoken",
    }


@pytest.fixture
def mock_client():
    mock = AsyncMock(spec=AsyncClient)
    mock.post = AsyncMock()
    mock.get = AsyncMock()
    return mock


@pytest.fixture
def mock_config(config_settings):
    return MagicMock(
        spec=Setting,
        settings=config_settings,
    )


@pytest.fixture
def social_lib(
    mock_session,
    mock_client,
    mock_config,
    mock_article,
):
    return RedditLib(
        session=mock_session,
        client=mock_client,
        config=mock_config,
        article=mock_article,
    )


@pytest.mark.asyncio
async def test_config_validation(social_lib, config_settings):
    with pytest.raises(ValueError):
        await social_lib.config_validation(None)

    with pytest.raises(ValueError):
        await social_lib.config_validation(
            {"wrong_config": "wrong_config_value"}
        )

    assert await social_lib.config_validation(config_settings) is None


@pytest.mark.asyncio
async def test_get_config(social_lib):
    config = await social_lib.get_config()
    assert config["client_id"] == "testclient"
    assert config["client_secret"] == "testclientsecret"
    assert config["redirect_url"] == "testurlredirect"
    assert config["sub_reddit"] == "testsubreddit"
    assert config["refresh_token"] == "testtoken"


@pytest.mark.asyncio
async def test_get_config_invalid_format(social_lib):
    social_lib.config.settings = None

    with pytest.raises(ValueError) as exc_info:
        await social_lib.get_config()

    assert "Invalid config format" in str(exc_info.value)


@pytest.mark.asyncio
async def test_prepare_post(social_lib):
    expected_message = (
        f"{social_lib.article.body}\n\n" f"{social_lib.article.url}"
    )
    post = await social_lib.prepare_post()
    assert post["content"] == expected_message


@pytest.mark.asyncio
async def test_get_access_token(social_lib, config_settings):
    with patch.object(social_lib.client, "post", new=AsyncMock()) as mock_post:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock(
            return_value={"access_token": "mock_new_token"}
        )
        mock_post.return_value = mock_response

        access_token = await social_lib.get_access_token(config_settings)

        assert access_token == "mock_new_token"


@pytest.mark.asyncio
async def test_get_access_token_bad_response(social_lib, config_settings):
    with patch.object(social_lib.client, "post", new=AsyncMock()) as mock_post:
        mock_response = AsyncMock()
        mock_response.status_code = 400
        mock_response.json = MagicMock(return_value={})
        mock_post.return_value = mock_response

        with pytest.raises(
            ValueError, match="Can't get access_token and refresh_token"
        ):
            await social_lib.get_access_token(config_settings)


@pytest.mark.asyncio
async def test_extract_url(social_lib):
    expected_url = "https://mock_example_link"
    json_data = {"jquery": [["", [expected_url, ""]]]}

    result_url = await social_lib.extract_url(json=json_data)

    assert result_url == expected_url


@pytest.mark.asyncio
async def test_post_successful(social_lib):
    expected_url = "https://mock_example_link"
    social_lib.get_access_token = AsyncMock(return_value="mock_access_token")
    with patch.object(social_lib.client, "post", new=AsyncMock()) as mock_post:
        mock_response = AsyncMock()
        mock_response.json = MagicMock(
            return_value={
                "success": True,
                "jquery": [["", [expected_url, ""]]],
            }
        )
        mock_post.return_value = mock_response

        url = await social_lib.post()

        assert url == expected_url


@pytest.mark.asyncio
async def test_post_fail(social_lib):
    social_lib.get_access_token = AsyncMock(return_value="mock_access_token")
    with patch.object(social_lib.client, "post", new=AsyncMock()) as mock_post:
        mock_response = AsyncMock()
        mock_response.json = MagicMock(
            return_value={
                "success": False,
            }
        )
        mock_response.text = "Can't get access_token and refresh_token"
        mock_post.return_value = mock_response

        with pytest.raises(
            ValueError, match="Can't get access_token and refresh_token"
        ):
            await social_lib.post()
