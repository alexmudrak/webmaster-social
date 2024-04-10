from typing import TYPE_CHECKING, List

from models.mixins import BaseTimestampMixin
from sqlalchemy import Column, UniqueConstraint
from sqlmodel import JSON, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.article import Article
    from models.setting import Setting


class ProjectBase(SQLModel):
    name: str = Field(..., title="Project Name")
    url: str = Field(
        ..., title="The URL of the project where the articles are published."
    )
    active: bool = Field(default=True, title="Active Status")
    parse_type: str = Field(default="html", nullable=False)
    parse_last_article_count: int = Field(default=10, nullable=False)
    parse_article_url_element: dict = Field(
        default=dict(), sa_column=Column(JSON)
    )
    parse_article_img_element: dict = Field(
        default=dict(), sa_column=Column(JSON)
    )
    parse_article_body_element: dict = Field(
        default=dict(), sa_column=Column(JSON)
    )


class Project(ProjectBase, BaseTimestampMixin, table=True):
    # type: ignore
    networks_setting: List["Setting"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "joined"},
    )
    articles: List["Article"] = Relationship(
        back_populates="project",
        # sa_relationship_kwargs={"lazy": "joined"},
    )

    __table_args__ = (
        UniqueConstraint("name", "url", name="unique_name_url"),
        {"extend_existing": True},
    )
