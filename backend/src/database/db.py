from hikvision_cameras.models import *
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker
from database.base import Base
from src.config import config



DATABASE_URL = f"postgresql+asyncpg://{config.DB_LOGIN}:{config.DB_PASSWORD}@{config.DB_URL}/{config.DB_NAME}"







engine = create_async_engine(DATABASE_URL, echo=True)

sessionmaker = async_sessionmaker(engine , expire_on_commit=False)

async def create_session():
    """
    Dependency that provides an async database session.
    """
    async with sessionmaker() as session:
        yield session


# инициализация бд

async def init_db():

    async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    


# удаление бд
async def delete_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



