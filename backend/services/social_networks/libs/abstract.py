from abc import ABC, abstractmethod

from httpx import AsyncClient
from models.article import Article
from models.setting import Setting
from sqlmodel.ext.asyncio.session import AsyncSession


class SocialNetworkAbstract(ABC):
    def __init__(
        self,
        session: AsyncSession,
        client: AsyncClient,
        config: Setting,
        article: Article,
    ):
        self.session = session
        self.client = client
        self.config = config
        self.article = article

    # TODO: Need to refactor and merge to `get_config`
    # TODO: Change to self method
    @staticmethod
    @abstractmethod
    async def config_validation():
        raise NotImplementedError

    @abstractmethod
    async def auth(self):
        raise NotImplementedError

    @abstractmethod
    async def get_config(self):
        raise NotImplementedError

    @abstractmethod
    async def post(self):
        raise NotImplementedError

    @abstractmethod
    async def prepare_post(self):
        raise NotImplementedError
