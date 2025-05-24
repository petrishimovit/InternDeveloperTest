# auth/services/user.py
from sqlalchemy.orm import Session
from auth.repositories import UserRepository
from auth.schemas.user import UserCreate, UserOut
from auth.config import authx
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    def __init__(self, db: Session):

        self.user_repo = UserRepository(db)

    def register(self, user: UserCreate) -> UserOut:

        if self.user_repo.get_user_by_email(user.email):

            raise HTTPException(400, detail="Email already registered")
        
        return self.user_repo.create_user(user)

    def login(self, email: str, password: str) -> dict:

        db_user = self.user_repo.get_user_by_email(email)

        if not db_user or not pwd_context.verify(password, db_user.password):

            raise HTTPException(401, detail="Invalid credentials")
        
        token = authx.create_access_token(uid=email)
        return {"access_token": token, "token_type": "bearer"}