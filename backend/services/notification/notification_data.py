from dataclasses import dataclass

from models.publish_article_status import PublishArticleStatus


@dataclass
class NotificationData:
    project_name: str
    article_title: str
    article_url: str
    publish_statuses: dict[str, PublishArticleStatus]
    message: str = ""
    done_status_count: int = 0
    fail_status_count: int = 0
