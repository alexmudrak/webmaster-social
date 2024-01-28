from models.project import Project
from schemas.project_schema import ProjectRead
from sqlmodel import desc, select


class ProjectsRepository:
    def __init__(self, session):
        self.session = session

    async def retrieve_all_project_objects(self) -> list[ProjectRead]:
        query = select(Project).order_by(desc(Project.created))
        result = await self.session.exec(query)
        objects = result.unique().all()
        return objects
