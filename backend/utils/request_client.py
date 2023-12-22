from httpx import AsyncClient


async def get_request_client() -> AsyncClient:
    client = AsyncClient()
    return client
