from schemas.setting_schema import (
    SettingCreate,
    SettingRead,
    SettingReadWithProject,
    SettingUpdate,
)
from sqlmodel.ext.asyncio.session import AsyncSession


class SettingController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_objects(self) -> list[SettingRead]:
        pass

    async def get_object(self, object_id: int) -> SettingReadWithProject:
        pass

    async def create_object(self, object_data: SettingCreate) -> SettingRead:
        pass

    async def update_object(
        self, object_id: int, object_data: SettingUpdate
    ) -> SettingRead:
        pass

    async def delete_object(self, object_id: int):
        pass
