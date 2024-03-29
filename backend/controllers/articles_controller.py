from controllers.social_networks_controller import SocialNetworksController
from core.logger import get_logger
from repositories.articles_repository import ArticlesRepository
from repositories.settings_repository import SettingsRepository
from schemas.articles_schema import ArticleRead
from sqlmodel.ext.asyncio.session import AsyncSession

logger = get_logger(__name__)


class ArticlesController:
    def __init__(self, db_manager: AsyncSession):
        self.db_manager = db_manager

    async def get_all_objects(self) -> list[ArticleRead]:
        async with self.db_manager as session:
            logs = await ArticlesRepository(session).retrieve_all_articles()

        return logs

    async def send_article_to_networks(
        self,
        article_id: int,
    ):
        async with self.db_manager as session:
            article = await ArticlesRepository(session).retrieve_article_by_id(
                article_id
            )
            networks_config = await SettingsRepository(
                session
            ).retrieve_settings_by_project_id(article.project.id)

            await SocialNetworksController(
                session
            ).run_task_send_article_to_networks(article, networks_config)

    async def send_article_to_network(
        self,
        article_id: int,
        network_name: str,
    ):
        async with self.db_manager as session:
            article = await ArticlesRepository(session).retrieve_article_by_id(
                article_id
            )
            network_config = await SettingsRepository(
                session
            ).retrieve_setting_by_project_id_and_network_name(
                article.project.id, network_name
            )
            await SocialNetworksController(
                session
            ).run_task_send_article_to_network(article, network_config)
