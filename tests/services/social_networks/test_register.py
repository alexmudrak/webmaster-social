from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient
from models.article import Article
from models.setting import Setting
from services.social_networks.libs.abstract import SocialNetworkAbstract
from services.social_networks.register import send_to_network
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def mock_network_lib():
    class MockSocialNetworkLib(SocialNetworkAbstract):
        async def post(self):
            return "Mocked post method called"

        @staticmethod
        async def config_validation():
            pass

        async def auth(self):
            pass

        async def get_config(self):
            pass

        async def prepare_post(self):
            pass

        async def extract_url(self):
            pass

    return MockSocialNetworkLib


@pytest.fixture
def mock_network_register(mock_network_lib):
    with patch.dict(
        "services.social_networks.register.NETWORK_REGISTER",
        {"mock_network": mock_network_lib},
    ):
        yield


@pytest.mark.asyncio
async def test_send_to_network(mock_network_register):
    _ = mock_network_register
    session = AsyncMock(spec=AsyncSession)
    client = AsyncMock(spec=AsyncClient)
    config = Setting(name="mock_network")
    article = MagicMock(spec=Article)

    result = await send_to_network(session, client, config, article)

    assert result == "Mocked post method called"
