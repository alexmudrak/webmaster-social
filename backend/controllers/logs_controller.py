from core.logger import get_logger
from models.log_entry import LogEntry
from repositories.logs_repository import LogsReposotiry
from sqlmodel.ext.asyncio.session import AsyncSession

logger = get_logger(__name__)


class LogsController:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_objects(self) -> list[LogEntry]:
        logs = await LogsReposotiry(self.session).retrieve_all_logs()

        return logs
