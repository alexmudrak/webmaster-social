from typing import TYPE_CHECKING, List, Optional

from models.mixins import BaseTimestampMixin
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.article import Article
    from models.setting import Setting


class PublishArticleStatusBase(SQLModel):
    # TODO: Rename `publish_article_link` to `url`
    article_id: int = Field(nullable=False, foreign_key="article.id")
    setting_id: int = Field(nullable=False, foreign_key="setting.id")
    status: str = Field(nullable=False, default="PENDING")
    status_text: Optional[str] = Field(nullable=True, default=None)
    try_count: int = Field(nullable=False, default=0)
    publish_article_link: Optional[str] = Field(nullable=True, default=None)


class PublishArticleStatus(
    PublishArticleStatusBase, BaseTimestampMixin, table=True
):
    # type: ignore
    article: "Article" = Relationship(
        back_populates="published",
        sa_relationship_kwargs={"lazy": "joined"},
    )
    networks_setting: List["Setting"] = Relationship(
        back_populates="published",
        sa_relationship_kwargs={"lazy": "joined"},
    )

    __tablename__ = "publish_article_status"
    __table_args__ = (
        UniqueConstraint(
            "article_id", "setting_id", name="unique_article_setting"
        ),
        {"extend_existing": True},
    )
