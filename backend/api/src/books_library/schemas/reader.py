from pydantic import BaseModel 
from typing import Optional

class ReaderCreate(BaseModel):
    name: str
    email: str

class ReaderUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]

class ReaderRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

