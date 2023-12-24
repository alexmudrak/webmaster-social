from typing import TYPE_CHECKING, Optional

from models.mixins import BaseTimestampMixin
from sqlalchemy import Column, UniqueConstraint
from sqlmodel import JSON, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.project import Project
    from models.publish_article_status import PublishArticleStatus


class SettingBase(SQLModel):
    name: str = Field(..., title="Settings Name")
    settings: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    project_id: Optional[int] = Field(
        default=None, nullable=True, foreign_key="project.id"
    )
    active: Optional[bool] = Field(
        default=True, nullable=False, title="Active Status"
    )


class Setting(SettingBase, BaseTimestampMixin, table=True):
    # type: ignore
    project: Optional["Project"] = Relationship(
        back_populates="networks_setting",
        sa_relationship_kwargs={"lazy": "joined"},
    )
    published: Optional["PublishArticleStatus"] = Relationship(
        back_populates="networks_setting",
        sa_relationship_kwargs={"lazy": "joined"},
    )

    __tableargs__ = (
        UniqueConstraint("name", "project_id", name="unique_name_project"),
        {"extend_existing": True},
    )
