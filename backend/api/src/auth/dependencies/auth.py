from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from auth.config.config import authx_cfg
from auth.repositories import UserRepository
from database.db import create_session
from authx import RequestToken
import traceback

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(create_session)
):
    try:
        
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Invalid or missing token")
        token = RequestToken(token=token,location="cookies")
        payload = authx_cfg.verify_token(token=token,verify_csrf=False)
        
        email = payload.sub
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token: sub missing")
        user_repo = UserRepository(db)
        user = await user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=401, detail=f"Unauthorized: {str(e)}")
