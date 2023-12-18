from datetime import datetime
from typing import Optional

from pydantic import Field as PydanticField
from pydantic import HttpUrl
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class ProjectBase(SQLModel):
    name: str = PydanticField(..., title="Project Name")
    url: str = PydanticField(..., title="Project URL")
    active: Optional[bool] = PydanticField(None, title="Active Status")


class Project(ProjectBase, table=True):
    # type: ignore
    id: int = Field(default=None, nullable=False, primary_key=True)
    created: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    __table_args__ = (UniqueConstraint("name", "url", name="unique_name_url"),)


class ProjectCreate(ProjectBase):
    url: HttpUrl


class ProjectUpdate(ProjectCreate):
    pass
