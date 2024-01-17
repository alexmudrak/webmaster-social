from models.mixins import BaseTimestampMixin
from sqlmodel import Field, SQLModel


class LogEntryBase(SQLModel):
    level: str = Field(index=True)
    logger_name: str = Field(index=True)
    message: str = Field(index=True)


class LogEntry(LogEntryBase, BaseTimestampMixin, table=True):
    # type: ignore
    __tablename__ = "log_entry"
    __table_args__ = ({"extend_existing": True},)
