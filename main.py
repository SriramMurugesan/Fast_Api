from typing import Optional
from fastapi import FastAPI, Response,status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_post = [{"title":"title1", "content":"content1", "id":1}, {"title":"sri", "content":"my name is sriram", "id":2}]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data":my_post}

@app.post("/posts")
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_post.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post)-1]
    return {"post_detail":post}

@app.get("/posts/{id}")
def get_post(id: int,response: Response):

   post = find_post(id)
   if post == None:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":f"post with id {id} not found"}
   return {"post_detail":post}
