from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from services.social_networks.libs.twitter import TwitterLib as Lib


@pytest.fixture
def config_settings():
    return {
        "client_id": "testclientid",
        "client_secret": "testclientsecret",
        "refresh_token": "testtoken",
        "redirect_uri": "testredirecturi",
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
    assert config["client_id"] == "testclientid"
    assert config["refresh_token"] == "testtoken"


@pytest.mark.asyncio
async def test_get_updated_token_success(social_lib, config_settings):
    new_token = {
        "refresh_token": "new_refresh_token",
        "access_token": "new_access_token",
    }
    client_mock = AsyncMock()
    client_mock.refresh_token = MagicMock(return_value=new_token)
    session_mock = MagicMock()

    social_lib.session = session_mock

    result = await social_lib.get_updated_token(client_mock, config_settings)

    assert result == new_token
    assert config_settings["refresh_token"] == new_token["refresh_token"]
    assert social_lib.config.settings == config_settings
    session_mock.add.assert_called_with(social_lib.config)


@pytest.mark.asyncio
async def test_get_config_invalid_format(social_lib):
    social_lib.config.settings = None

    with pytest.raises(ValueError) as exc_info:
        await social_lib.get_config()

    assert "Invalid config format" in str(exc_info.value)


@pytest.mark.asyncio
async def test_prepare_post(social_lib):
    expected_message = (
        f"{social_lib.article.title}\n\n" f"{social_lib.article.url}"
    )
    post = await social_lib.prepare_post()
    assert post["message"] == expected_message


@pytest.mark.asyncio
async def test_extract_url(social_lib):
    expected_url = "https://twitter.com/crawler_post/status/123456"
    json_data = {"data": {"id": "123456"}}

    result_url = await social_lib.extract_url(json=json_data)

    assert result_url == expected_url


@pytest.mark.asyncio
async def test_post_successful(social_lib):
    expected_url = "https://twitter.com/crawler_post/status/123456"

    with patch.object(
        social_lib,
        "get_updated_token",
        return_value=MagicMock(
            return_value={"access_token": 123},
        ),
    ), patch.object(
        social_lib.client,
        "post",
        new=AsyncMock(),
    ) as mock_post:
        mock_response = AsyncMock()
        mock_response.json = MagicMock(
            return_value={
                "data": {"id": "123456"},
            }
        )
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        url = await social_lib.post()

        assert url == expected_url
