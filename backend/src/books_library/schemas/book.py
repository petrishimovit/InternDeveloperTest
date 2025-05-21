from pydantic import BaseModel, Field
from typing import Optional

class BookCreate(BaseModel):
    name: str
    author: str
    publication_year: Optional[int] = None
    isbn: Optional[str] = None
    copies: int = Field(default=1, ge=0)

class BookUpdate(BaseModel):
    name: Optional[str]
    author: Optional[str]
    publication_year: Optional[int]
    isbn: Optional[str]
    copies: Optional[int] = Field(default=None, ge=0)

class BookRead(BaseModel):
    id: int
    name: str
    author: str
    publication_year: Optional[int]
    isbn: Optional[str]
    copies: int

    class Config:
        orm_mode = True
