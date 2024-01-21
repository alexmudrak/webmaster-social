from datetime import datetime

from fastapi import HTTPException
from models.setting import Setting
from schemas.setting_schema import SettingCreate, SettingRead, SettingUpdate
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class SettingController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_objects(self) -> list[SettingRead]:
        query = select(Setting)
        result = await self.session.exec(query)
        db_objects = result.unique().all()
        settings_with_project_name = [
            SettingRead(
                **setting.model_dump(),
                project_name=setting.project.name if setting.project else None,
            )
            for setting in db_objects
        ]
        return settings_with_project_name

    async def get_object(self, object_id: int) -> Setting:
        db_object = await self.session.get(Setting, object_id)
        if not db_object:
            raise HTTPException(status_code=404, detail="Setting not found")
        return db_object

    async def create_object(self, object_data: SettingCreate) -> Setting:
        existing_object = await self.session.exec(
            select(Setting).where(
                (Setting.name == object_data.name)
                & (Setting.project_id == object_data.project_id)
            )
        )
        existing_object = existing_object.unique().one_or_none()

        if existing_object:
            raise HTTPException(
                status_code=409,
                detail=(
                    "A object with the same name and "
                    "project ID combination already exists."
                ),
            )

        # TODO: Add config validation
        db_object = Setting(
            name=object_data.name,
            settings=object_data.settings,
            project_id=object_data.project_id,
            active=object_data.active,
        )
        self.session.add(db_object)
        await self.session.commit()
        await self.session.refresh(db_object)
        return db_object

    async def update_object(
        self, object_id: int, object_data: SettingUpdate
    ) -> Setting:
        db_object = await self.session.get(Setting, object_id)

        if not db_object:
            raise HTTPException(status_code=404, detail="Setting not found")
        # TODO: Add config validation
        # TODO: Add condition to check value

        db_object.name = object_data.name
        db_object.settings = object_data.settings
        db_object.project_id = object_data.project_id
        db_object.active = object_data.active
        db_object.updated = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(db_object)
        return db_object

    async def delete_object(self, object_id: int):
        db_object = await self.session.get(Setting, object_id)
        if not db_object:
            raise HTTPException(status_code=404, detail="Setting not found")

        await self.session.delete(db_object)
        await self.session.commit()
        return {"message": f"Setting `{object_id}` was deleted"}
