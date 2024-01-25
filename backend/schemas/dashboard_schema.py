from datetime import datetime

from pydantic import BaseModel


class ArticleCard(BaseModel):
    total: int | None
    published: int | None
    with_error: int | None


class ProjectCard(BaseModel):
    total: int | None


class NetworkCard(BaseModel):
    total: int | None


class DashboardCardData(BaseModel):
    articles: ArticleCard
    projects: ProjectCard
    networks: NetworkCard


class DashboardNetworkStatusesData(BaseModel):
    id: int
    name: str
    status: str
    status_text: str | None


class DashboardStatusesData(BaseModel):
    date: datetime
    project_name: str
    article_id: int
    article_title: str
    network_statuses: list[DashboardNetworkStatusesData]
