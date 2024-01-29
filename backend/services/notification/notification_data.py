from dataclasses import dataclass

from models.article_status import ArticleStatus


@dataclass
class NotificationData:
    project_name: str
    article_title: str
    article_url: str
    publish_statuses: dict[str, ArticleStatus]
    message: str = ""
    done_status_count: int = 0
    fail_status_count: int = 0
