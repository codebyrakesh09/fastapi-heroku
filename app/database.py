from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:rakesh@2002@localhost/fastapi'

# SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:rakesh%402002@localhost/postgres'
# you should not hardcode this here it exposes sensitive info!

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # Connecting Database
# while True: 

#     try:
#         con = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="rakesh@2002", cursor_factory=RealDictCursor)
#         cursor = con.cursor()
#         print("database connected successfully.")
#         break

#     except Exception as error:
#         print("Oops! database not connected.")
#         print("Error:", error)
#         time.sleep(2)

 