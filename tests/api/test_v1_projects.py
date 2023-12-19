import pytest
from core.database import get_session
from httpx import AsyncClient
from main import app
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = (
    "postgresql+asyncpg://wmhelper:wmhelperdbpass@localhost/wmsocial_test"
)


async def session_test():
    engine = AsyncEngine(
        create_engine(
            DATABASE_URL,
            echo=True,
            future=True,
        )
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest.fixture()
async def client_fixture():
    app.dependency_overrides[get_session] = session_test

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_all_projects(client_fixture):
    payload = {"name": "mock", "url": "https://example.com", "active": True}
    client = await client_fixture.__anext__()
    response = await client.post("/projects/", json=payload)

    response = await client.get("/projects/")
    assert response.status_code == 200
    assert len(response.json()) == 1
