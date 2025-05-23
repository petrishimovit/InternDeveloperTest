from fastapi import APIRouter
from books_library.routes import router as libraryrouter

router = APIRouter()

router.include_router(libraryrouter)