from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel, EmailStr
from app.routers import post, user
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas, utils
from app.database import engine, SessionLocal, get_db, Base


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



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

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
