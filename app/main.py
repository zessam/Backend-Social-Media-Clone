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
    published: bool = True #default true
    rating: Optional[int] = None

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
def get_posts():
    cursor.execute("SELECT * FROM posts ORDER BY id ASC;")
    posts =  cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    new_post = cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s)  RETURNING *""", 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post} 
#title str, content str
 

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    
    post = cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    conn.commit()
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
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deletedPost = cursor.fetchone()
    conn.commit()
   
    
    if deletedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, (str(id))))
    updated_post = cursor.fetchone()
    conn.commit()

    if  updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    return{"data": updated_post}
