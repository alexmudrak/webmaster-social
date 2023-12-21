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
        objects = result.unique().all()
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
            parse_material_id_element=(object_data.parse_material_id_element),
            parse_material_body_element=(
                object_data.parse_material_body_element
            ),
            parse_material_img_element=(
                object_data.parse_material_img_element
            ),
            parse_material_url_element=(
                object_data.parse_material_url_element
            ),
            active=object_data.active,
            updated=datetime.utcnow(),
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

        if object_data.parse_material_id_element:
            db_object.parse_material_id_element = (
                object_data.parse_material_id_element
            )
        if object_data.parse_material_body_element:
            db_object.parse_material_body_element = (
                object_data.parse_material_body_element
            )

        if object_data.parse_material_img_element:
            db_object.parse_material_img_element = (
                object_data.parse_material_img_element
            )

        if object_data.parse_material_url_element:
            db_object.parse_material_url_element = (
                object_data.parse_material_url_element
            )

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
