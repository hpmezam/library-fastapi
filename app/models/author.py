from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from app.models.book import Book

class Author(SQLModel, table=True):
    id: Optional[int] =  Field(default=None, primary_key=True)
    name: str
    birthday: date
    nationality: str
    # One-to-many relationship with the book
    books: List['Book'] = Relationship(back_populates="author")
    
