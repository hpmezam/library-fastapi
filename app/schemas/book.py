from sqlmodel import SQLModel
from typing import Optional
from pydantic import field_validator
from datetime import date

class BookBase(SQLModel):
    title: str
    isbn: str

class BookCreate(BookBase):
    author_id: int

class BookUpdate(SQLModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    author_id: Optional[int] = None

class AuthorRead(SQLModel):
    name: str
    
class BookRead(BookBase):
    id: int
    author_id: int
    author: Optional[AuthorRead]