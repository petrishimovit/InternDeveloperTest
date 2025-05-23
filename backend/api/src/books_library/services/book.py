
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import BookRepository
from schemas.book import BookCreate, BookUpdate
from models.book import Book

class BookService:

    def __init__(self, session: AsyncSession):
        self.repo = BookRepository(session)

    async def get_all(self) -> List[Book]:

        return await self.repo.get_all()
    

    async def get_by_id(self, book_id: int) -> Book | None:

        return await self.repo.get_by_id(book_id)


    async def create(self, book_in: BookCreate) -> Book:
        
        return await self.repo.create(book_in)

    async def update(self, book_id: int, book_in: BookUpdate) -> Book | None:

        return await self.repo.update(book_id, book_in)

    async def delete(self, book_id: int) -> bool:

        return await self.repo.delete(book_id)

    async def get_books_by_owner(self, reader_id: int) -> List[Book]:

        return await self.repo.get_books_by_owner(reader_id)

    async def assign_to_reader(self, book_id: int, reader_id: int) -> bool:

        return await self.repo.give_book_to_reader(reader_id, book_id)

    async def unassign_from_reader(self, book_id: int) -> bool:

        return await self.repo.take_book_from_reader(book_id)