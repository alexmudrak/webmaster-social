from datetime import datetime

from fastapi import HTTPException
from models.project import Project, ProjectCreate, ProjectUpdate
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class ProjectController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_objects(self) -> list[Project]:
        query = select(Project)
        result = await self.session.exec(query)
        projects = result.all()
        return list(projects)

    async def get_object(self, object_id: int) -> Project:
        project = await self.session.get(Project, object_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    async def create_object(self, object_data: ProjectCreate) -> Project:
        if not object_data.url:
            raise HTTPException(status_code=400, detail="Invalid URL provided")

        existing_project = await self.session.exec(
            select(Project).where(
                (Project.name == object_data.name)
                & (Project.url == str(object_data.url))
            )
        )
        existing_project = existing_project.one_or_none()

        if existing_project:
            raise HTTPException(
                status_code=409,
                detail=(
                    "A project with the same name and "
                    "URL combination already exists."
                ),
            )

        project = Project(
            name=object_data.name,
            url=str(object_data.url),
            active=object_data.active,
        )
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def update_object(
        self, object_id: int, object_data: ProjectUpdate
    ) -> Project:
        if not object_data.url:
            raise HTTPException(status_code=400, detail="Invalid URL provided")

        project = await self.session.get(Project, object_id)

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        project.name = object_data.name
        project.url = str(object_data.url)
        project.active = object_data.active
        project.updated = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def delete_object(self, object_id: int) -> dict[str, str]:
        project = await self.session.get(Project, object_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        await self.session.delete(project)
        await self.session.commit()
        return {"message": f"Project `{object_id}` was deleted"}
