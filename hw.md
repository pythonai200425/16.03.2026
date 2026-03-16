# Homework – Build a REST API for Books

## Goal

Build a **REST API** using **FastAPI** that works with a **SQLite DAL (Data Access Layer)** for a table called **books**

Your task is to build a **complete REST API for managing books**

The system should follow this architecture:

Client → REST API → DAL → SQLite database

The API receives HTTP requests, validates input using **Pydantic**, and calls SQL functions implemented in the DAL

# Part 1 – Books Database

Create a SQLite table called **books**

Suggested fields for the table:

* `id` – integer primary key, auto increment
* `title` – text, required
* `author` – text, required
* `language` – text
* `price` – real (must be >= 0)
* `published_year` – integer
* `created_at` – timestamp (default current time)

# Part 2 – Data Access Layer (DAL)

You are given with the SQL code (see below -- DAL code)  

The DAL should contain functions such as:  

* create the books table
* drop and recreate the books table
* insert a new book
* return all books
* return one book by id
* update a book by id
* delete a book by id
* convert database rows to dictionaries
* open a SQLite connection

# Part 3 – Build the REST API

Your REST API should include at least the following endpoints.

## Root endpoint

### Get all books

`GET /books`

Returns a list of all books in the database

### Get one book

`GET /books/{book_id}`

Returns the book with the given id

### Create a new book

`POST /books`

Adds a new book to the database

The request body must be validated using a **Pydantic model**

### Update a book

`PUT /books/{book_id}`

Updates an existing book

### Delete a book

`DELETE /books/{book_id}`

Deletes the book with the given id

### Recreate the books table

`DELETE /tables/books`

Drops and recreates the books table

This is useful during development and testing.

# Part 4 – Pydantic Models

You must create **Pydantic models** that represent the request body of your API  

# DAL code

Below is a complete example of a **DAL file** for the `books` table

```python
import sqlite3

DB_NAME = "books.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


def create_table_books():
    query = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        language TEXT,
        price REAL NOT NULL CHECK(price >= 0),
        published_year INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    with get_connection() as conn:
        conn.execute(query)


def drop_table_books():
    with get_connection() as conn:
        conn.execute("DROP TABLE IF EXISTS books")


def recreate_table_books():
    drop_table_books()
    create_table_books()


def insert_book(title, author, language, price, published_year):
    query = """
    INSERT INTO books (title, author, language, price, published_year)
    VALUES (?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.execute(query, (title, author, language, price, published_year))
        book_id = cursor.lastrowid
    return get_book_by_id(book_id)


def get_all_books():
    query = """
    SELECT id, title, author, language, price, published_year, created_at
    FROM books
    ORDER BY id
    """
    with get_connection() as conn:
        rows = conn.execute(query).fetchall()
    return [row_to_dict(row) for row in rows]


def get_book_by_id(book_id):
    query = """
    SELECT id, title, author, language, price, published_year, created_at
    FROM books
    WHERE id = ?
    """
    with get_connection() as conn:
        row = conn.execute(query, (book_id,)).fetchone()
    return row_to_dict(row)


def update_book(book_id, title, author, language, price, published_year):
    query = """
    UPDATE books
    SET title = ?,
        author = ?,
        language = ?,
        price = ?,
        published_year = ?
    WHERE id = ?
    """
    with get_connection() as conn:
        cursor = conn.execute(query, (title, author, language, price, published_year, book_id))
        affected_rows = cursor.rowcount
    if affected_rows == 0:
        return None
    return get_book_by_id(book_id)


def delete_book(book_id):
    existing_book = get_book_by_id(book_id)
    if existing_book is None:
        return None
    with get_connection() as conn:
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    return existing_book
```

Good luck 🚀

Submit email: **[pythonai200425+restsql@gmail.com](mailto:pythonai200425+restsql@gmail.com)**
