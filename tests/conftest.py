import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from core.database import get_session
from httpx import AsyncClient
from main import app
from models.project import Project
from models.setting import Setting
from sqlalchemy import text
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_PORT = os.getenv("TEST_DB_PORT")
TEST_DB_NAME = os.getenv("TEST_DB_NAME")
TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")

DATABASE_URL = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"

engine = AsyncEngine(
    create_engine(
        DATABASE_URL,
        echo=True,
        future=True,
    )
)


@pytest_asyncio.fixture(scope="function")
async def async_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_db(
    async_db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()

        for table in reversed(SQLModel.metadata.sorted_tables):
            await session.exec(text(f"TRUNCATE {table.name} CASCADE;"))
            await session.commit()


@pytest.fixture(scope="session")
def event_loop():
    import asyncio

    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_client(async_db: AsyncSession) -> AsyncClient:
    async def override_get_session():
        return async_db

    app.dependency_overrides[get_session] = override_get_session

    return AsyncClient(app=app, base_url="http://localhost")


@pytest.fixture()
async def exist_project(async_db: AsyncSession) -> Project:
    db_object = Project(
        name="test",
        url="https://test.com",
        active=True,
    )
    db = async_db
    db.add(db_object)
    await db.commit()
    await db.refresh(db_object)
    return db_object


@pytest.fixture()
async def exist_setting_with_project(
    async_db: AsyncSession, exist_project: Project
) -> Setting:
    project = await exist_project

    db_object = Setting(
        name="test setting",
        project_id=project.id,
        settings={"prop 1": 1, "prop 2": 2},
        active=True,
    )
    db = async_db
    db.add(db_object)
    await db.commit()
    await db.refresh(db_object)
    return db_object


@pytest.fixture()
async def exist_setting_without_project(async_db: AsyncSession) -> Setting:
    db_object = Setting(
        name="test setting",
        settings={"prop 1": 1, "prop 2": 2},
        active=True,
    )
    db = async_db
    db.add(db_object)
    await db.commit()
    await db.refresh(db_object)
    return db_object
