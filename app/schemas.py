from pydantic import BaseModel,  EmailStr, Field  # for schema
from datetime import datetime
from typing import Optional, Annotated
# from pydantic.types import conint # used in older version pydanticV1


# schemas (pydantic model)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # default value
    # rating: Optional[int] = None  # optional and default value


class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:  # allow Pydantic to create a response schema from an ORM/database object. (convert that SQLAlchemy object into the Pydantic response model.)
        from_attributes = True  


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]
