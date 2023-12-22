import pytest
from httpx import AsyncClient
from utils.request_client import get_request_client


@pytest.mark.asyncio
async def test_get_request_client():
    result = await get_request_client()
    assert isinstance(result, AsyncClient)

    result_1 = await get_request_client()
    result_2 = await get_request_client()
    assert result_1 is not result_2

    async with result_1 as client:
        assert not client.is_closed

    assert client.is_closed
