from models.article import ArticleBase
from pydantic import validator
from utils.string_handler import truncate_text


class ArticleRead(ArticleBase):
    @validator("body")
    def truncate_body(cls, value):
        return truncate_text(value, 100)
