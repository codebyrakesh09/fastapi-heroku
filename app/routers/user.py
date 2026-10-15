from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schemas, utlils

router = APIRouter(prefix="/users", tags=['users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
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

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found.")

    return user
