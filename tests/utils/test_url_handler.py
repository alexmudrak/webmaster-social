import pytest
from utils.url_handler import get_correct_url


@pytest.mark.asyncio
async def test_get_correct_url_relative():
    original_url = "http://domain.com/path"
    parsed_url = "/some-path-to-node/"
    expected_url = "http://domain.com/some-path-to-node/"

    result_url = await get_correct_url(original_url, parsed_url)
    assert result_url == expected_url


@pytest.mark.asyncio
async def test_get_correct_url_absolute():
    original_url = "http://domain.com/path"
    parsed_url = "http://example.com/absolute-path"
    expected_url = "http://example.com/absolute-path"

    result_url = await get_correct_url(original_url, parsed_url)
    assert result_url == expected_url
