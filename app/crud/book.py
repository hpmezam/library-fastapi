from sqlmodel import Session, select
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.models.author import Author
from app.models.book import Book
from fastapi import HTTPException

def create_book(db: Session, book: BookCreate) -> BookRead:
    author = db.get(Author, book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with id {book.author_id} not found")
    
    existing = db.exec(
        select(Book).where(Book.isbn == book.isbn)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail=f"Book with ISBN '{book.isbn}' already exists")
    
    new_book = Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
    
def get_all_books(db: Session) -> list[BookRead]:
    return db.exec(select(Book)).all()

def get_book(db: Session, id: int) -> BookRead:
    book = db.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
    return book

def update_book(db: Session, id: int, book: BookUpdate) -> BookRead:
    existing = db.get(Book, id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
    
    book_data = book.model_dump(exclude_unset=True)
    
    if "author_id" in book_data:
        author = db.get(Author, book_data["author_id"])
        if not author:
            raise HTTPException(status_code=404, detail=f"Author with id {book_data['author_id']} not found")
        
    if "isbn" in book_data:
        duplicate = db.exec(
            select(Book).where(Book.isbn == book_data.get('isbn', existing.isbn)).where(Book.id != id)
        ).first()
        if duplicate:
            raise HTTPException(status_code=400, detail=f"Book with ISBN '{book_data['isbn']}' already exists")
    
    no_changes = all(
        getattr(existing, field) == value 
        for field, value in book_data.items()
    )
    
    if no_changes:
        raise HTTPException(status_code=400, detail="No changes detected")
    
    for field, value in book_data.items():
        setattr(existing, field, value)
        
    db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing

def delete_book(db: Session, id: int) -> dict:
    book = db.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
    
    title = book.title
    db.delete(book)
    db.commit()
    return {"message": f"The book '{title}' was successfully deleted"}
        
        