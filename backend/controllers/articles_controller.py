from controllers.social_networks_controller import SocialNetworksController
from core.logger import get_logger
from repositories.articles_repository import ArticlesReposotiry
from repositories.settings_repository import SettingsReposotiry
from schemas.articles_schema import ArticleRead
from sqlmodel.ext.asyncio.session import AsyncSession

logger = get_logger(__name__)


class ArticlesController:
    def __init__(self, db_manager: AsyncSession):
        self.db_manager = db_manager

    async def get_all_objects(self) -> list[ArticleRead]:
        async with self.db_manager as session:
            logs = await ArticlesReposotiry(session).retrieve_all_articles()

        return logs

    async def send_article_to_networks(
        self,
        article_id: int,
        network_name: str,
    ):
        async with self.db_manager as session:
            article = await ArticlesReposotiry(session).retrieve_article_by_id(
                article_id
            )
            network_config = await SettingsReposotiry(
                session
            ).retrieve_setting_by_project_id_and_network_name(
                article.project.id, network_name
            )
            await SocialNetworksController(
                session
            ).run_task_send_article_and_by_network(article, network_config)
