from datetime import datetime

from models.article import ArticleBase
from pydantic import BaseModel, validator
from utils.string_handler import truncate_text


class ArticleNetworkStatus(BaseModel):
    id: int
    name: str
    status: str
    status_text: str | None
    url: str | None


class ArticleRead(ArticleBase):
    id: int
    created: datetime
    project_name: str | None
    network_statuses: list[ArticleNetworkStatus]

    @validator("body")
    def truncate_body(cls, value):
        return truncate_text(value, 100)
