from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:

    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='password',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successful")
        break
    except Exception as error:
        print("connecting to database failed")
        print("Error:", error)
        time.sleep(2)


my_post = [{"title":"title1", "content":"content1", "id":1}, {"title":"sri", "content":"my name is sriram", "id":2}]


# function to find post
def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i
    return None 

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts",status_code = status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """, (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post)-1]
    return {"post_detail":post}

@app.get("/posts/{id}")
def get_post(id: int):

   post = find_post(id)
   if post == None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
   return {"post_detail":post}


@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {"data":post_dict}