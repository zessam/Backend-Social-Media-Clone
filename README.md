# Backend clone  of social media app by using FastAPI

#### This API  has 4 routes

## 1) Post route

#### This route is responsible for creating posts, deleting posts, updating posts, and Checking post

## 2) Users route

#### This route is about creating users and searching users by id

## 3) Auth route

#### This route is about the login system

## 4) Vote route

 #### This route is about the likes or vote system and this route contain code for update or back vote there is no logic about down vote

# How to run locally
First, clone this repo by using the following command
````

git clone [https://github.com/Sanjeev-Thiyagarajan/fastapi-course.git](https://github.com/zezo-rgb/FASTAPI-Course.git)

````
then 
````

cd FASTAPI

````

Then install a fast app using all flag like 

````

pip install fastapi[all]

````

Then go to this repo folder in your local computer and run the following command
````

uvicorn main:app --reload

````

Then you can use the following link to use the  API

````

http://127.0.0.1:8000/docs 

````

## After running this API you need a database in Postgres 
Create a database in Postgres then create a file name .env and write the following things in your file 

````
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = password_that_you_set
DATABASE_NAME = name_of_database
DATABASE_USERNAME = User_name
SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60(base)

````
