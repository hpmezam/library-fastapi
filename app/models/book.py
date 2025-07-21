from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.author import Author
    
class Book(SQLModel, table=True):
    id: Optional[int] =  Field(default=None, primary_key=True)
    title: str 
    isbn: str = Field(index=True)
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")

    # Many-to-one relationship with author
    author: Optional['Author'] = Relationship(back_populates="books")