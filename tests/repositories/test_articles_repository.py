from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from models.article import Article
from repositories.articles_repository import ArticlesRepository
from schemas.articles_schema import ArticleRead
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.mark.asyncio
async def test_retrieve_all_articles(mock_async_session):
    mock_articles = [
        Article(
            id=i,
            created=datetime.strptime("2021-01-01", "%Y-%m-%d"),
            project=MagicMock(name=""),
            published=[],
            url="http://example.com",
            title=f"Article {i}",
            img_url="http://example.com/img-url",
            body="",
        )
        for i in range(5)
    ]

    for i, article in enumerate(mock_articles):
        article.project.name = f"Project {i}"

    mock_exec = MagicMock()
    mock_exec.unique.return_value.all.return_value = mock_articles
    mock_async_session.exec.return_value = mock_exec

    articles_repo = ArticlesRepository(session=mock_async_session)
    result = await articles_repo.retrieve_all_articles()

    assert len(result) == len(mock_articles)
    for article_read, article in zip(result, mock_articles):
        assert isinstance(article_read, ArticleRead)
        assert article_read.id == article.id


@pytest.mark.asyncio
async def test_retrieve_article_by_id(mock_async_session):
    article_id = 1
    mock_article = MagicMock(
        spec=Article,
        id=1,
        created="2021-01-01",
        project=AsyncMock(name=""),
        published=[],
    )
    mock_article.project.name = "Project 1"

    mock_exec = MagicMock()
    mock_exec.unique.return_value.first.return_value = mock_article
    mock_async_session.exec.return_value = mock_exec

    articles_repo = ArticlesRepository(session=mock_async_session)
    result = await articles_repo.retrieve_article_by_id(article_id=article_id)

    assert isinstance(result, Article)
    assert result.id == article_id


@pytest.mark.asyncio
async def test_retrieve_article_by_list_id(mock_async_session):
    article_ids = [1, 2, 3]
    mock_articles = [
        Article(
            id=i,
            created=datetime.strptime("2021-01-01", "%Y-%m-%d"),
            project=MagicMock(name=""),
            published=[],
            url="http://example.com",
            title=f"Article {i}",
            img_url="http://example.com/img-url",
            body="",
        )
        for i in article_ids
    ]

    for i, article in enumerate(mock_articles):
        article.project.name = f"Project {i}"

    mock_exec = MagicMock()
    mock_exec.unique.return_value.all.return_value = mock_articles
    mock_async_session.exec.return_value = mock_exec

    articles_repo = ArticlesRepository(session=mock_async_session)
    result = await articles_repo.retrieve_article_by_list_id(
        articles_id=article_ids
    )

    assert len(result) == len(article_ids)
    for article in result:
        assert article.id in article_ids
