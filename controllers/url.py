import logging
import pymongo
from models import UrlInDB, UserInDB
from mongodb import get_mongo_client, get_mongo_user_collection


async def add_new_url_to_user(user: UserInDB, url: UrlInDB):
    if user.urls:
        user.urls.append(url)
    else:
        user.urls = [url]
    try:
        client = await get_mongo_client()
        user_collection = client.user_collection
        user_collection.update_one({"_id": user._id}, {"urls": user.urls})
        
    except:
        logging.warning("Failed to add new url to user")
        return False
   
        
    