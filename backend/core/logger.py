import asyncio
import logging

from core.database import get_session_context
from core.settings import Settings
from models.log_entry import LogEntry

SETTINGS = Settings()


class DatabaseHandler(logging.Handler):
    def emit(self, record):
        asyncio.create_task(self.async_emit(record))

    async def async_emit(self, record):
        log_entry = LogEntry(
            level=record.levelname.replace(":", ""),
            logger_name=record.name,
            message=self.format(record),
        )

        async with get_session_context() as session:
            session.add(log_entry)
            await session.commit()


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = f"{record.levelname}:"
        return super().format(record)


def get_logger(
    logger_name: str,
    log_level: int | str | None = None,
):
    logger = logging.getLogger(logger_name)

    if not logger.handlers:
        logger.setLevel(log_level or SETTINGS.LOG_LEVEL)

        formatter = CustomFormatter(
            "%(levelname)-9s %(asctime)s - [%(name)s] - %(message)s"
        )
        db_formatter = logging.Formatter("%(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        db_handler = DatabaseHandler()
        db_handler.setFormatter(db_formatter)
        logger.addHandler(db_handler)

        logger.propagate = False

    return logger
