# auth/routes/auth.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.schemas.user import UserCreate, UserOut
from auth.services import UserService
from database.db import create_session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(create_session)):

    user_service = UserService(db)

    return user_service.register(user)

@router.post("/login")

def login(user: UserCreate, db: Session = Depends(create_session)):

    user_service = UserService(db)

    return user_service.login(user.email, user.password)