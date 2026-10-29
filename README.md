# PostgreSQL Book Manager API

A small, practical **FastAPI** project for learning relational databases with **PostgreSQL**, **SQLAlchemy ORM**, and **Alembic**.

This project builds on the CRUD/API concepts practiced in my earlier repository: **[FastAPI Book Manager](https://github.com/MSirani/fastapi-book-manager)**. That repository is the starting point for learning FastAPI endpoints and basic book CRUD; this project takes the next step by separating authors and books into related tables, using PostgreSQL, and managing schema changes with Alembic.

## What this project demonstrates

- FastAPI REST endpoints and automatic interactive docs
- PostgreSQL database connection through SQLAlchemy
- Two related tables: `authors` and `books`
- A one-to-many relationship: one author can have multiple books
- `ForeignKey` constraints to maintain referential integrity
- CRUD operations for authors and books
- A relationship endpoint that returns each book with its author
- Database schema migrations using Alembic
- Pydantic request/response validation

## Tech stack

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Pydantic
- psycopg 3

## Project structure

```text
postgres-book-manager/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── migrations/
│   ├── versions/
│   │   └── 0001_create_authors_and_books.py
│   ├── env.py
│   └── script.py.mako
├── .env.example
├── .gitignore
├── alembic.ini
├── README.md
└── requirements.txt
```

## Requirements

1. Python 3.11 or newer
2. A running PostgreSQL server (local or hosted)
3. A PostgreSQL database and user with permission to create tables

> Installing the Python packages does **not** install the PostgreSQL database server. If PostgreSQL is blocked or unavailable to download in your region, you can use a trusted hosted PostgreSQL provider that is accessible to you. Keep the database URL private.

## Setup on Windows (Command Prompt)

### 1. Clone the repository

Replace `YOUR_USERNAME` with your GitHub username or use the URL of your own fork.

```bat
git clone https://github.com/YOUR_USERNAME/postgres-book-manager.git
cd postgres-book-manager
```

### 2. Create and activate a virtual environment

```bat
py -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create a PostgreSQL database

Using your PostgreSQL administrator account, create a database and a dedicated application user. Example SQL:

```sql
CREATE USER book_manager WITH PASSWORD 'replace_with_a_strong_password';
CREATE DATABASE book_manager OWNER book_manager;
```

Run these statements in `psql` or a PostgreSQL administration tool. Do not publish the real password.

### 5. Configure the connection

Copy `.env.example` to `.env` and set `DATABASE_URL` to your database connection string.

Example for a local database:

```text
DATABASE_URL=postgresql+psycopg://book_manager:YOUR_PASSWORD@localhost:5432/book_manager
```

If your password contains characters such as `@`, `:`, `/`, or `#`, URL-encode those characters in the connection string.

The app and Alembic read `DATABASE_URL` from the environment. For a simple local workflow, install `python-dotenv` and load `.env` before starting the app. One convenient option is to add this near the top of `app/database.py` and `migrations/env.py` before reading the variable:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 6. Apply the database migration

```bat
python -m alembic upgrade head
```

This creates the `authors` and `books` tables in PostgreSQL. Schema changes should be made through Alembic migrations rather than `Base.metadata.create_all()`.

### 7. Start the API

```bat
python -m uvicorn app.main:app --reload
```

Open these URLs in your browser:

- API root: http://127.0.0.1:8000/
- Interactive Swagger docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/authors` | Create an author |
| `GET` | `/authors` | List authors |
| `GET` | `/authors/{author_id}` | Get one author |
| `PUT` | `/authors/{author_id}` | Update an author |
| `DELETE` | `/authors/{author_id}` | Delete an author and their books |
| `POST` | `/books` | Create a book |
| `GET` | `/books` | List books |
| `GET` | `/books/{book_id}` | Get one book |
| `PUT` | `/books/{book_id}` | Update a book |
| `DELETE` | `/books/{book_id}` | Delete a book |
| `GET` | `/books-with-authors` | List books with author details |
| `GET` | `/authors/{author_id}/books` | List books by one author |

## Quick test in Swagger

1. Open `/docs`.
2. Use `POST /authors` with:

```json
{
  "name": "Ursula K. Le Guin",
  "bio": "American author of speculative fiction."
}
```

3. Copy the returned author `id`.
4. Use `POST /books` with that ID:

```json
{
  "title": "A Wizard of Earthsea",
  "description": "A fantasy novel.",
  "author_id": 1
}
```

5. Open `GET /books-with-authors` to see the book and its related author in one response.

The `author_id` in `books` is a foreign key referencing `authors.id`. This is the relational link that lets the API return joined data.

## Alembic workflow

After changing a SQLAlchemy model:

```bat
python -m alembic revision --autogenerate -m "describe the change"
python -m alembic upgrade head
```

Review each generated migration before applying it. To see the current revision and migration history:

```bat
python -m alembic current
python -m alembic history
```

## Notes

- Never commit `.env`, database passwords, or production connection strings.
- `DELETE /authors/{author_id}` deletes that author's books as well, because the relationship is configured with cascading deletes.
- This is a learning project, not a production deployment template. Before production use, add authentication, stronger operational configuration, tests, and deployment-specific security settings.

## Related project

**[FastAPI Book Manager](https://github.com/MSirani/fastapi-book-manager)** — the earlier project used to practice FastAPI routing and basic CRUD. This repository continues that learning path with PostgreSQL, relational tables, SQLAlchemy relationships, and Alembic migrations.
