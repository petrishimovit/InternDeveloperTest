
import pytest
from httpx import AsyncClient
from fastapi import status 
from auth.services.user import UserService
from auth.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient, db_session: AsyncSession):
    
    user_data = UserCreate(email="test@example.com", password="password")
    user_service = UserService(db_session)
    await user_service.register(user_data)

    
    response = await async_client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Login successful"}
    assert "access_token" in response.cookies
    