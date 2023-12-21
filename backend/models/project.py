from typing import TYPE_CHECKING, List

from models.mixins import BaseTimestampMixin
from sqlalchemy import Column, UniqueConstraint
from sqlmodel import JSON, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.setting import Setting


class ProjectBase(SQLModel):
    name: str = Field(..., title="Project Name")
    url: str = Field(
        ..., title="The URL of the project where the materials are published."
    )
    parse_type: str = Field(default="html", nullable=False)
    parse_last_material: int = Field(default=10, nullable=False)
    parse_material_id_element: dict = Field(
        default=dict(), sa_column=Column(JSON)
    )
    parse_material_url_element: dict = Field(
        default=dict(), sa_column=Column(JSON)
    )
    parse_material_img_element: dict = Field(
        default=dict(), sa_column=Column(JSON)
    )
    parse_material_body_element: dict = Field(
        default=dict(), sa_column=Column(JSON)
    )
    active: bool = Field(default=True, title="Active Status")


class Project(ProjectBase, BaseTimestampMixin, table=True):
    # type: ignore
    id: int = Field(default=None, nullable=False, primary_key=True)
    networks_setting: List["Setting"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "joined"},
    )

    __table_args__ = (
        UniqueConstraint("name", "url", name="unique_name_url"),
        {"extend_existing": True},
    )
