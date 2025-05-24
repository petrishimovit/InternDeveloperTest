from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from auth.repositories.user import UserRepository
from auth.schemas.user import UserCreate, UserOut
from auth.config.config import authx_cfg
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register(self, user: UserCreate) -> UserOut:
        if await self.user_repo.get_user_by_email(user.email):
            raise HTTPException(400, detail="Email already registered")
        return await self.user_repo.create_user(user)

    async def login(self, email: str, password: str) -> dict:
        db_user = await self.user_repo.get_user_by_email(email)
        if not db_user or not pwd_context.verify(password, db_user.password):
            raise HTTPException(401, detail="Invalid credentials")
        token = authx_cfg.create_access_token(uid=email)  # Используй authx_cfg
        print(f"Generated token: {token}")  # Отладка
        return {"access_token": token, "token_type": "bearer"}
