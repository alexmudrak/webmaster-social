from controllers.articles_controller import ArticlesController
from core.database import get_session, get_session_context
from fastapi import APIRouter, BackgroundTasks, Depends
from schemas.articles_schema import ArticleRead
from schemas.task_schema import TaskResponse
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
    db_manager: AsyncSession = Depends(get_session_context),
):
    # TODO: Add pager
    return await ArticlesController(db_manager).get_all_objects()


@router.post(
    "/task/{article_id}",
    summary="Task for sending article to all networks.",
)
async def send_article_to_all_networks(
    article_id: int,
    session: AsyncSession = Depends(get_session),
):
    pass


@router.post(
    "/task/{article_id}/{network_name}",
    summary="Task for sending article to a specific network.",
    tags=["Tasks"],
    response_model=TaskResponse,
)
async def send_article_to_all_specific(
    article_id: int,
    network_name: str,
    background_tasks: BackgroundTasks,
    db_manager: AsyncSession = Depends(get_session_context),
):
    background_tasks.add_task(
        ArticlesController(db_manager).send_article_to_networks,
        article_id,
        network_name,
    )

    return TaskResponse(
        task_type="send_article_to_network",
        networks=network_name,
        status="success",
    )
