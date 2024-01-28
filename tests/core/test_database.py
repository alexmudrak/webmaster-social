import pytest
from core.database import get_or_create
from models.setting import Setting as ExampleModel
from sqlalchemy.ext.asyncio import AsyncSession as AsyncSessionType
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel import SQLModel


@pytest.mark.asyncio
async def test_init_db(async_db_engine: AsyncEngine):
    async with async_db_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.mark.asyncio
async def test_get_session_context(async_db):
    async with async_db as session:
        assert isinstance(session, AsyncSessionType)


@pytest.mark.asyncio
async def test_get_or_create(async_db):
    async with async_db as session:
        instance = await get_or_create(session, ExampleModel, name="test")
        assert isinstance(instance, ExampleModel)
        assert instance.name == "test"

        same_instance = await get_or_create(session, ExampleModel, name="test")
        assert same_instance is instance
