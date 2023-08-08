from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange



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


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p




@app.get("/")
def root():
    return{"message": "Hello-World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000000000)
    my_posts.append(post)

    return {"data": post_dict} 
#title str, content str


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
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
def delete_post(id: int):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"data": post_dict}
