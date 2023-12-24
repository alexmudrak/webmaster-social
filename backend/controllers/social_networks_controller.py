from typing import List, Optional

from models.article import Article
from models.publish_article_status import PublishArticleStatus
from models.setting import Setting
from services.social_networks.register import send_to_network
from sqlmodel import and_, distinct, func, or_, select, text
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.request_client import get_request_client


class SocialNetworksController:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_article(
        self,
        project_id: int,
        networks_count: int,
    ) -> Optional[Article]:
        # TODO: Add documentation
        query = (
            select(Article)
            .where(Article.project_id == project_id)
            .outerjoin(PublishArticleStatus)
            .group_by(text("Article.id"))
            .having(
                or_(
                    func.count(PublishArticleStatus.id) is None,
                    func.count(distinct(PublishArticleStatus.setting_id))
                    < networks_count,
                    and_(
                        func.count(distinct(PublishArticleStatus.setting_id))
                        >= networks_count,
                        func.bool_or(
                            PublishArticleStatus.publish_status == "ERROR"
                        ),
                    ),
                )
            )
        )

        result = await self.session.exec(query)
        article = result.unique().first()

        return article

    async def get_networks_config(self, project_id: int) -> List[Setting]:
        # TODO: Add documentation
        query = select(Setting).where(Setting.project_id == project_id)

        result = await self.session.exec(query)
        settings = list(result.unique().all())

        return settings

    async def send_article(self, project_id: int):
        # TODO: Add documentation

        networks_config: list[Setting] = await self.get_networks_config(
            project_id
        )
        article = await self.get_article(project_id, len(networks_config))

        # TODO: Send article to available social networks
        # TODO: Save SendingModel result to DB

        async with await get_request_client() as client:
            for network_config in networks_config:
                await send_to_network(
                    self.session, client, network_config, article
                )
