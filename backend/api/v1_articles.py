from controllers.articles_controller import ArticlesController
from core.database import get_session
from fastapi import APIRouter, Depends
from schemas.articles_schema import ArticleRead
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)


@router.get(
    "/",
    summary="Get all articles from DB.",
    response_model=list[ArticleRead],
)
async def get_all_articles(
    session: AsyncSession = Depends(get_session),
):
    # TODO: Add pager
    return await ArticlesController(session).get_all_objects()
