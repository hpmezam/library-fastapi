from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate

def create_author(db: Session, author: AuthorCreate) -> AuthorRead:
    existing = db.exec(select(Author).where(Author.name == author.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"The author with name '{author.name}' already exists")
    new_author = Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

def get_all_authors(db: Session) -> list[AuthorRead]:
    return  db.exec(select(Author)).all()

def get_author(db: Session, id: int) -> AuthorRead:
    # 1. Get existing object
    author = db.get(Author, id)
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with id {id} not found")
    return author

def update_author(db: Session, id: int, author: AuthorUpdate) -> AuthorRead:
    # 1. Get existing object
    existing = db.get(Author, id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Author with id {id} not found")

    # 2. Get only fields that were provided
    author_data = author.model_dump(exclude_unset=True)

    # 3. Check if a different product already has the same name
    if "name" in author_data:
        duplicate = db.exec(
            select(Author)
            .where(Author.name == author_data["name"])
            .where(Author.id != id)
        ).first()
        if duplicate:
            raise HTTPException(
                status_code=400,
                detail=f"Another author with name '{author_data['name']}' already exists"
            )

    # 4. Check if the new values differ from the current ones
    no_changes = all(
        getattr(existing, field) == value
        for field, value in author_data.items()
    )
    if no_changes:
        raise HTTPException(
            status_code=400,
            detail="No changes detected"
        )

    # 5. Apply updates
    for key, value in author_data.items():
        setattr(existing, key, value)

    db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing

def delete_author(db: Session, id: int) -> dict:
    author = db.get(Author, id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {id} not found"
        )

    name = author.name
    db.delete(author)
    db.commit()
    return {"message": f"The author '{name}' was successfully deleted"}