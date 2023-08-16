from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
 


app = FastAPI()




# my_posts = [
#     {
#              "title": "Post 1 title", 
#              "content": "content of post 1", 
#              "id": 1 
#              },
#              {
#              "title": "Post 2 title", 
#              "content": "content of post 2", 
#              "id": 2 
#              }]

while True:

    # connecting a database 
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='zezo', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB Connection Successful")
        break

    except Exception as error:
        print("DB Connection failed")
        print("Error", error)
        time.sleep(2)




# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return{"Hello-World"}




