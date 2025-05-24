from fastapi import APIRouter, Depends, HTTPException, status, Response , Request
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from books_library.schemas.reader import ReaderCreate, ReaderRead, ReaderUpdate
from books_library.repositories.reader import ReaderRepository
from database.db import create_session
from auth.dependencies.auth import get_current_user
from auth.models.user import User
from auth.config.config import authx_cfg

router = APIRouter(prefix="/readers", tags=["readers"])

@router.get("/", response_model=List[ReaderRead])
async def get_readers(request: Request, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    repo = ReaderRepository(session)
    readers = await repo.get_all()
    return readers

@router.get("/{reader_id}", response_model=ReaderRead)
async def get_reader(request: Request, reader_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    repo = ReaderRepository(session)
    reader = await repo.get_by_id(reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

@router.post("/", response_model=ReaderRead, status_code=status.HTTP_201_CREATED)
async def create_reader(request: Request, reader_data: ReaderCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    repo = ReaderRepository(session)
    reader = await repo.create(reader_data)
    return reader

@router.put("/{reader_id}", response_model=ReaderRead)
async def update_reader(request: Request, reader_id: int, reader_data: ReaderUpdate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    repo = ReaderRepository(session)
    reader = await repo.update(reader_id, reader_data)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

@router.delete("/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reader(request: Request, reader_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    repo = ReaderRepository(session)
    success = await repo.delete(reader_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reader not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)