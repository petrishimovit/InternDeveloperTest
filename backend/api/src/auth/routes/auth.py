from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from auth.schemas.user import UserCreate, UserOut
from auth.services.user import UserService
from auth.config.config import authx_cfg
from database.db import create_session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(create_session)):
    user_service = UserService(db)
    return await user_service.register(user)

@router.post("/login")
async def login(user: UserCreate, response: Response, db: AsyncSession = Depends(create_session)):
    user_service = UserService(db)
    result = await user_service.login(user.email, user.password)
    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=False,  # Только HTTPS
        samesite="lax",
        max_age=3600
    )

    
    return {"message": "Login successful"}