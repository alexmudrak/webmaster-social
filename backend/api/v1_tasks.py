from controllers.parser_controller import ParserController
from controllers.social_networks_controller import SocialNetworksController
from core.database import get_session
from fastapi import APIRouter, BackgroundTasks, Depends
from schemas.task_schema import TaskResponse
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "/collect-articles/{project_id}",
    summary="Run collect task.",
    response_model=TaskResponse,
)
async def run_collect_task(
    project_id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    background_tasks.add_task(
        ParserController(session).collect_data, project_id
    )

    return TaskResponse(
        task_type="collect_data", networks="", status="success"
    )


@router.post(
    "/send-article/{project_id}",
    summary="Send collected article to all social networks task.",
    response_model=TaskResponse,
)
async def send_article_task(
    project_id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    background_tasks.add_task(
        SocialNetworksController(session).send_article_to_networks, project_id
    )

    return TaskResponse(
        task_type="send_article", networks="all", status="success"
    )


@router.post(
    "/send-article/{project_id}/{network_name}",
    summary="Send collected article to single social network task.",
    response_model=TaskResponse,
)
async def send_singel_article_task(
    project_id: int,
    network_name: str,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    background_tasks.add_task(
        SocialNetworksController(session).send_article_to_networks,
        project_id,
        network_name,
    )

    return TaskResponse(
        task_type="send_article", networks=network_name, status="success"
    )
