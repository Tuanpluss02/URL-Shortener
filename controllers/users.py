import bcrypt
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from config import ALGORITHM, SECRET_KEY
from models import TokenData, UrlInDB, User, UserInDB
from jose import JWTError, jwt
from passlib.context import CryptContext
from mongodb import get_mongo_user_collection
import logging

from ultils import format_ids

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password_w_salt, hashed_password):
    return pwd_context.verify(plain_password_w_salt, str(hashed_password), scheme="bcrypt")


def get_password_hash(password_w_salt):
    return pwd_context.hash(password_w_salt)    


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password + user["salt"], user["hashed_password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def create_user(request, collection):
    salt = bcrypt.gensalt().decode()
    hashed_password = get_password_hash(request.password + salt)
    user = {}
    user["username"] = request.username
    user["salt"] = salt
    user["hashed_password"] = hashed_password
    user["urls"] = []
    dbuser = UserInDB(**user)
    try:
        response = collection.insert_one(dict(dbuser))
        return {"id_inserted": str(response.inserted_id)}
    except Exception as e:
        raise Exception(f"{e}")


async def get_user(name):
    users_collection = await get_mongo_user_collection()
    row = users_collection.find_one({"username": name})
    if row is not None:
        row = format_ids(row)
        return row
    else:
        return None

