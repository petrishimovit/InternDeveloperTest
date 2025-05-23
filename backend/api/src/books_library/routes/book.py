from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database.db import create_session
from services.reader_service import ReaderService
from schemas.reader import ReaderCreate, ReaderUpdate, ReaderOut

router = APIRouter(prefix="/readers", tags=["Читатели"])


@router.post("/", response_model=ReaderOut, status_code=201, summary="Создать читателя")
async def create_reader(reader_in: ReaderCreate, session: AsyncSession = Depends(get_async_session)):
    service = ReaderService(session)
    return await service.create(reader_in)


@router.get("/", response_model=List[ReaderOut], summary="Получить список читателей")
async def list_readers(session: AsyncSession = Depends(get_async_session)):
    service = ReaderService(session)
    return await service.get_all()


@router.get("/{reader_id}", response_model=ReaderOut, summary="Получить читателя по ID")
async def get_reader(reader_id: int, session: AsyncSession = Depends(get_async_session)):
    service = ReaderService(session)
    reader = await service.get_by_id(reader_id)
    if not reader:
        raise HTTPException(404, detail="Читатель не найден")
    return reader


@router.put("/{reader_id}", response_model=ReaderOut, summary="Обновить данные читателя")
async def update_reader(reader_id: int, reader_in: ReaderUpdate, session: AsyncSession = Depends(get_async_session)):
    service = ReaderService(session)
    reader = await service.update(reader_id, reader_in)
    if not reader:
        raise HTTPException(404, detail="Читатель не найден")
    return reader


@router.delete("/{reader_id}", status_code=204, summary="Удалить читателя")
async def delete_reader(reader_id: int, session: AsyncSession = Depends(get_async_session)):
    service = ReaderService(session)
    success = await service.delete(reader_id)
    if not success:
        raise HTTPException(404, detail="Читатель не найден")