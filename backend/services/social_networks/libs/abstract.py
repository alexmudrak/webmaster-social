from abc import ABC, abstractmethod

from httpx import AsyncClient
from models.article import Article
from sqlmodel.ext.asyncio.session import AsyncSession


class SocialNetworkAbstract(ABC):
    def __init__(
        self,
        session: AsyncSession,
        client: AsyncClient,
    ):
        self.session = session
        self.client = client

    @abstractmethod
    async def auth(self):
        raise NotImplementedError

    @abstractmethod
    async def get_config(self):
        raise NotImplementedError

    @abstractmethod
    async def post(self, article: Article):
        raise NotImplementedError

    @abstractmethod
    async def prepare_post(self):
        raise NotImplementedError
