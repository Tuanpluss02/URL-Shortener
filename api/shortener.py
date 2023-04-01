import logging
from typing import Optional
from bson import ObjectId
import pymongo
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from config import MONGODB_NAME, BASE_SHORT_URL,MONGODB_URL
from controllers.shortener import add_new_url_to_user, check_valid_request, push_url_to_public_db
from controllers.users import get_current_active_user, get_user, get_user_ins
from models import BaseUrl, User

router = APIRouter()
logger = logging.getLogger(__name__)
mongo_client = pymongo.MongoClient(MONGODB_URL)
db = mongo_client[MONGODB_NAME]
url_collection = db["url_collection"]


# @router.post("/shorten" )
# async def shorten_url(long_url: str, short_name: str):
#     if short_name == "shorten":
#         raise HTTPException(status_code=400, detail="Short name cannot be \'shorten\'")
#     if not is_valid_url(long_url):
#         raise HTTPException(status_code=400, detail="Invalid URL")
#     if not all(c.isalnum() or c == "-" for c in short_name):
#         raise HTTPException(status_code=400, detail="Short name can only contain letters and numbers")
#     short_url = BASE_SHORT_URL + short_name

#     if url_collection.find_one({"shortname": short_name}):
#         return JSONResponse(status_code=202, content= {"detail" : "Short name already exists"})
#     try:
#         result = url_collection.insert_one({"shortname": short_name,"short_url" : short_url, "long_url": long_url})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#     if not result.acknowledged:
#         raise HTTPException(status_code=500, detail="Failed to insert the record into the database")

#     return JSONResponse(status_code=200,content= {"messages" : "success", "short_url": short_url})

@router.post("/shorten" )
async def shorten_url(long_url: str, short_name: str,current_user: User = Depends(get_current_active_user)):
    short_url = await check_valid_request(long_url, short_name)
    url_request = BaseUrl(shortname=short_name,short_url=str(short_url), long_url=long_url)
    url_in_db = await push_url_to_public_db(url_request)
    user_db = await get_user_ins(current_user['username'])
    if url_in_db is not None:
        try:
            await add_new_url_to_user(user_db,url_in_db)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(status_code=200,content= {"messages" : "success", "short_url": short_url})
    

@router.get("/{short_name}" )
async def redirect_to_long_url(short_name: str):
    url_doc = url_collection.find_one({"shortname": short_name})

    if url_doc is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    long_url = url_doc["long_url"]
    return RedirectResponse(url=long_url)


@router.patch("/admin/edit-url" )
async def edit_url(short_name: Optional[str] = None, short_url: Optional[str] = None, long_url: str = None): # type: ignore
    if long_url is None:
        raise HTTPException(status_code=400, detail="Long URL must be provided")
    if short_name is None and short_url is None:
        raise HTTPException(status_code=400, detail="Either short_name or short_url must be provided")

    if short_name is not None:
        filter = {"shortname": short_name}
    else:
        if not str(short_url).startswith(BASE_SHORT_URL):
            raise HTTPException(status_code=400, detail="Short URL must start with " + BASE_SHORT_URL)

        short_name = str(short_url)[len(BASE_SHORT_URL):]
        filter = {"shortname": short_name}

    url_doc = url_collection.find_one(filter)

    if url_doc is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    result = url_collection.update_one(filter, {"$set": {"long_url": long_url}})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Failed to update the record")

    return {"short_url": BASE_SHORT_URL + short_name, "long_url": long_url}


@router.delete("/admin/delete-url" )
async def delete_url(short_name: Optional[str] = None, short_url: Optional[str] = None, id : Optional[str] = None):
    if short_name is None and short_url is None and id is None:
        raise HTTPException(status_code=400, detail="Either id or short_name or short_url must be provided")

    if id is not None:
        filter = {"_id": ObjectId(id)}
    elif short_name is not None:
        filter = {"shortname": short_name}
    else:
        if not str(short_url).startswith(BASE_SHORT_URL):
            raise HTTPException(status_code=400, detail="Short URL must start with " + BASE_SHORT_URL)

        short_name = str(short_url)[len(BASE_SHORT_URL):]
        filter = {"shortname": short_name}

    result = url_collection.delete_one(filter)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {"message": "Short URL deleted successfully"}

@router.get("/admin/get_urls" )
async def get_urls():
    urls = []
    get_all_urls = url_collection.find()
    for url in get_all_urls:
        urls.append({"id": str(url['_id']) ,"short_url": url['short_url'], "long_url": url["long_url"]})
    return {"urls": urls}
