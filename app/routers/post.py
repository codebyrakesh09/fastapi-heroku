from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schemas, oauthn2
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=['posts'])

@router.get("/", response_model=List[schemas.PostBase])
def get_posts(db: Session = Depends(get_db), 
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):
    # print(db)

    posts = (
                db.query(models.Post)
                .filter(models.Post.title.contains(search))
                .limit(limit)
                .offset(skip)
                .all()
            )
 # ORM

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    print(results)
    
    
    # print(posts)  # will return sql query

    # return {"status": posts}
    return posts
    # return results


@router.get("/{id}")
def get_one_db_post(id: int, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauthn2.get_current_user)):
    # cursor.execute(""" SELECT * FROM products WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f" post id: {id} not found!")
 
    # print(test_post)
    # return {"post_detail": post}
    return post


# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):

#     new_post = models.Post(**post.model_dump())
#     db.add(new_post)  # to add data in database
#     db.commit()  # to commit changes
#     db.refresh(new_post)

#     # return {"data": new_post}
#     return new_post

@router.post("/", status_code=status.HTTP_201_CREATED) 
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauthn2.get_current_user)):

    print(current_user.email)
    print(current_user.id)

    # new_post = models.Post(**post.model_dump())
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)  # to add data in database
    db.commit()  # to commit changes
    db.refresh(new_post)

    # return {"data": new_post}
    return new_post

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauthn2.get_current_user)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    print(deleted_post)

    deleted_post_first = deleted_post.first()

    if deleted_post_first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found!")

    # if deleted_post_first.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/update/{id}")
def update_post(id: int, post: schemas.PostCreate, 
                db: Session = Depends(get_db),
                current_user: int = Depends(oauthn2.get_current_user)):
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


