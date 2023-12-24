from typing import Dict, Type

from httpx import AsyncClient
from models.article import Article
from models.setting import Setting
from services.social_networks.libs.abstract import SocialNetworkAbstract
from sqlmodel.ext.asyncio.session import AsyncSession

# After implementing a new social network library
# it needs to be added to the registry
NETWORK_REGISTER: Dict[str, Type[SocialNetworkAbstract]] = {}


async def send_to_network(
    session: AsyncSession,
    client: AsyncClient,
    network_config: Setting,
    article: Article,
):
    network_lib = NETWORK_REGISTER.get(network_config.name)

    if not network_lib:
        raise NotImplementedError(
            f"A lib for network `{network_config.name}` "
            "is not implemented yet."
        )

    network_object = network_lib(session, client)

    # Start send to network
    # TODO: Prepare article for publishing
    await network_object.post(article)
