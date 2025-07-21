from fastapi import APIRouter, Depends, HTTPException
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate, AuthorWithBook
from app.crud.author import create_author, get_all_authors, get_author, update_author, delete_author
from sqlmodel import Session
from typing import List

from app.db.session import get_db 
from app.models.author import Author
from app.crud.author import  Author as author_crud

author_router = APIRouter(prefix="/authors", tags=["Authors"])

@author_router.post("/", response_model=AuthorRead)
def create(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db, author)

@author_router.get("/", response_model=list[AuthorRead])
def list_all(db: Session = Depends(get_db)):
    return get_all_authors(db)

@author_router.get("/{id}", response_model=AuthorRead)
def get_author_info(id: int, db: Session = Depends(get_db)):
    return get_author(db, id)

@author_router.get("/{id}/with-books", response_model=AuthorWithBook)
def get_author_with_books(id: int, db: Session = Depends(get_db)):
    return get_author(db, id)

@author_router.put('/{id}')
def update(id: int, product: AuthorUpdate, db: Session = Depends(get_db)):
    return update_author(db, id, product)

@author_router.delete("/{id}", status_code=200)
def delete(id: int, db: Session = Depends(get_db)):
    return delete_author(db, id)