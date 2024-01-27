from models.setting import Setting
from sqlmodel import select


class SettingsRepository:
    def __init__(self, session):
        self.session = session

    async def retrieve_settings_by_project_id(
        self, project_id
    ) -> list[Setting]:
        query = select(Setting).where(
            Setting.project_id == project_id,
        )
        result = await self.session.exec(query)
        objects = result.unique().all()

        return list(objects)

    async def retrieve_setting_by_project_id_and_network_name(
        self,
        project_id: int,
        network_name: str,
    ) -> Setting:
        query = select(Setting).where(
            Setting.project_id == project_id,
            Setting.name == network_name,
        )
        result = await self.session.exec(query)
        object = result.unique().first()

        return object

    async def retrieve_unique_settings(self) -> list[str]:
        query = select(Setting.name)
        result = await self.session.exec(query)
        objects = result.unique().all()

        return objects
