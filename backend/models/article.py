from typing import TYPE_CHECKING, List, Optional

from models.mixins import BaseTimestampMixin
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.article_status import ArticleStatus
    from models.project import Project


class ArticleBase(SQLModel):
    url: str = Field(nullable=False)
    title: str = Field(nullable=True)
    img_url: str = Field(nullable=True)
    body: str = Field(nullable=True)
    project_id: Optional[int] = Field(
        default=None, nullable=True, foreign_key="project.id"
    )


class Article(ArticleBase, BaseTimestampMixin, table=True):
    # type: ignore
    project: "Project" = Relationship(
        back_populates="articles",
    )
    published: List["ArticleStatus"] = Relationship(
        back_populates="article",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    __table_args__ = (
        UniqueConstraint("project_id", "url", name="unique_project_url"),
        {"extend_existing": True},
    )
