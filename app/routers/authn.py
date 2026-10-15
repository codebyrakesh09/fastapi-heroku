from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  # this only takes form data with username and password.
from .. import database, schemas, models, utlils, oauthn2

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
# def user_login(user_credential: schemas.UserLogin, db: Session = Depends(database.get_db)):
def user_login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):


    # user = db.query(models.User).filter(models.User.email == user_credential.email).first()
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    # print(user)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utlils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token...
    access_token = oauthn2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

