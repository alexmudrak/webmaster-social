import asyncio

from sqlmodel.ext.asyncio.session import AsyncSession


class ParserController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def collect_data(self, project_id: int):
        # Get project by id
        # Get parse type
        # Get parse url
        # Get parse config
        # Run correct parse type
        # Run parser for collect
        await asyncio.sleep(2)
        print(f"Task done - {project_id}")
