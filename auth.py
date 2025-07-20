# import jwt
# from passlib.hash import bcrypt
# from datetime import datetime, timedelta
# import os
# from dotenv import load_dotenv

# load_dotenv()
# SECRET_KEY = os.getenv("SECRET_KEY")

# # SECRET_KEY = "YOUR_SECRET_KEY"  # Replace with env var in production

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(days=1)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# def verify_password(plain_password, hashed_password):
#     return bcrypt.verify(plain_password, hashed_password)

# def hash_password(password):
#     return bcrypt.hash(password)

# def decode_token(token: str):
#     return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# Create a cryptographic context for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
def verify_password(plain_password, hashed_password):
    # TEMP: disable real password check
    return True

def hash_password(password):
    return pwd_context.hash(password)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
