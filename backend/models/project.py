from typing import List, Optional

from models.mixins import BaseTimestampMixin
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


class ProjectBase(SQLModel):
    name: str = Field(..., title="Project Name")
    url: str = Field(..., title="Project URL")
    active: Optional[bool] = Field(None, title="Active Status")


class Project(ProjectBase, BaseTimestampMixin, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    setting: List["Setting"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "joined"},
    )

    __table_args__ = (
        UniqueConstraint("name", "url", name="unique_name_url"),
        {"extend_existing": True},
    )
