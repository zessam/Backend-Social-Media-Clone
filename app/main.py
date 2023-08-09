from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal, get_db



models.Base.metadata.create_all(bind=engine)
 


app = FastAPI()





class Post(BaseModel):
    title: str 
    content: str
    published: bool = True #default true
    #rating: Optional[int] = None

my_posts = [
    {
             "title": "Post 1 title", 
             "content": "content of post 1", 
             "id": 1 
             },
             {
             "title": "Post 2 title", 
             "content": "content of post 2", 
             "id": 2 
             }]

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




def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p




@app.get("/")
def root():
    return{"message": "Hello-World"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts ORDER BY id ASC;")
    # posts =  cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}






@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # new_post = cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s)  RETURNING *""", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post} 
#title str, content str
 

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    
    # post = cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post: 
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found 404"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found 404")
    return{"post_detail": post}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deletedPost = cursor.fetchone()
    # conn.commit()
    deletedPost = db.query(models.Post).filter(models.Post.id == id)
    


    if deletedPost.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    deletedPost.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, (str(id))))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)


    if  post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return{"data": post_query.first()}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}