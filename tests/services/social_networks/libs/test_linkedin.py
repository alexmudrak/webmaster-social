from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from services.social_networks.libs.linkedin import LinkedinLib as Lib


@pytest.fixture
def config_settings():
    return {
        "access_token": "testtoken",
        "user_id": "testuserid",
        "client_id": "testclientid",
        "client_secret": "testclientsecret",
    }


@pytest.fixture
def social_lib(
    mock_session,
    mock_client,
    mock_config,
    mock_article,
):
    return Lib(
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
    assert config["access_token"] == "testtoken"
    assert config["client_id"] == "testclientid"


@pytest.mark.asyncio
async def test_get_config_invalid_format(social_lib):
    social_lib.config.settings = None

    with pytest.raises(ValueError) as exc_info:
        await social_lib.get_config()

    assert "Invalid config format" in str(exc_info.value)


@pytest.mark.asyncio
async def test_prepare_post(social_lib, config_settings):
    expected_author = f"urn:li:person:{config_settings['user_id']}"

    post = await social_lib.prepare_post(config_settings)

    assert post["author"] == expected_author


@pytest.mark.asyncio
async def test_extract_url(social_lib):
    expected_url = "https://www.linkedin.com/feed/update/123456/"
    json_data = {"id": "123456"}

    result_url = await social_lib.extract_url(json=json_data)

    assert result_url == expected_url


@pytest.mark.asyncio
async def test_post_successful(social_lib):
    expected_url = "https://www.linkedin.com/feed/update/123456/"
    social_lib.get_access_token = AsyncMock(return_value="mock_access_token")
    with patch.object(social_lib.client, "post", new=AsyncMock()) as mock_post:
        mock_response = AsyncMock()
        mock_response.status_code = 201
        mock_response.json = MagicMock(return_value={"id": "123456"})
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
