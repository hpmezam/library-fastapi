from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_db
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.crud.book import create_book, get_all_books, get_book, update_book, delete_book

book_router = APIRouter(prefix="/books", tags=["Books"])

@book_router.post("/", response_model=BookRead)
def create(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)

@book_router.get("/", response_model=list[BookRead])
def list_all(db: Session = Depends(get_db)):
    return get_all_books(db)

@book_router.get("/{id}", response_model=BookRead)
def get(id: int, db: Session = Depends(get_db)):
    return get_book(db, id)

@book_router.put("/{id}", response_model=BookRead)
def update(id: int, book: BookUpdate, db: Session = Depends(get_db)):
    return update_book(db, id, book)

@book_router.delete("/{id}", response_model=dict)
def delete(id: int, db: Session = Depends(get_db)):
    return delete_book(db, id)