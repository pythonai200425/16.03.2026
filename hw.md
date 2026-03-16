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

You are given with the SQL code (see below)  
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

# Full DAL File to Build

Below is a complete example of a **DAL file** for the `books` table.

Students can use this as the DAL layer that the REST API will call.

```python
import sqlite3

DB_NAME = "books.db"


class DALSql:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.create_table_books()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def row_to_dict(self, row):
        if row is None:
            return None
        return dict(row)

    def create_table_books(self):
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
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    def drop_table_books(self):
        query = "DROP TABLE IF EXISTS books"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    def recreate_table_books(self):
        self.drop_table_books()
        self.create_table_books()

    def insert_book(self, title, author, language, price, published_year):
        query = """
        INSERT INTO books (title, author, language, price, published_year)
        VALUES (?, ?, ?, ?, ?)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (title, author, language, price, published_year))
        conn.commit()
        book_id = cursor.lastrowid
        conn.close()
        return self.get_book_by_id(book_id)

    def get_all_books(self):
        query = """
        SELECT id, title, author, language, price, published_year, created_at
        FROM books
        ORDER BY id
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return [self.row_to_dict(row) for row in rows]

    def get_book_by_id(self, book_id):
        query = """
        SELECT id, title, author, language, price, published_year, created_at
        FROM books
        WHERE id = ?
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (book_id,))
        row = cursor.fetchone()
        conn.close()
        return self.row_to_dict(row)

    def update_book(self, book_id, title, author, language, price, published_year):
        query = """
        UPDATE books
        SET title = ?,
            author = ?,
            language = ?,
            price = ?,
            published_year = ?
        WHERE id = ?
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (title, author, language, price, published_year, book_id))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()

        if affected_rows == 0:
            return None

        return self.get_book_by_id(book_id)

    def delete_book(self, book_id):
        existing_book = self.get_book_by_id(book_id)
        if existing_book is None:
            return None

        query = "DELETE FROM books WHERE id = ?"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (book_id,))
        conn.commit()
        conn.close()
        return existing_book
```

Good luck 🚀

Submit email: **[pythonai200425+restsql@gmail.com](mailto:pythonai200425+restsql@gmail.com)**
