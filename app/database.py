from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import psycopg2

#DB Driver
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

SQLALCHMEY_DATABASE_URL = 'postgresql://postgres:zezo@localhost/fastapi'

engine = create_engine(SQLALCHMEY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:

#     # connecting a database
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='zezo', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB Connection Successful")
#         break

#     except Exception as error:
#         print("DB Connection failed")
#         print("Error", error)
#         time.sleep(2)