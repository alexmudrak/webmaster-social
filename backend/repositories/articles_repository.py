from models.article import Article
from sqlmodel import desc, select


class ArticlesReposotiry:
    def __init__(self, session):
        self.session = session

    async def retrieve_all_articles(self) -> list[Article]:
        query = select(Article).order_by(desc(Article.created))
        result = await self.session.exec(query)
        objects = result.unique().all()
        return list(objects)
