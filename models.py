from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    hashed_password: str
    salt: str
    disabled: bool = False

class UrlInDB(BaseModel):
    _id: ObjectId
    long_url: str
    short_url: str
    shortname: str
    vierw_count: int = 0
    date_created: datetime = Field(default_factory=datetime.utcnow)
    def __getitem__(self, key):
        return getattr(self, key)


class BaseUser(BaseModel):
    username : str
    password : str

class UserInDB(User):
    _id: ObjectId
    date_created: datetime = Field(default_factory=datetime.utcnow)
    def __getitem__(self, key):
        return getattr(self, key)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None