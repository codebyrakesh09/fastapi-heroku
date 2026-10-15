from .database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):  # sqlalchemy model (database structure in postgresql database.)
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # setting a foreign key.
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
   
# class Products(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     price = Column(String, nullable=False)
#     is_sale = Column(Boolean, nullable=False)
#     inventory = Column(Integer, server_default='False', nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

   


 