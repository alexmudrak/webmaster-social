from controllers.parser_controller import ParserController
from core.database import get_session
from fastapi import APIRouter, BackgroundTasks, Depends
from schemas.task_schema import TaskResponse
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "/",
    summary="Run collect task.",
    response_model=TaskResponse,
)
async def run_collect_task(
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    background_tasks.add_task(ParserController(session).collect_data, 1)
    return TaskResponse(task_type="collect_data", status="success")
