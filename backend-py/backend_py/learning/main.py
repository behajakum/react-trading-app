import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from trade_apis.config.config import get_server_config, get_system_config, get_broker_config

app = FastAPI()
templates = Jinja2Templates(directory='templates')


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item) -> Item:
    return item


@app.get("/{name}")
async def display_name(name: str):
    return {"message": f"Hello {name}"}


@app.get("/blog/publish")
async def get_blogs(limit: str, is_show: bool):
    return {'data': f'blog list: {limit}, show: {is_show}'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
