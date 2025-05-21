from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from models import Book
from schemas.book import BookCreate, BookUpdate
from typing import List, Optional


class BookRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Book]:

        result = await self.session.execute(select(Book))

        return result.scalars().all()

    async def get_by_id(self, book_id: int) -> Optional[Book]:

        result = await self.session.execute(select(Book).where(Book.id == book_id))

        return result.scalar_one_or_none()

    async def get_by_isbn(self, isbn: str) -> Optional[Book]:

        result = await self.session.execute(select(Book).where(Book.isbn == isbn))

        return result.scalar_one_or_none()

    async def create(self, book_data: BookCreate) -> Book:

        book = Book(**book_data.model_dump())

        self.session.add(book)

        await self.session.commit()

        await self.session.refresh(book)

        return book

    async def update(self, book_id: int, book_data: BookUpdate) -> Optional[Book]:

        book = await self.get_by_id(book_id)

        if not book:
            return None
        
        for field, value in book_data.model_dump(exclude_unset=True).items():

            setattr(book, field, value)

        await self.session.commit()

        await self.session.refresh(book)

        return book

    async def delete(self, book_id: int) -> bool:

        book = await self.get_by_id(book_id)

        if not book:

            return False
        
        await self.session.delete(book)

        await self.session.commit()
        
        return True

    
    



