from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, field_validator


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data":"this is yout posts"}

@app.post("/createposts")
def create_posts(post:Post):
    print(post.rating)
    print(post.dict())
    return {"data":post} 