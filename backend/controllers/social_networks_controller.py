import asyncio
from typing import List, Optional

from core.database import get_or_create, get_session_context
from core.logger import get_logger
from fastapi import HTTPException
from models.article import Article
from models.publish_article_status import PublishArticleStatus
from models.setting import Setting
from services.notification.notification_service import (
    NotificationData,
    NotificationSender,
)
from services.social_networks.register import send_to_network
from sqlmodel import and_, distinct, func, or_, select, text
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.request_client import get_request_client

logger = get_logger(__name__)


class SocialNetworksController:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_article(
        self,
        project_id: int,
        networks_count: int,
    ) -> Optional[Article]:
        # TODO: Add documentation
        # TODO: Need to refactoring
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
                        # TODO: Perhaps get this value max `try_count` from
                        # project config for network
                        func.every(PublishArticleStatus.try_count < 3),
                        func.bool_or(PublishArticleStatus.status == "ERROR"),
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

    async def send_to_single_network(
        self,
        client,
        network_config,
        article,
    ):
        # Need to check status for network config
        # Active or not Active
        logger.info(
            f"Start work with `{article.project.name}` - "
            f"`{network_config.name}` - {article.id}"
        )
        async with get_session_context() as session:
            publish_status = await get_or_create(
                session,
                PublishArticleStatus,
                article_id=article.id,
                setting_id=network_config.id,
            )

            publish_status.status = "PENDING"
            publish_status.status_text = None
            publish_status.try_count += 1

            await session.commit()

            try:
                logger.debug(
                    f"Try to send {article.id} to " f"`{network_config.name}`"
                )

                await send_to_network(
                    session,
                    client,
                    network_config,
                    article,
                )

                publish_status.status = "DONE"
            except Exception as error:
                publish_status.status = "ERROR"
                publish_status.status_text = str(error)
                logger.error(
                    f"Error when sending {article.id} to"
                    f"`{network_config.name}`. "
                    f"Error: {publish_status.status_text}"
                )
            finally:
                await session.commit()
                logger.info(
                    f"Complete work with `{article.project.name}` - "
                    f"`{network_config.name}` - {article.id} - "
                    f"Status: {publish_status.status}"
                )

        return network_config.name, publish_status

    async def send_article_to_networks(self, project_id: int):
        # TODO: Add documentation
        networks_config = await self.get_networks_config(project_id)
        article = await self.get_article(project_id, len(networks_config))

        if not article:
            raise HTTPException(
                status_code=404, detail="Articles for publishing not found"
            )

        done_status = {
            publish.setting_id
            for publish in article.published
            if publish.status == "DONE"
            or (publish.status == "ERROR" and publish.try_count >= 3)
        }

        async with await get_request_client() as client:
            tasks = []
            for network_config in networks_config:
                if network_config.id not in done_status:
                    task = self.send_to_single_network(
                        client,
                        network_config,
                        article,
                    )
                    tasks.append(task)

            results_list = await asyncio.gather(*tasks)
            results = {name: status for name, status in results_list}

        await self.session.close()

        # Send notification
        result_data = NotificationData(
            project_name=article.project.name,
            article_title=article.title,
            article_url=article.url,
            publish_statuses=results,
        )

        await NotificationSender().send_message(result_data)
