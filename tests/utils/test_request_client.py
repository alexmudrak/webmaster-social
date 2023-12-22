import pytest
from httpx import AsyncClient
from utils.request_client import get_request_client


@pytest.mark.asyncio
async def test_get_request_client():
    # Тестирование возвращаемого типа
    result = await get_request_client()
    assert isinstance(result, AsyncClient)

    # Тестирование, что возвращается новый экземпляр
    result_1 = await get_request_client()
    result_2 = await get_request_client()
    assert result_1 is not result_2

    # Тестирование закрытия клиента после использования
    async with result_1 as client:
        assert not client.is_closed

    assert client.is_closed

    # Дополнительные тесты, если необходимо
