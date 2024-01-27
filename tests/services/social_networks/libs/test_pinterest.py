from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from services.social_networks.libs.pinterest import PinterestLib as Lib


@pytest.fixture
def config_settings():
    return {
        "board_id": "testboardid",
        "cookies": {"csrftoken": "testtoken"},
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
    assert config["board_id"] == "testboardid"
    assert config["cookies"] == {"csrftoken": "testtoken"}


@pytest.mark.asyncio
async def test_get_config_invalid_format(social_lib):
    social_lib.config.settings = None

    with pytest.raises(ValueError) as exc_info:
        await social_lib.get_config()

    assert "Invalid config format" in str(exc_info.value)


@pytest.mark.asyncio
async def test_prepare_post(social_lib):
    expected_message = (
        "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. "
        "Aeneancommodo ligula eget dolor. Aenean massa. Cum sociis "
        "natoquepenatibus et magnis dis parturient montes, nascetur "
        "ridiculus. Donec quam..."
    )
    post = await social_lib.prepare_post()

    assert post["message"] == expected_message


@pytest.mark.asyncio
async def test_extract_url(social_lib):
    expected_url = "https://ru.pinterest.com/pin/123456/"
    json_data = {"resource_response": {"data": {"id": "123456"}}}

    result_url = await social_lib.extract_url(json=json_data)

    assert result_url == expected_url


@pytest.mark.asyncio
async def test_post_successful(social_lib):
    expected_url = "https://ru.pinterest.com/pin/123456/"

    with patch.object(
        social_lib.client,
        "post",
        new=AsyncMock(),
    ) as mock_post:
        mock_response = AsyncMock()
        mock_response.json = MagicMock(
            return_value={
                "resource_response": {"data": {"id": "123456"}},
            }
        )
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        url = await social_lib.post()

        assert url == expected_url
