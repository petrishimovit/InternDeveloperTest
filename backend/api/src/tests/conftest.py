# src/tests/conftest.py
import sys
import os
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import importlib.util

# Корректируем sys.path для импорта из src/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # src/tests/
SRC_DIR = os.path.dirname(BASE_DIR)  # src/
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Явный импорт main.py
spec = importlib.util.spec_from_file_location("main", os.path.join(SRC_DIR, "main.py"))
main = importlib.util.module_from_spec(spec)
sys.modules["main"] = main
spec.loader.exec_module(main)

from tests.test_db import engine, create_test_session
from auth.models.user import User
from books_library.models.book import Book
from books_library.models.reader import Reader

app = main.app  # Доступ к атрибуту app

@pytest.fixture(scope="session")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Book.metadata.create_all)
        await conn.run_sync(Reader.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)
        await conn.run_sync(Book.metadata.drop_all)
        await conn.run_sync(Reader.metadata.drop_all)

@pytest.fixture
async def db_session():
    async with create_test_session() as session:
        async with session.begin():
            yield session
        await session.rollback()

@pytest.fixture
def client(init_db):
    return TestClient(app)

@pytest.fixture
async def async_client(init_db):
    return AsyncClient(app=app, base_url="http://test")