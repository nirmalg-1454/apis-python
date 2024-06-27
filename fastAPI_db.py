from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
import sqlite3

# Create an instance of FastAPI
app = FastAPI()
db_file = "items.db"

def create_connection():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

# Define your endpoints
@app.get("/items/", description="Get all Items")
def read_items():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * from items")
    items = cursor.fetchall()
    conn.close()
    return [dict(item) for item in items]

@app.get("/items/{item_id}", description="Get Single Item")
def read_item(item_id: int):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from items where item_id = {item_id}")
    items = cursor.fetchall()
    conn.close()
    if items:
        return [dict(item) for item in items]
    else:
        return {item_id: "NOT FOUND"}

@app.post("/items/<item_id>")
def add_item(item_id: int, desc: str = None):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO items values({item_id}, {desc}")
    conn.commit()
    conn.close()
    return {item_id: "Item Added Successfully"}

@app.put("/items/{item_id}")
def update_item(item_id: int, desc: str = None):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE items set description = {desc} where item_id = {item_id}")
    conn.commit()
    conn.close()
    return {cursor.rowcount: f"Rows Updated Successfully for {item_id}"}

@app.delete("/items/<item_id>")
def delete_item(item_id: int):
    fake_items_db.pop(item_id)
    return {item_id: "Deleted Successfully"}

# Route for serving the Swagger UI
@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="FastAPI Swagger UI")

# Include the auto-generated OpenAPI schema
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_json():
    return app.openapi()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)