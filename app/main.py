from fastapi import FastAPI
from app.routers.author import author_router
from app.routers.book import book_router

app = FastAPI(title='LIBRARY API')

app.include_router(author_router)
app.include_router(book_router)