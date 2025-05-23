from fastapi import APIRouter
from .book import router as bookrouter
from .reader import router as readerrouter

router = APIRouter()

router.include_router(bookrouter)

router.include_router(readerrouter)