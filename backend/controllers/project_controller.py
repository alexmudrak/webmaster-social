from datetime import datetime

from fastapi import HTTPException
from models.project import Project
from schemas.project_schema import ProjectCreate, ProjectUpdate
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class ProjectController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_objects(self) -> list[Project]:
        query = select(Project)
        result = await self.session.exec(query)
        objects = result.all()
        return list(objects)

    async def get_object(self, object_id: int) -> Project:
        db_object = await self.session.get(Project, object_id)
        if not db_object:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_object

    async def create_object(self, object_data: ProjectCreate) -> Project:
        if not object_data.url:
            raise HTTPException(status_code=400, detail="Invalid URL provided")

        existing_object = await self.session.exec(
            select(Project).where(
                (Project.name == object_data.name)
                & (Project.url == str(object_data.url))
            )
        )
        existing_object = existing_object.unique().one_or_none()

        if existing_object:
            raise HTTPException(
                status_code=409,
                detail=(
                    "A project with the same name and "
                    "URL combination already exists."
                ),
            )

        db_object = Project(
            name=object_data.name,
            url=str(object_data.url),
            active=object_data.active,
        )
        self.session.add(db_object)
        await self.session.commit()
        await self.session.refresh(db_object)
        return db_object

    async def update_object(
        self, object_id: int, object_data: ProjectUpdate
    ) -> Project:
        if not object_data.url:
            raise HTTPException(status_code=400, detail="Invalid URL provided")

        db_object = await self.session.get(Project, object_id)

        if not db_object:
            raise HTTPException(status_code=404, detail="Project not found")

        db_object.name = object_data.name
        db_object.url = str(object_data.url)
        db_object.active = object_data.active
        db_object.updated = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(db_object)
        return db_object

    async def delete_object(self, object_id: int) -> dict[str, str]:
        db_object = await self.session.get(Project, object_id)
        if not db_object:
            raise HTTPException(status_code=404, detail="Project not found")

        await self.session.delete(db_object)
        await self.session.commit()
        return {"message": f"Project `{object_id}` was deleted"}
