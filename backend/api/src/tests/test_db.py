from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # tests/
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'test_db.sqlite')}"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_test_session() -> AsyncSession:

    async with async_session() as session:
        yield session