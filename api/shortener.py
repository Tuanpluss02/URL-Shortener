import logging
from typing import Optional
from bson import ObjectId
import pymongo
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from config import MONGODB_NAME, MONGODB_URL
from controllers.shortener import add_new_url_to_user, check_valid_request, get_urls_from_user, push_url_to_public_db, remove_url, update_url
from controllers.users import get_current_active_user, get_user_ins
from models import BaseUrl, User
from validate import is_valid_shortname, is_valid_url

router = APIRouter()
logger = logging.getLogger(__name__)
mongo_client = pymongo.MongoClient(MONGODB_URL)
db = mongo_client[MONGODB_NAME]
url_collection = db["url_collection"]


@router.post("/shorten")
async def shorten_url(long_url: str, short_name: str, current_user: User = Depends(get_current_active_user)):
    short_url = await check_valid_request(long_url, short_name)
    url_request = BaseUrl(shortname=short_name,
                          short_url=str(short_url), long_url=long_url)
    url_in_db = await push_url_to_public_db(url_request)
    user_db = await get_user_ins(current_user['username'])
    if url_in_db is not None:
        try:
            await add_new_url_to_user(user_db, url_in_db)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(status_code=200, content={"messages": "success", "short_url": short_url})


@router.get("/{short_name}")
async def redirect_to_long_url(short_name: str):
    url_doc = url_collection.find_one({"shortname": short_name})
    if url_doc is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    long_url = url_doc["long_url"]
    return RedirectResponse(url=long_url)


@router.patch("/user/edit-url")
async def edit_url(shortname: str, new_shortname: str,  new_long_url: str, current_user: User = Depends(get_current_active_user)):
    result = await update_url(shortname, new_shortname, new_long_url, current_user['username'])
    return {"message": "success", "shortname": result.shortname, "short_url": result.short_url, "long_url": result.long_url}


@router.delete("/user/delete-url")
async def delete_url(short_name: str, current_user: User = Depends(get_current_active_user)):
    if short_name is None:
        raise HTTPException(
            status_code=400, detail="Short name must be provided")
    await remove_url(short_name, current_user['username'])
    return {"message": "Short URL deleted successfully"}


@router.get("/user/get_urls")
async def get_urls(current_user: User = Depends(get_current_active_user)):
    urls = await get_urls_from_user(current_user)
    urls.reverse()
    return {"urls": urls}
