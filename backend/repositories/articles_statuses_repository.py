from models.publish_article_status import PublishArticleStatus
from sqlmodel import desc, select


class ArticlesStatusesReposotiry:
    def __init__(self, session):
        self.session = session

    async def retrieve_last_5_id_articles_statuses(
        self,
    ) -> list[int]:
        query = select(PublishArticleStatus.article_id).order_by(
            desc(PublishArticleStatus.created)
        )
        result = await self.session.exec(query)
        objects = result.unique().all()

        return objects[:5]
