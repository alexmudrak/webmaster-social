import asyncio
from typing import Coroutine, List, Optional

from core.database import get_or_create, get_session_context
from core.logger import get_logger
from httpx import AsyncClient
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


# TODO: Need to refactoring full class
class SocialNetworksController:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def run_task_send_article_to_networks(
        self, article: Article, networks_setting: list[Setting]
    ):
        async with await get_request_client() as client:
            tasks = [
                self.send_to_single_network(client, network_config, article)
                for network_config in networks_setting
            ]
            results_list = await asyncio.gather(*tasks)
            results = {name: status for name, status in results_list}

        if results and article:
            await self.send_notification(article, results)

    async def run_task_send_article_to_network(
        self, article: Article, network_setting: Setting
    ):
        async with await get_request_client() as client:
            network_name, publish_status = await self.send_to_single_network(
                client, network_setting, article
            )

            result = {network_name: publish_status}
            await self.send_notification(article, result)

    async def get_article(
        self,
        project_id: int,
        networks_count: int,
        setting_exists: Optional[Setting] | None = None,
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

        if setting_exists:
            query = (
                select(Article)
                .where(Article.project_id == project_id)
                .outerjoin(PublishArticleStatus)
                .group_by(text("Article.id"))
                .having(
                    func.count(
                        PublishArticleStatus.setting_id == setting_exists.id
                    )
                    == 0
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
        client: AsyncClient,
        network_config: Setting,
        article: Article,
    ) -> tuple[str, PublishArticleStatus]:
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

            # TODO: Investigate to optimize
            config = await get_or_create(
                session,
                Setting,
                id=network_config.id,
            )

            await session.commit()

            try:
                logger.debug(
                    f"Try to send {article.id} to " f"`{network_config.name}`"
                )

                url = await send_to_network(
                    session,
                    client,
                    config,
                    article,
                )

                publish_status.status = "DONE"
                publish_status.publish_article_link = url
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

    async def get_setting_by_name(
        self,
        networks_config: list[Setting],
        network_name: str | None,
    ) -> Optional[Setting]:
        return next(
            (
                setting
                for setting in networks_config
                if setting.name == network_name
            ),
            None,
        )

    def get_done_status(self, article: Article) -> set[int | None]:
        return {
            publish.setting_id
            for publish in article.published
            if publish.status == "DONE"
            or (publish.status == "ERROR" and publish.try_count >= 3)
        }

    def create_network_tasks(
        self,
        network_name: str | None,
        setting_exists: Optional[Setting],
        networks_config: list[Setting],
        done_status: set[int | None],
        client: AsyncClient,
        article: Article,
    ) -> list[Coroutine]:
        tasks = []
        if not network_name:
            tasks = [
                self.send_to_single_network(client, network_config, article)
                for network_config in networks_config
                if network_config.id not in done_status
            ]
        elif setting_exists:
            tasks.append(
                self.send_to_single_network(client, setting_exists, article)
            )

        return tasks

    async def send_notification(
        self, article: Article, results: dict[str, PublishArticleStatus]
    ):
        result_data = NotificationData(
            project_name=article.project.name,
            article_title=article.title,
            article_url=article.url,
            publish_statuses=results,
        )
        await NotificationSender().send_message(result_data)

    async def send_article_to_networks(
        self,
        project_id: int,
        network_name: str | None = None,
    ):
        # TODO: Add documentation
        try:
            networks_config = await self.get_networks_config(project_id)
            setting_exists = await self.get_setting_by_name(
                networks_config,
                network_name,
            )

            article = await self.get_article(
                project_id,
                len(networks_config),
                setting_exists=setting_exists,
            )

            if network_name and not setting_exists:
                logger.error(
                    f"Network config for `{network_name}` "
                    f"of Project `{project_id}` not found"
                )
                return

            if not article:
                logger.error("Articles for publishing not found")
                return

            done_status = self.get_done_status(article)

            async with await get_request_client() as client:
                tasks = self.create_network_tasks(
                    network_name,
                    setting_exists,
                    networks_config,
                    done_status,
                    client,
                    article,
                )
                results_list = await asyncio.gather(*tasks)
                results = {name: status for name, status in results_list}

            await self.session.close()

            if results and article:
                await self.send_notification(article, results)
        finally:
            await self.session.close()
