from fastapi import Depends, HTTPException
from authx import RequestToken
from sqlalchemy.orm import Session
from auth.config import authx
from auth.repositories import UserRepository
from database.db import create_session


def get_current_user(token: RequestToken = Depends(authx.get_token_from_request), db: Session = Depends(create_session)):
    try:
        payload = authx.verify_token(token=token)
        email = payload.get("uid")
        if not email:
            raise HTTPException(401, detail="Invalid token")
        user_repo = UserRepository(db)
        user = user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(401, detail="Unauthorized")