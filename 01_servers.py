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
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Items API</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #020408;
    --gold: #f0c040;
    --teal: #00e5cc;
    --red: #ff3b5c;
    --white: #f0f0f0;
    --dim: rgba(240,192,64,0.08);
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--white);
    font-family: 'DM Mono', monospace;
    min-height: 100vh;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  /* ── GRID BACKGROUND ── */
  body::before {
    content: '';
    position: fixed; inset: 0;
    background-image:
      linear-gradient(rgba(0,229,204,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,229,204,0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
    animation: gridShift 20s linear infinite;
  }
  @keyframes gridShift {
    0%   { background-position: 0 0; }
    100% { background-position: 48px 48px; }
  }

  /* ── CANVAS 3D ── */
  #bg3d {
    position: fixed; inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: 0.55;
  }

  /* ── SCAN LINE ── */
  body::after {
    content: '';
    position: fixed; inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0,0,0,0.12) 2px,
      rgba(0,0,0,0.12) 4px
    );
    pointer-events: none;
    z-index: 10;
  }

  /* ── HERO ── */
  .hero {
    position: relative;
    z-index: 5;
    text-align: center;
    padding: 60px 32px 48px;
    max-width: 860px;
  }

  .badge {
    display: inline-block;
    background: var(--dim);
    border: 1px solid rgba(240,192,64,0.3);
    color: var(--gold);
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 2px;
    margin-bottom: 28px;
    animation: fadeUp 0.8s ease both;
  }

  h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(64px, 12vw, 130px);
    line-height: 0.92;
    letter-spacing: -0.01em;
    background: linear-gradient(135deg, var(--white) 0%, var(--gold) 45%, var(--teal) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: fadeUp 0.9s 0.1s ease both;
    user-select: none;
  }

  .subtitle {
    margin-top: 20px;
    font-size: 0.82rem;
    color: rgba(240,240,240,0.45);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    animation: fadeUp 1s 0.2s ease both;
  }

  /* ── PILLS ── */
  .pills {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 36px 0;
    animation: fadeUp 1s 0.3s ease both;
  }
  .pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    color: rgba(240,240,240,0.6);
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    padding: 6px 14px;
    border-radius: 2px;
    text-transform: uppercase;
  }
  .pill span { color: var(--teal); margin-right: 5px; }

  /* ── DIVIDER ── */
  .divider {
    width: 80px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 0 auto 36px;
    animation: fadeUp 1s 0.35s ease both;
  }

  /* ── CTA BUTTON ── */
  .cta {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 16px 40px;
    border: 1px solid var(--gold);
    color: var(--gold);
    text-decoration: none;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    background: transparent;
    position: relative;
    overflow: hidden;
    transition: color 0.3s;
    animation: fadeUp 1s 0.45s ease both;
  }
  .cta::before {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--gold);
    transform: translateX(-100%);
    transition: transform 0.35s cubic-bezier(0.77,0,0.18,1);
    z-index: -1;
  }
  .cta:hover { color: var(--bg); }
  .cta:hover::before { transform: translateX(0); }
  .cta svg { transition: transform 0.3s; }
  .cta:hover svg { transform: translateX(4px); }

  /* ── ENDPOINTS GRID ── */
  .endpoints {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.06);
    width: 100%;
    max-width: 700px;
    margin: 56px auto 0;
    animation: fadeUp 1s 0.55s ease both;
  }
  .ep {
    background: var(--bg);
    padding: 20px 18px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    transition: background 0.2s;
  }
  .ep:hover { background: rgba(0,229,204,0.04); }
  .method {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    font-weight: 500;
    padding: 2px 7px;
    border-radius: 2px;
    display: inline-block;
    width: fit-content;
  }
  .get  { background: rgba(0,229,204,0.15); color: var(--teal); }
  .post { background: rgba(240,192,64,0.15); color: var(--gold); }
  .put  { background: rgba(100,160,255,0.15); color: #7ab0ff; }
  .del  { background: rgba(255,59,92,0.15);   color: var(--red); }
  .ep-path {
    font-size: 0.72rem;
    color: rgba(240,240,240,0.55);
    margin-top: 3px;
  }
  .ep-desc {
    font-size: 0.65rem;
    color: rgba(240,240,240,0.28);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  /* ── FOOTER ── */
  footer {
    position: relative;
    z-index: 5;
    margin-top: 64px;
    margin-bottom: 32px;
    font-size: 0.65rem;
    color: rgba(240,240,240,0.18);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    text-align: center;
  }

  /* ── KEYFRAMES ── */
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
  }
</style>
</head>
<body>

<canvas id="bg3d"></canvas>

<div class="hero">
  <div class="badge">REST API &mdash; v1.0</div>
  <h1>Items<br/>API</h1>
  <p class="subtitle">id &bull; name &bull; price &bull; description</p>

  <div class="pills">
    <div class="pill"><span>●</span>Live</div>
    <div class="pill"><span>⚡</span>FastAPI</div>
    <div class="pill"><span>◈</span>JSON</div>
    <div class="pill"><span>✦</span>RESTful</div>
  </div>

  <div class="divider"></div>

  <a href="/docs" class="cta">
    Explore Swagger Docs
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </a>

  <div class="endpoints">
    <div class="ep">
      <span class="method get">GET</span>
      <div class="ep-path">/items</div>
      <div class="ep-desc">List all</div>
    </div>
    <div class="ep">
      <span class="method post">POST</span>
      <div class="ep-path">/items</div>
      <div class="ep-desc">Create</div>
    </div>
    <div class="ep">
      <span class="method get">GET</span>
      <div class="ep-path">/items/{id}</div>
      <div class="ep-desc">Fetch one</div>
    </div>
    <div class="ep">
      <span class="method put">PUT</span>
      <div class="ep-path">/items/{id}</div>
      <div class="ep-desc">Update</div>
    </div>
    <div class="ep">
      <span class="method del">DELETE</span>
      <div class="ep-path">/items/{id}</div>
      <div class="ep-desc">Remove</div>
    </div>
  </div>
</div>

<footer>Items API &mdash; powered by FastAPI</footer>

<script>
// ── 3D floating particles on canvas ──
const canvas = document.getElementById('bg3d');
const ctx = canvas.getContext('2d');
let W, H, nodes;

const COLORS = ['#f0c040','#00e5cc','#ff3b5c','#7ab0ff'];

function resize() {
  W = canvas.width  = window.innerWidth;
  H = canvas.height = window.innerHeight;
}

function initNodes() {
  nodes = Array.from({length: 60}, () => ({
    x: Math.random() * W,
    y: Math.random() * H,
    z: Math.random() * 800 + 100,
    vx: (Math.random() - 0.5) * 0.5,
    vy: (Math.random() - 0.5) * 0.5,
    vz: (Math.random() - 0.5) * 1.2,
    color: COLORS[Math.floor(Math.random() * COLORS.length)],
  }));
}

function project(x, y, z) {
  const fov = 600;
  const scale = fov / (fov + z);
  return {
    sx: W/2 + (x - W/2) * scale,
    sy: H/2 + (y - H/2) * scale,
    scale,
  };
}

function draw() {
  ctx.clearRect(0, 0, W, H);

  // draw edges
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i], b = nodes[j];
      const dx = a.x - b.x, dy = a.y - b.y, dz = a.z - b.z;
      const dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
      if (dist < 220) {
        const pa = project(a.x, a.y, a.z);
        const pb = project(b.x, b.y, b.z);
        ctx.beginPath();
        ctx.moveTo(pa.sx, pa.sy);
        ctx.lineTo(pb.sx, pb.sy);
        ctx.strokeStyle = `rgba(0,229,204,${0.12 * (1 - dist/220)})`;
        ctx.lineWidth = 0.6;
        ctx.stroke();
      }
    }
  }

  // draw nodes
  for (const n of nodes) {
    const p = project(n.x, n.y, n.z);
    const r = Math.max(1, 4 * p.scale);
    ctx.beginPath();
    ctx.arc(p.sx, p.sy, r, 0, Math.PI * 2);
    ctx.fillStyle = n.color;
    ctx.globalAlpha = 0.7 * p.scale;
    ctx.fill();
    ctx.globalAlpha = 1;
  }
}

function update() {
  for (const n of nodes) {
    n.x += n.vx; n.y += n.vy; n.z += n.vz;
    if (n.x < 0 || n.x > W)  n.vx *= -1;
    if (n.y < 0 || n.y > H)  n.vy *= -1;
    if (n.z < 0 || n.z > 900) n.vz *= -1;
  }
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

resize();
initNodes();
loop();
window.addEventListener('resize', () => { resize(); initNodes(); });
</script>
</body>
</html>'''

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