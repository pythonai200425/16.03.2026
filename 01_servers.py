from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi import Response, status

import dal_sqlite

# pip install uvicorn fastapi
# uvicorn 01_servers:app --port 8002 --reload
# swagger: http://127.0.0.1:8002/docs

app = FastAPI()


class Product(BaseModel):
    name: str
    price: float
    stock: int
    category: str


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
def basic_url():
    return "Welcome!"


# ---- GET all ----
@app.get("/products")
def get_products():
    return dal_sqlite.get_all_products()


# ---- GET by id ----
@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, response: Response):
    product = dal_sqlite.get_product_by_id(product_id)
    if not product:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {}
    return product


# ---- POST create ----
@app.post("/products")
def create_product(product: Product, response: Response):
    row_id = dal_sqlite.insert_product(product.name, product.price, product.stock, product.category)
    new_product = {**product.__dict__, "id": row_id}
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Product created", "item": new_product,
            "url": f"/products/{row_id}"}


# ---- PUT full update ----
# Replaces the entire product; if not found, creates a new one
@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product, response: Response):
    updated = dal_sqlite.update_product(product_id, product.name, product.price, product.stock, product.category)
    if updated:
        return {"message": "Product updated", "item": {**product.__dict__, "id": product_id}}

    # Not found → create new
    row_id = dal_sqlite.insert_product(product.name, product.price, product.stock, product.category)
    new_product = {**product.__dict__, "id": row_id}
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Product created", "item": new_product,
            "url": f"/products/{row_id}"}

# ---- DELETE by id ----
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    deleted = dal_sqlite.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Product id={product_id} not found")
    return {"message": f"Product {product_id} deleted"}


# ---- DROP & recreate products table ----
@app.delete("/tables/products")
def drop_table_products():
    dal_sqlite.drop_table_products()
    return {"message": "Table dropped and recreated"}