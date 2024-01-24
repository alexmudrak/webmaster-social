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
