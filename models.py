from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field

class BaseUrl(BaseModel):
    long_url: str
    short_url: str
    shortname: str
        

class UrlInDB(BaseModel):
    _id: ObjectId = ObjectId()
    long_url: str =''
    short_url: str= ''
    shortname: str =''
    def __setitem__(self, key, value):
        self.__dict__[key] = value
    def to_dict(self):
        return self.__dict__


class BaseUser(BaseModel):
    username : str
    password : str

class User(BaseModel):
    username: str
    hashed_password: str
    salt: str
    disabled: bool = False
    urls: Optional[List[UrlInDB]]
    def __getitem__(self, key):
        return self.__dict__[key]


class UserInDB(User):
    _id: ObjectId = ObjectId()

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None