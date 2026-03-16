# 🛒 Products REST API
> A clean, fast REST API for managing products — built with **FastAPI** + **SQLite** · Updated **16.03.2026**
---
## 🚀 Quick Start
### 1 · Install dependencies
```bash
pip install -r requirements.txt
```
### 2 · Run the server
```bash
uvicorn 01_servers:app --port 8002 --reload
```
### 3 · Open in browser
| Interface | URL |
|-----------|-----|
| 🏠 Home page | http://127.0.0.1:8002/ |
| 📄 Swagger UI | http://127.0.0.1:8002/docs |
| 📦 All products | http://127.0.0.1:8002/products |
> ⚠️ If the page doesn't reload, try changing the port (e.g. `--port 8003`)
---
## 📦 Product Schema
```json
{
  "id":         1,
  "name":       "Laptop",
  "price":      1200.0,
  "stock":      10,
  "category":   "Electronics",
  "created_at": "2026-03-16 10:00:00"
}
```
| Field | Type | Required |
|-------|------|----------|
| `id` | `int` | auto-generated |
| `name` | `str` | ✅ yes |
| `price` | `float` | ✅ yes (≥ 0) |
| `stock` | `int` | ✅ yes (≥ 0) |
| `category` | `str` | ✅ yes |
| `created_at` | `str` | auto-generated |
---
## 🔌 Endpoints
### `GET /` — Home page
Returns a decorated HTML landing page with a link to Swagger docs.
---
### `GET /products` — List all products
```bash
curl http://127.0.0.1:8002/products
```
**Response `200`**
```json
[
  { "id": 1, "name": "Laptop",  "price": 1200.0, "stock": 10, "category": "Electronics", "created_at": "2026-03-16 10:00:00" },
  { "id": 2, "name": "Phone",   "price": 800.0,  "stock": 25, "category": "Electronics", "created_at": "2026-03-16 10:01:00" }
]
```
---
### `GET /products/{id}` — Get product by ID
```bash
curl http://127.0.0.1:8002/products/1
```
| Status | Meaning |
|--------|---------|
| `200` | Product returned |
| `204` | Product not found |
---
### `POST /products` — Create product
```bash
curl -X POST http://127.0.0.1:8002/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Monitor", "price": 350.0, "stock": 5, "category": "Electronics"}'
```
**Response `201`**
```json
{
  "message": "Product created",
  "item": { "id": 3, "name": "Monitor", "price": 350.0, "stock": 5, "category": "Electronics" },
  "url": "/products/3"
}
```
---
### `PUT /products/{id}` — Full replace (upsert)
Replaces all fields. If the product doesn't exist, **creates a new one**.
```bash
curl -X PUT http://127.0.0.1:8002/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop Pro", "price": 1500.0, "stock": 8, "category": "Electronics"}'
```
| Status | Meaning |
|--------|---------|
| `200` | Product replaced |
| `201` | Product not found — created new |
---
### `DELETE /products/{id}` — Delete product
```bash
curl -X DELETE http://127.0.0.1:8002/products/1
```
**Response `200`**
```json
{
  "message": "Product 1 deleted"
}
```
| Status | Meaning |
|--------|---------|
| `200` | Product deleted |
| `404` | Product not found |
---
### `DELETE /tables/products` — Drop & recreate table
> ⚠️ **Destructive** — deletes all products and recreates the empty table.
```bash
curl -X DELETE http://127.0.0.1:8002/tables/products
```
**Response `200`**
```json
{ "message": "Table dropped and recreated" }
```
---
## 🔁 PUT vs PATCH
| | `PUT` | `PATCH` |
|-|-------|---------|
| Sends | All fields | Only changed fields |
| Product missing | Creates new (upsert) | Returns `404` |
| Use when | Full replacement | Small updates |
---
## 🛠 Tech Stack
| Tool | Purpose |
|------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |
| [Pydantic](https://docs.pydantic.dev/) | Data validation |
| [SQLite](https://www.sqlite.org/) | Persistent database |
---
## 📁 Project Structure
```
.
├── 01_servers.py       # Main API file
├── dal_sqlite.py       # Database access layer (SQLite)
├── products.db         # SQLite database (auto-created)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```
---
## 📋 Requirements
```
fastapi
uvicorn
pydantic
```
Install all at once:
```bash
pip install -r requirements.txt
```
---
*Powered by FastAPI ⚡ & SQLite 🗄️*
