from datetime import datetime

from sqlmodel import Field, SQLModel


class BaseTimestampMixin(SQLModel):
    # type: ignore
    id: int = Field(default=None, nullable=False, primary_key=True)
    created: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated: datetime = Field(default_factory=datetime.utcnow, nullable=False)
