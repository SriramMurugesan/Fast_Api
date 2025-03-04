from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel, EmailStr
from app.routers import post, user, auth
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

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
