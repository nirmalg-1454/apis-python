from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

# Create an instance of FastAPI
app = FastAPI()

# Example data - In a real application, this would come from a database or other source
fake_items_db = {
    1: {"1": "Foo"},
    2: {"2": "Bar"},
    3: {"3": "Baz"}
}

# Define your endpoints
@app.get("/items/")
def read_items():
    return fake_items_db

@app.get("/items/{item_id}")
def read_item(item_id: int):
    try:
        return fake_items_db[item_id]
    except:
        return {item_id: "Item Not Found"}

@app.post("/items/<item_id>")
def add_item(item_id: int, desc: str = None):
    return {}

@app.put("/items/{item_id}")
def update_item(item_id: int, desc: str = None):
    fake_items_db[item_id] = {item_id: desc}
    return {item_id: "Item Updated Succesfully"}

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