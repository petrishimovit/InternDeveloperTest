import pytest
from httpx import AsyncClient
from fastapi import status
from auth.services.user import UserService
from auth.schemas.user import UserCreate
from books_library.schemas.book import BookCreate
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_book(async_client: AsyncClient, db_session: AsyncSession):
    
    user_data = UserCreate(email="test@example.com", password="password")
    user_service = UserService(db_session)
    await user_service.register(user_data)
    login_response = await async_client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password"}
    )
    cookies = login_response.cookies

    
    book_data = BookCreate(title="Test Book", author="Author", year=2023)
    response = await async_client.post(
        "/books/",
        json=book_data.dict(),
        cookies=cookies
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "Test Book"