import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from services.social_networks.libs.telegraph import TelegraphLib as Lib


@pytest.fixture
def config_settings():
    return {
        "author_name": "testauthorname",
        "access_token": "testtoken",
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
    assert config["author_name"] == "testauthorname"
    assert config["access_token"] == "testtoken"


@pytest.mark.asyncio
async def test_get_config_invalid_format(social_lib):
    social_lib.config.settings = None

    with pytest.raises(ValueError) as exc_info:
        await social_lib.get_config()

    assert "Invalid config format" in str(exc_info.value)


@pytest.mark.asyncio
async def test_prepare_post(social_lib):
    image = social_lib.article.img_url
    message = social_lib.article.body
    link = social_lib.article.url

    expected_message = json.dumps(
        [
            {"tag": "img", "attrs": {"src": image}},
            {"tag": "p", "children": [f"{message}\n\n{link}"]},
        ]
    )
    post = await social_lib.prepare_post()

    assert post["content"] == expected_message


@pytest.mark.asyncio
async def test_extract_url(social_lib):
    expected_url = "https://example-telegraph-url/123456/"
    json_data = {"result": {"url": expected_url}}

    result_url = await social_lib.extract_url(json=json_data)

    assert result_url == expected_url


@pytest.mark.asyncio
async def test_post_successful(social_lib):
    expected_url = "https://example-telegraph-url/123456/"

    with patch.object(
        social_lib.client,
        "post",
        new=AsyncMock(),
    ) as mock_post:
        mock_response = AsyncMock()
        mock_response.json = MagicMock(
            return_value={
                "result": {
                    "url": expected_url,
                    "ok": True,
                },
            }
        )
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        url = await social_lib.post()

        assert url == expected_url
