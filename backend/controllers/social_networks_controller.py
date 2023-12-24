from models.article import Article
from models.setting import Setting
from services.social_networks.register import send_to_network
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.request_client import get_request_client


class SocialNetworksController:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_older_article(self, project_id: int) -> Article:
        # TODO: need to implement
        return Article

    async def get_networks_config(self, project_id: int) -> list[Setting]:
        # TODO: need to implement
        return [Setting]

    async def send_article(self, project_id: int):
        # TODO: Add documentation

        # TODO: Get older article which not send to
        #       social
        article: Article = await self.get_older_article(project_id)

        # TODO: Get social network settings which linked
        #       to project
        networks_config: list[Setting] = await self.get_networks_config(
            project_id
        )

        # TODO: Send article to available social networks
        # TODO: Save SendingModel result to DB

        async with await get_request_client() as client:
            for network_config in networks_config:
                await send_to_network(
                    self.session, client, network_config, article
                )
