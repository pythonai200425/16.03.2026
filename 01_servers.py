from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import HTMLResponse
from fastapi import Response, status

import dal_sqlite

# pip install uvicorn
# pip install fastapi
# uvicorn 01_servers:app --port 8002 --reload
# swagger = http://127.0.0.1:8002/items
# swagger = http://127.0.0.1:8002/docs

# pip install -r .\requirements.txt

# if page not reloaded change the port


app = FastAPI()

class Product(BaseModel):
    # class variables
    name: str
    price: float
    stock: int
    category: str


# Go to claude.ai
'''
i have a rest api for items with id name price description
in the main url i need to return a nice decorated page with animation and colors and 3d and link to swagger
please update this code:
@app.get("/", response_class=HTMLResponse)
def basic_url():
    return """<h1>Welcome to my site!!</h1><br /><a href="/docs" />Browse to swagger</h2>""" 
'''
@app.get("/", response_class=HTMLResponse)
def basic_url():
  return "Welcome!"

# ---- GET all ----
@app.get("/products")
def get_prodcuts():
    return dal_sqlite.get_all_products()

# ---- GET by id ----
@app.get("/products/{item_id}")
def get_product_by_id(item_id: int, response: Response):
    product = dal_sqlite.get_product_by_id(item_id)
    if not product:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {}
    return product

# ---- POST create ----
@app.post("/products")
def create_product(product: Product, response: Response):
    row_id = dal_sqlite.insert_product(product.name, product.price, product.stock, product.category)
    new_product = {**product.__dict__, 'id': row_id}
    # d1  = {a: 1, b: 2}
    # d2 = {**d1 a: 1, b: 2, 'id': row_id}
    print(new_product)
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Product created", "item": new_product,
            "url": f"/products/{new_product['id']}"}

@app.delete("/tables/products")
def drop_table_products():
    dal_sqlite.drop_table_products()
    return {'message': 'done'}

'''
# ---- PUT update full ----
# dict1['danny'] = 90
# update , if not exist create (replace null)
@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item["id"] == item_id:
            new_item = {
                "id": item_id,
                "name": updated_item.name,
                "price": updated_item.price,
                "description": updated_item.description
            }
            items[index] = new_item
            return {"message": "Item replaced", "item": new_item}

    # raise HTTPException(status_code=404, detail="Item not found")
    # not found -- create new
    global auto_increment
    auto_increment += 1
    new_item = {
        "id": auto_increment,
        "name" : updated_item.name,
        "price": updated_item.price,
        "description": updated_item.description
    }
    items.append(new_item)
    return {"message": "Item created", "item": new_item,
            "url": f"http://127.0.0.1:8003/items/{new_item['id']}"}

# ---- PATCH partial update ----
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

# update only, if not exist -- error
@app.patch("/items/{item_id}")
def patch_item(item_id: int, item_update: ItemUpdate):
    for item in items:
        if item["id"] == item_id:
            # Check each field manually
            if item_update.name is not None:
                item["name"] = item_update.name

            if item_update.price is not None:
                item["price"] = item_update.price

            if item_update.description is not None:
                item["description"] = item_update.description

            return {"message": "Item updated", "item": item}

    raise HTTPException(status_code=404, detail="Item not found")

# ---- DELETE ----
@app.delete("/items/{item_id}")
def delete_item_by_id(item_id: int):
    for i, item in enumerate(items):
        if item["id"] == item_id:
            deleted = items.pop(i)
            return {"message": f"item {item_id} deleted", "deleted item": deleted}
    raise HTTPException(status_code=404, detail=f"Item id={item_id} not found")


# d1 = {1: {'name': 'suzi', 'age': 60}}
# d1[1] = {'name': 'danny'}  # put
'''