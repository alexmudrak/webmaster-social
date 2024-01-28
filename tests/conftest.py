import os
from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from core.database import AsyncSession, get_session
from httpx import AsyncClient
from main import app
from models.article import Article
from models.project import Project
from models.setting import Setting
from sqlalchemy import text
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlmodel import SQLModel, create_engine

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


@pytest.fixture
def mock_article():
    return MagicMock(
        spec=Article,
        title="Test Article",
        body=(
            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean"
            "commodo ligula eget dolor. Aenean massa. Cum sociis natoque"
            "penatibus et magnis dis parturient montes, nascetur ridiculus."
            " Donec quam felis, ultricies nec, pellentesque eu, pretium quis,"
            "sem. Nulla consequat massa quis enim. Donec pede justo, "
            "vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut"
            "imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede "
            "mollis pretium. Integer tincidunt. Cras dapibus. Vivamus "
            "semper nisi. Aenean vulputate eleifend tellus. Aenean leo, "
            "porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem "
            "ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus "
            "viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean "
            "imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper "
            "ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, "
            "tellus eget condimentum rhoncus, sem quam semper libero, sit "
            "adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, "
            "pulvinar, hendrerit id, lorem. Maecenas nec odio et ante "
            "tincidunt tempus. Donec vitae sapien ut libero venenatis "
            "faucibus. Nullam quis ante. Etiam sit amet orci eget eros "
            "faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet. "
            "Donec sodales sagittis magna. Sed consequat, leo eget bibendum "
            "sodales, augue velit cursus nunc, quis gravida magna mi a. "
            "Fusce vulputate eleifend sapien. Vestibulum purus quam, "
            "scelerisque ut, mollis sed, nonummy id, metus. Nullam accumsan "
            "lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. "
            "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices "
            "posuere cubilia Curae; In ac dui quis mi consectetuer lacinia. "
            "Nam pretium turpis et arcu. Duis arcu tortor, suscipit eget, "
            "imperdiet nec, imperdiet iaculis, ipsum. Sed aliquam ultrices "
            "mauris. Integer "
            "ante arcu, accumsan a, consectetuer eget, posuere ut, mauris. "
            "Praesent adipiscing. Phasellus ullamcorper ipsum rutrum nunc. "
            "Nunc nonummy metus. Vestibulum volutpat pretium libero. Cras id "
            "dui. Aenean ut"
        ),
        url="http://test.com",
        img_url="http://test.com/image.jpg",
    )


@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_client():
    mock = AsyncMock(spec=AsyncClient)
    mock.post = AsyncMock()
    mock.get = AsyncMock()
    return mock


@pytest.fixture
def mock_config(config_settings):
    return MagicMock(
        spec=Setting,
        settings=config_settings,
    )
