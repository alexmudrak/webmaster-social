from models.article_status import ArticleStatus
from sqlmodel import desc, select


class ArticlesStatusesRepository:
    def __init__(self, session):
        self.session = session

    async def retrieve_last_5_id_articles_statuses(
        self,
    ) -> list[int]:
        query = select(ArticleStatus.article_id).order_by(
            desc(ArticleStatus.created)
        )
        result = await self.session.exec(query)
        objects = result.unique().all()

        return objects[:5]
