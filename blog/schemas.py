from typing import List
from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

class ShowBlog(Blog):
    title: str
    body: str
    class Config:
        orm_mode = True