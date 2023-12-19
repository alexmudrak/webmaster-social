from datetime import datetime
from typing import Optional

from sqlalchemy import Column, UniqueConstraint
from sqlmodel import JSON, Field, SQLModel


class SettingBase(SQLModel):
    name: str = Field(..., title="Settings Name")
    settings: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    project_id: Optional[int] = Field(
        default=None, nullable=True, foreign_key="project.id"
    )
    active: Optional[bool] = Field(None, title="Active Status")


class Setting(SettingBase, table=True):
    # type: ignore
    id: int = Field(default=None, nullable=False, primary_key=True)
    created: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "project_id", name="unique_name_project"),
    )


class SettingCreate(SettingBase):
    pass


class SettingUpdate(SettingCreate):
    pass
