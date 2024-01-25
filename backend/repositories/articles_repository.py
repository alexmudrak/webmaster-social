from models.article import Article
from schemas.articles_schema import ArticleNetworkStatus, ArticleRead
from sqlmodel import desc, select


class ArticlesReposotiry:
    def __init__(self, session):
        self.session = session

    async def retrieve_all_articles(self) -> list[ArticleRead]:
        query = select(Article).order_by(desc(Article.created))
        result = await self.session.exec(query)
        objects = result.unique().all()

        articles_with_project_name = [
            ArticleRead(
                **object.model_dump(),
                project_name=object.project.name if object.project else None,
                network_statuses=[
                    ArticleNetworkStatus(
                        id=published.networks_setting.id,
                        name=published.networks_setting.name,
                        status=published.status,
                        status_text=published.status_text,
                        url=published.publish_article_link,
                    )
                    for published in object.published
                ],
            )
            for object in objects
        ]

        return articles_with_project_name

    async def retrieve_article_by_id(self, article_id: int) -> Article:
        query = select(Article).where(
            Article.id == article_id,
        )
        result = await self.session.exec(query)
        object = result.unique().first()

        return object

    async def retrieve_article_by_list_id(
        self, articles_id: list[int]
    ) -> list[Article]:
        query = select(Article).where(Article.id.in_(articles_id))
        result = await self.session.exec(query)
        objects = result.unique().all()

        return objects
