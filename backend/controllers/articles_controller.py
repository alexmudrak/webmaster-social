from core.logger import get_logger
from repositories.articles_repository import ArticlesReposotiry
from schemas.articles_schema import ArticleRead
from sqlmodel.ext.asyncio.session import AsyncSession

logger = get_logger(__name__)


class ArticlesController:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_objects(self) -> list[ArticleRead]:
        logs = await ArticlesReposotiry(self.session).retrieve_all_articles()

        return logs
