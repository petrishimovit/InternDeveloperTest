from books_library.repositories.book import BookRepository
from books_library.repositories.reader import ReaderRepository
from books_library.models import Book
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = BookRepository(session)
        self.reader_repo = ReaderRepository(session)

    async def give_to_reader(self, book_id: int, reader_id: int) -> Book:
        book = await self.repo.get_by_id(book_id)
        if not book:
            raise ValueError("Книга не найдена")
        if book.reader_id is not None:
            raise ValueError("Книга уже выдана")

        reader = await self.reader_repo.get_by_id(reader_id)
        if not reader:
            raise ValueError("Читатель не найден")

        result = await self.session.execute(select(Book).where(Book.reader_id == reader_id))
        books = result.scalars().all()
        if len(books) >= 3:
            raise ValueError("Читателю уже выдано 3 книги")

        book.reader_id = reader_id
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def return_from_reader(self, book_id: int) -> Book:
        book = await self.repo.get_by_id(book_id)
        if not book:
            raise ValueError("Книга не найдена")
        if book.reader_id is None:
            raise ValueError("Книга не привязана к читателю")

        book.reader_id = None
        await self.session.commit()
        await self.session.refresh(book)
        return book
