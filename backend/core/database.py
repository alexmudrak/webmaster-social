from core.settings import Settings
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlmodel import SQLModel, and_, create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession

engine = AsyncEngine(
    create_engine(
        Settings().DB_URL,
        echo=True,
        future=True,
    )
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with async_session() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_or_create(session: AsyncSession, model, **kwargs):
    instance = await session.exec(
        select(model).where(
            and_(
                *(
                    getattr(model, key) == value
                    for key, value in kwargs.items()
                )
            )
        )
    )
    instance = instance.unique().first()

    if instance:
        return instance
    else:
        new_instance = model(**kwargs)
        session.add(new_instance)
        await session.commit()
        return new_instance
