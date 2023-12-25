from typing import Dict, Type

from httpx import AsyncClient
from models.article import Article
from models.setting import Setting
from services.social_networks.libs.abstract import SocialNetworkAbstract
from services.social_networks.libs.vkontakte import VkontakteLib
from sqlmodel.ext.asyncio.session import AsyncSession

# After implementing a new social network library
# it needs to be added to the registry
NETWORK_REGISTER: Dict[str, Type[SocialNetworkAbstract]] = {
    "vkontakte": VkontakteLib,
}


async def send_to_network(
    session: AsyncSession,
    client: AsyncClient,
    config: Setting,
    article: Article,
):
    network_lib = NETWORK_REGISTER.get(config.name)

    if not network_lib:
        raise NotImplementedError(
            f"A lib for network `{config.name}` " "is not implemented yet."
        )

    network_object = network_lib(
        session,
        client,
        config,
        article,
    )

    # Start send to network
    # TODO: Prepare article for publishing
    await network_object.post()
