from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from pydantic import BaseModel  # for schema
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .import models
from .database import engine, get_db
from sqlalchemy.orm import Session

# this tells postgresql to create the model if it is not present there.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# schemas (pydantic model)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value
    # rating: Optional[int] = None  # optional and default value

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

@app.get("/")  # -> Decorator
async def root():
    return {"Message": "Hello World, changes happens"}

# @app.get("/posts")
# def get_pots():
#     return {"data": "This is your post"}

# @app.get("/posts")
# def get_pots():
#     return {"data": mydata}


# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM products""")
#     post = cursor.fetchall()
#     return {"data": post}


@app.get("/sqlalcehmy")
def test_posts(db: Session = Depends(get_db)):
    # print(db)
    posts = db.query(models.Post).all()  # ORM, using this got all posts from DB wihtout sql any query.
    print(posts)  # will return sql query

    return {"status": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # print(db)
    posts = db.query(models.Post).all()  # ORM
    # print(posts)  # will return sql query

    return {"status": posts}


# @app.get("/posts/{id}")
# def get_one_db_post(id: int):
#     cursor.execute(""" SELECT * FROM products WHERE id = %s """, (str(id),))
#     post = cursor.fetchone()
    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f" post id: {id} not found!")
        
#     # print(test_post)
#     return {"post_detail": post}

@app.get("/posts/{id}")
def get_one_db_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM products WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f" post id: {id} not found!")
        
    # print(test_post)
    return {"post_detail": post}


# @app.post("/createpost")
# def create_post(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}

# @app.post("/createpost")
# def create_post(new_post: Post):
#     print(new_post)
#     print(new_post.title + " " + new_post.content)
#     print(new_post.published)
#     print(new_post.rating)
#     # print(new_post.dict()) - > depricated in new version of pydantic
#     print(new_post.model_dump())
#     return {"new_post": new_post}

# @app.post("/createpost", status_code=status.HTTP_201_CREATED)
# def create_post(new_post: Post):
#     post_dict = new_post.model_dump()
#     post_dict['id'] = randrange(0, 1000000)
#     mydata.append(post_dict)
#     return {"new_post": post_dict}

# @app.post("/createpost", status_code=status.HTTP_201_CREATED)
# def create_post(new_post: Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))  # this is called staged changed.

#     # print(cursor.fetchone())
#     post = cursor.fetchone()
#     con.commit()

#     return {"new_post": post}

@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))  # this is called staged changed.

    # print(post.model_dump())

    # new_post = models.Post(title = post.title, content = post.content, published = post.published)

    new_post = models.Post(**post.model_dump())
    db.add(new_post)  # to add data in database
    db.commit()  # to commit changes
    db.refresh(new_post)

    return {"data": new_post}


def find_post(id):
    for data in mydata:
        if data['id'] == id:
            return data

# @app.get("/post/{id}")
# def get_post(id: int):  # now no need to take response: Response
#     # print(id)
#     post = find_post(id)
#     if not post:
#         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f" post id: {id} not found!")

#         # response.status_code = 404
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"data": f" post id: {id} not found!"}

#     return {"data": post}
#     # return {"data": f"this is post {id}"}

def find_index_post(id):
    for i, data in enumerate(mydata):
        if data['id'] == id:
            return i

# @app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     # we will find id... 
#     # then delete it from the list using .pop()
#     post = find_index_post(id)
#     # print(type(post))

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found!")

#     mydata.pop(post)
#     # return {"message":f"id: {post} is deleted successfully."}
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
#     deleted_post = cursor.fetchone()
#     con.commit()

#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found!")

#     return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # con.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    print(deleted_post)

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found!")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/post/{id}")
# def update_post(id: int, post: Post):
#     # print(post)
#     # print(post.title +" "+ post.content)

#     index = find_index_post(id)

#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found!")

#     post_dict = post.model_dump()  # from JSON (recive with HTTP request) to dictionary...
#     post_dict['id'] = id
#     mydata[index] = post_dict

#     return {"message": " content of the post updated."}

# @app.put("/post/{id}")
# def update_post(id: int, post: Post):
#     cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post. published, str(id)))
#     updated_post = cursor.fetchone()
#     con.commit()

#     print(cursor.fetchone())

#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found!")
    
#     return {"message": updated_post}


@app.put("/post/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
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

