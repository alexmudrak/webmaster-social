from sqlmodel.ext.asyncio.session import AsyncSession


class SocialNetworksController:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def send_article(self, project_id: int):
        # TODO: Add documentation

        # TODO: Get older article which not send to
        #       social
        # TODO: Get social network settings which linked
        #       to project
        # TODO: Prepare article for publishing
        # TODO: Send article to available social networks
        # TODO: Save SendingModel result to DB
        pass
