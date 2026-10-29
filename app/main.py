from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.database import get_session
from app.models import Author, Book
from app.schemas import (
    AuthorCreate,
    AuthorOut,
    AuthorUpdate,
    BookCreate,
    BookOut,
    BookUpdate,
    BookWithAuthor,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Alembic creates and updates tables. Do not use create_all() here.
    yield


app = FastAPI(
    title="PostgreSQL Book Manager API",
    description="A FastAPI CRUD project using PostgreSQL, SQLAlchemy ORM, and Alembic.",
    version="1.0.0",
    lifespan=lifespan,
)


def get_author_or_404(session: Session, author_id: int) -> Author:
    author = session.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def get_book_or_404(session: Session, book_id: int) -> Book:
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/")
def home():
    return {
        "message": "PostgreSQL Book Manager API is running",
        "docs": "/docs",
    }


# Authors CRUD


@app.post("/authors", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author(data: AuthorCreate, session: Session = Depends(get_session)):
    author = Author(name=data.name.strip(), bio=data.bio)
    session.add(author)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="An author with this name already exists")
    session.refresh(author)
    return author


@app.get("/authors", response_model=list[AuthorOut])
def list_authors(session: Session = Depends(get_session)):
    return session.scalars(select(Author).order_by(Author.id)).all()


@app.get("/authors/{author_id}", response_model=AuthorOut)
def get_author(author_id: int, session: Session = Depends(get_session)):
    return get_author_or_404(session, author_id)


@app.put("/authors/{author_id}", response_model=AuthorOut)
def update_author(
    author_id: int,
    data: AuthorUpdate,
    session: Session = Depends(get_session),
):
    author = get_author_or_404(session, author_id)
    author.name = data.name.strip()
    author.bio = data.bio
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="An author with this name already exists")
    session.refresh(author)
    return author


@app.delete("/authors/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, session: Session = Depends(get_session)):
    author = get_author_or_404(session, author_id)
    session.delete(author)
    session.commit()
    return None


# Books CRUD


@app.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(data: BookCreate, session: Session = Depends(get_session)):
    get_author_or_404(session, data.author_id)
    book = Book(
        title=data.title.strip(),
        description=data.description,
        author_id=data.author_id,
    )
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.get("/books", response_model=list[BookOut])
def list_books(session: Session = Depends(get_session)):
    return session.scalars(select(Book).order_by(Book.id)).all()


@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, session: Session = Depends(get_session)):
    return get_book_or_404(session, book_id)


@app.put("/books/{book_id}", response_model=BookOut)
def update_book(
    book_id: int,
    data: BookUpdate,
    session: Session = Depends(get_session),
):
    book = get_book_or_404(session, book_id)
    get_author_or_404(session, data.author_id)
    book.title = data.title.strip()
    book.description = data.description
    book.author_id = data.author_id
    session.commit()
    session.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = get_book_or_404(session, book_id)
    session.delete(book)
    session.commit()
    return None


# Relationship / JOIN example


@app.get("/books-with-authors", response_model=list[BookWithAuthor])
def list_books_with_authors(session: Session = Depends(get_session)):
    statement = select(Book).options(joinedload(Book.author)).order_by(Book.id)
    return session.scalars(statement).all()


@app.get("/authors/{author_id}/books", response_model=list[BookOut])
def list_author_books(author_id: int, session: Session = Depends(get_session)):
    get_author_or_404(session, author_id)
    statement = select(Book).where(Book.author_id == author_id).order_by(Book.id)
    return session.scalars(statement).all()
