import pytest
from utils.cloudflare_handler import cloudflare_decode_email


@pytest.mark.asyncio
async def test_cloudflare_decode_email():
    encoded_string = "36534e575b465a53765b575f5a1855595b"
    expected_result = "example@mail.com"

    result = await cloudflare_decode_email(encoded_string)
    assert result == expected_result
