from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app = FastAPI()

@app.get("/blog")
def blog(limit, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs"}
    else:
        return {"data": f"{limit} blogs from db"}

@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}

@app.get("/blog/{id}")
def show(id: int):
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id: int):
    return {"data": id}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post("/blog")
def blog_create(request: Blog):
    print(request)
    return request