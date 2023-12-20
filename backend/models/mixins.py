from datetime import datetime

from sqlmodel import Field, SQLModel


class BaseTimestampMixin(SQLModel):
    created: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated: datetime = Field(default_factory=datetime.utcnow, nullable=False)
