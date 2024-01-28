from models.log_entry import LogEntry
from sqlmodel import desc, select


class LogsRepository:
    def __init__(self, session):
        self.session = session

    async def retrieve_all_logs(self) -> list[LogEntry]:
        query = select(LogEntry).order_by(desc(LogEntry.created))
        result = await self.session.exec(query)
        objects = result.unique().all()
        return list(objects)
