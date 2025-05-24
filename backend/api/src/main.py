from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db import init_db , delete_db
from books_library import models
from routes import router
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    logger.info("Starting database initialization")
    await delete_db()
    await init_db()
    logger.info("Database initialization completed")
    yield
   
    logger.info("Shutting down, dropping tables (optional)")
    

app = FastAPI(lifespan=lifespan)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    