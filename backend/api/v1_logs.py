from controllers.logs_controller import LogsController
from core.database import get_session
from fastapi import APIRouter, Depends
from models.log_entry import LogEntry
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
)


@router.get(
    "/",
    summary="Get last logs from DB.",
    response_model=list[LogEntry],
)
async def get_all_logs(
    session: AsyncSession = Depends(get_session),
):
    return await LogsController(session).get_all_objects()
