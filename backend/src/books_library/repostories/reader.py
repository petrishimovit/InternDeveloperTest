from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Reader, Book
from schemas.reader import ReaderCreate, ReaderUpdate
from typing import List, Optional


class ReaderRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Reader]:
        result = await self.session.execute(select(Reader))
        return result.scalars().all()

    async def get_by_id(self, reader_id: int) -> Optional[Reader]:
        result = await self.session.execute(select(Reader).where(Reader.id == reader_id))
        return result.scalar_one_or_none()

    async def create(self, reader_data: ReaderCreate) -> Reader:
        reader = Reader(**reader_data.model_dump())
        self.session.add(reader)
        await self.session.commit()
        await self.session.refresh(reader)
        return reader

    async def update(self, reader_id: int, reader_data: ReaderUpdate) -> Optional[Reader]:
        reader = await self.get_by_id(reader_id)
        if not reader:
            return None
        for field, value in reader_data.model_dump(exclude_unset=True).items():
            setattr(reader, field, value)
        await self.session.commit()
        await self.session.refresh(reader)
        return reader

    async def delete(self, reader_id: int) -> bool:
        reader = await self.get_by_id(reader_id)

        if not reader:
            return False
        
        await self.session.delete(reader)

        await self.session.commit()
        return True
    
    async def give_book_to_reader(self, reader_id: int, book_id: int) -> bool:
        reader = await self.reader_repo.get_by_id(reader_id)
        if not reader:
            raise ValueError("Reader not found")

        # Получаем количество книг у читателя
        books = await self.book_repo.get_books_by_owner(reader_id)
        if len(books) >= 3:
            raise ValueError("Reader cannot have more than 3 books")

        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        if book.owner_id is not None:
            raise ValueError("Book already assigned")

        return await self.reader_repo.give_book_to_reader(reader_id, book_id)

    async def take_book_from_reader(self, book_id: int) -> bool:
        result = await self.session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book or book.owner_id is None:
            return False  

       
        book.owner_id = None
        await self.session.commit()
        return True