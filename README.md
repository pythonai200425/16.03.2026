# 🛒 Items REST API

> A clean, fast REST API for managing items — built with **FastAPI** · Updated **16.03.2026**

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
| 📦 All items | http://127.0.0.1:8002/items |

> ⚠️ If the page doesn't reload, try changing the port (e.g. `--port 8003`)

---

## 📦 Item Schema

```json
{
  "id":          1,
  "name":        "Laptop",
  "price":       1200.0,
  "description": "Gaming laptop"
}
```

| Field | Type | Required |
|-------|------|----------|
| `id` | `int` | auto-generated |
| `name` | `str` | ✅ yes |
| `price` | `float` | ✅ yes |
| `description` | `str` | optional |

---

## 🔌 Endpoints

### `GET /` — Home page
Returns a decorated HTML landing page with a link to Swagger docs.

---

### `GET /items` — List all items
```bash
curl http://127.0.0.1:8002/items
```
**Response `200`**
```json
[
  { "id": 1, "name": "Laptop",  "price": 1200, "description": "Gaming laptop" },
  { "id": 2, "name": "Phone",   "price": 800,  "description": "Smartphone" }
]
```

---

### `GET /items/{id}` — Get item by ID
```bash
curl http://127.0.0.1:8002/items/1
```
| Status | Meaning |
|--------|---------|
| `200` | Item returned |
| `404` | Item not found |

---

### `POST /items` — Create item
```bash
curl -X POST http://127.0.0.1:8002/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Monitor", "price": 350, "description": "4K display"}'
```
**Response `201`**
```json
{
  "message": "Item created",
  "item": { "id": 3, "name": "Monitor", "price": 350, "description": "4K display" },
  "url": "/items/3"
}
```

---

### `PUT /items/{id}` — Full replace (upsert)
Replaces all fields. If the item doesn't exist, **creates a new one**.
```bash
curl -X PUT http://127.0.0.1:8002/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop Pro", "price": 1500, "description": "Updated model"}'
```
| Status | Meaning |
|--------|---------|
| `200` | Item replaced or created |

---

### `PATCH /items/{id}` — Partial update
Updates only the fields you send. Item **must exist** (no upsert).
```bash
curl -X PATCH http://127.0.0.1:8002/items/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 999}'
```
| Status | Meaning |
|--------|---------|
| `200` | Item updated |
| `404` | Item not found |

---

### `DELETE /items/{id}` — Delete item
```bash
curl -X DELETE http://127.0.0.1:8002/items/1
```
**Response `200`**
```json
{
  "message": "item 1 deleted",
  "deleted item": { "id": 1, "name": "Laptop", "price": 1200, "description": "Gaming laptop" }
}
```
| Status | Meaning |
|--------|---------|
| `200` | Item deleted |
| `404` | Item not found |

---

## 🔁 PUT vs PATCH

| | `PUT` | `PATCH` |
|-|-------|---------|
| Sends | All fields | Only changed fields |
| Item missing | Creates new (upsert) | Returns `404` |
| Use when | Full replacement | Small updates |

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |
| [Pydantic](https://docs.pydantic.dev/) | Data validation |

---

## 📁 Project Structure

```
.
├── 01_servers.py       # Main API file
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

*Powered by FastAPI ⚡*
