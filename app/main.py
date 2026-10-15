from fastapi import FastAPI, APIRouter, Depends
# from typing import Optional
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
# import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, authn, vote
from .config import Settings

from fastapi.middleware.cors import CORSMiddleware

# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     path: int
#     # database_password: str = "rakesh@2002"
#     database_username: str = "postgres"
#     secret_key: str = "234dfsdf676ds7f676df"
    
#     # database_hostname: str
#     # database_port: str
#     # database_password: str
#     # database_name: str
#     # database_username: str

# settings = Settings()

# print(settings.database_password)



# # this tells postgresql to create the model if it is not present there.
# models.Base.metadata.create_all(bind=engine)
# # after using alembic we don't need this above code...

app = FastAPI()

# mydata = [{"title":"title of post 1", "content":"content of post 1", "id":1}, 
#           {"title":"title of post 2", "content":"content of post 2", "id":2}]


# @app.get("/posts")
# def get_pots():
#     return {"data": mydata}


# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM products""")
#     post = cursor.fetchall()
#     return {"data": post}

# @app.get("/")
# def root(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()  # ORM, using this got all posts from DB wihtout sql any query.
#     print(posts)  # will return sql query

#     return posts

# origins = [
#     "https://www.google.com",
#     "https://www.youtube.com"

# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():

    return {"message": " hello world! name is rd"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authn.router)
app.include_router(vote.router)

