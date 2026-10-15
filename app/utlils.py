from passlib.context import CryptContext

# it basically tells which actual password-hashing algorithm we are using (bcrypt).
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):
    return pwd_content.hash(password)

def verify(user_password, hashed_password):
    return pwd_content.verify(user_password, hashed_password)