from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utlils
from .database import engine, get_db
from sqlalchemy.orm import Session

# this tells postgresql to create the model if it is not present there.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Connecting Database
while True: 

    try:
        con = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="rakesh@2002", cursor_factory=RealDictCursor)
        cursor = con.cursor()
        print("database connected successfully.")
        break

    except Exception as error:
        print("Oops! database not connected.")
        print("Error:", error)
        time.sleep(2)

mydata = [{"title":"title of post 1", "content":"content of post 1", "id":1}, 
          {"title":"title of post 2", "content":"content of post 2", "id":2}]


# @app.get("/posts")
# def get_pots():
#     return {"data": mydata}


# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM products""")
#     post = cursor.fetchall()
#     return {"data": post}


# @app.get("/sqlalcehmy")
# def test_posts(db: Session = Depends(get_db)):
#     # print(db)
#     posts = db.query(models.Post).all()  # ORM, using this got all posts from DB wihtout sql any query.
#     print(posts)  # will return sql query

#     return {"status": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # print(db)
    posts = db.query(models.Post).all()  # ORM
    # print(posts)  # will return sql query

    # return {"status": posts}
    return posts


@app.get("/posts/{id}")
def get_one_db_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM products WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f" post id: {id} not found!")
 
    # print(test_post)
    # return {"post_detail": post}
    return post


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.model_dump())
    db.add(new_post)  # to add data in database
    db.commit()  # to commit changes
    db.refresh(new_post)

    # return {"data": new_post}
    return new_post


@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    print(deleted_post)

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found!")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post. published, str(id)))
    # updated_post = cursor.fetchone()
    # con.commit()

    # print(cursor.fetchone())

    post_query = db.query(models.Post). filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found!")

    # post_query.update({'title': 'this is my updated title!', 'content': 'this is my updated content!'}, synchronize_session=False)  # hardcoded updated data

    # post_query.update(post.model_dump(), synchronize_session=False)
    # post.model_dump() not is not working becuase .update() requires differnt kind of dictionary.

    post_query.update(
        {
            models.Post.title: post.title,
            models.Post.content: post.content,
            models.Post.published: post.published
        },
        synchronize_session=False
    )
    db.commit()


    return {"message": post_query.first()}


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def user_create(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hashing password = user.password
    hashed_password = utlils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())  # converted data from json into dict.
    db.add(new_user)  # to add data in database.
    db.commit()  # to commit changes.
    db.refresh(new_user)

    # return {"data": new_post}
    return new_user

@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found.")

    return user
