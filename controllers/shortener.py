import logging
from typing import Any, Dict, Union
from bson import ObjectId
from fastapi import HTTPException
from config import BASE_SHORT_URL
from models import BaseUrl, UrlInDB, User, UserInDB
from mongodb import  get_mongo_url_collection, get_mongo_user_collection
from validate import is_valid_url

async def add_new_url_to_user(user: Union[UserInDB, Dict[str, Any]], url: UrlInDB):
    if isinstance(user, dict):
        user = UserInDB(**user)
    try:
        user_collection = await get_mongo_user_collection()
        url_push = url.to_dict()
        update = {"$push": {"urls": url_push}}
        user_collection.update_one({"username": user.username}, update)
        mongo_response = user_collection.find_one({"username": user.username})
        if(mongo_response is None):
            raise HTTPException(status_code=500, detail="Failed to add new url to user")
        user_updated = mongo_response.copy()  
        user_updated['_id'] = str(mongo_response['_id']) 
        user_updated = UrlInDB(**user_updated)
    except:
        raise HTTPException(status_code=500, detail="Failed to add new url to user")

    
async def check_valid_request(long_url: str, shortname: str) -> str:
    if shortname == "shorten":
        raise HTTPException(status_code=400, detail="Short name cannot be \'shorten\'")
    if not is_valid_url(long_url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    if not all(c.isalnum() or c == "-" for c in shortname):
        raise HTTPException(status_code=400, detail="Short name can only contain letters and numbers")
    url_collection = await get_mongo_url_collection()
    if url_collection.find_one({"shortname": shortname}):
        raise HTTPException(status_code=400, detail="Short name already exists")
    short_url = BASE_SHORT_URL + shortname
    return short_url

async def push_url_to_public_db(url: BaseUrl)->UrlInDB:
    url_db = UrlInDB()
    url_db["_id"] = ObjectId()
    url_db["shortname"] = url.shortname
    url_db["short_url"] = url.short_url  
    url_db["long_url"] = url.long_url
    try:
        url_collection = await get_mongo_url_collection()
        _id = url_collection.insert_one(url_db.to_dict())
        mongo_response = url_collection.find_one({"_id": ObjectId(_id.inserted_id)})
        if(mongo_response is None):
            raise Exception("Failed to add new url to public db")
        url_data_dict = mongo_response.copy() 
        url_data_dict['_id'] = str(mongo_response['_id']) 
        url_data = UrlInDB(**url_data_dict) 
        return url_data
    except:
        logging.warning("Failed to add new url to public db")
        return UrlInDB(**{})

