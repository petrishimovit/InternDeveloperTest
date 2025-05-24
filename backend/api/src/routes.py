from fastapi import APIRouter
from books_library.routes import router as libraryrouter
from auth.routes import router as authrouter

router = APIRouter()

router.include_router(libraryrouter)


router.include_router(authrouter)