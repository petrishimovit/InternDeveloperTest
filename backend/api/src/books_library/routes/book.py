from fastapi import APIRouter, Depends, HTTPException, status , Request
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from books_library.schemas.book import BookCreate, BookRead, BookUpdate
from books_library.services.book import BookService
from database.db import create_session
from auth.dependencies.auth import get_current_user
from auth.models.user import User
from auth.config.config import authx_cfg

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookRead])
async def get_books(request: Request, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    service = BookService(session)
    books = await service.repo.get_all()
    return books

@router.get("/{book_id}", response_model=BookRead)
async def get_book(request: Request, book_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    service = BookService(session)
    book = await service.repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(request: Request, book_data: BookCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    service = BookService(session)
    book = await service.repo.create(book_data)
    return book

@router.put("/{book_id}", response_model=BookRead)
async def update_book(request: Request, book_id: int, book_data: BookUpdate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    service = BookService(session)
    book = await service.repo.update(book_id, book_data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(request: Request, book_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    service = BookService(session)
    success = await service.repo.delete(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return

@router.post("/{book_id}/give/{reader_id}", response_model=BookRead)
async def give_book(request: Request, book_id: int, reader_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    service = BookService(session)
    try:
        book = await service.give_to_reader(book_id, reader_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return book

@router.post("/{book_id}/return", response_model=BookRead)
async def return_book(request: Request, book_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(create_session)):
    service = BookService(session)
    try:
        book = await service.return_from_reader(book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return book