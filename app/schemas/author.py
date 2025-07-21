from sqlmodel import SQLModel
from typing import Optional, List
from datetime import date

class AuthorBase(SQLModel):
    name: str
    birthday: date
    nationality: str
    
class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    name: Optional[str] = None
    birthday: Optional[date] = None
    nationality: Optional[str] = None

class AuthorRead(AuthorBase):
    id: int
    
class Book(SQLModel):
    id: int
    title: str
    isbn: str
    
class AuthorWithBook(SQLModel):
    name: str
    books: List[Book]= []