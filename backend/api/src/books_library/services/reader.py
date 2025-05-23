from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from books_library.repositories import (ReaderRepository , BookRepository)
from books_library.schemas.reader import ReaderCreate, ReaderUpdate
from books_library.models.reader import Reader


class ReaderService:

    def __init__(self, session: AsyncSession):

        self.reader_repo = ReaderRepository(session)

        self.book_repo = BookRepository(session)

    async def get_all(self) -> List[Reader]:

        return await self.reader_repo.get_all()
    

    async def get_by_id(self, reader_id: int) -> Reader | None:

        return await self.reader_repo.get_by_id(reader_id)

    async def create(self, reader_in: ReaderCreate) -> Reader:


        return await self.reader_repo.create(reader_in)

    async def update(self, reader_id: int, reader_in: ReaderUpdate) -> Reader | None:


        return await self.reader_repo.update(reader_id, reader_in)

    async def delete(self, reader_id: int) -> bool:


        return await self.reader_repo.delete(reader_id)

    async def give_book(self, reader_id: int, book_id: int) -> bool:

        
        books = await self.book_repo.get_books_by_owner(reader_id)
        
        if len(books) >= 3:
            raise HTTPException(400, "У читателя максимальное кол-во книг")

    
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise HTTPException(404, "Не найдена")

        if book.owner_id:
            raise HTTPException(400, "Книга занята")

        return await self.reader_repo.give_book_to_reader(reader_id, book_id)

    async def take_book(self, book_id: int) -> bool:

        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise HTTPException(404, "Не найдена")
        
        if not book.owner_id:
            raise HTTPException(400, "Книга уже свободна.")

        return await self.reader_repo.take_book_from_reader(book_id)