from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from books_library.models import Reader
from books_library.schemas.reader import ReaderCreate, ReaderUpdate


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
