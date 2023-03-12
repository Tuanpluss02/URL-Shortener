import logging
from typing import Optional
import pymongo
import json
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from mongodb import close_mongo_connection, connect_to_mongo, get_nosql_db
from config import MONGODB_NAME, BASE_SHORT_URL,MONGODB_URL


app = FastAPI()
mongo_client = pymongo.MongoClient(MONGODB_URL)
db = mongo_client[MONGODB_NAME]
url_collection = db["url_collection"]

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:3000",
#     "http://localhost:3000",
# ]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# async def startup_event():
#     await connect_to_mongo()
#     client = await get_nosql_db()
#     db = client[MONGODB_NAME]
#     if "url_collection" not in db.list_collection_names():
#         try:
#             db.create_collection("url_collection")
#         except pymongo.error.CollectionInvalid as error:
#             logging.warning(error)
#     try:
#         url_collection = db.url_collection
#         url_collection.create_index(
#             "shortname", shortname="shortname", unique=True)
#     except pymongo.error.CollectionInvalid as error:
#         logging.warning(error)


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


@app.get("/")
async def root():
    "Root endpoint"
    return RedirectResponse(url="http://127.0.0.1:8000/docs")
    # return RedirectResponse(url="https://stormx.software")



@app.post("/shorten")
async def shorten_url(long_url: str, short_name: str):
    if not long_url.startswith(("http://", "https://")):
        long_url = "http://" + long_url

    if not all(c.isalnum() or c == "-" for c in short_name):
        raise HTTPException(status_code=400, detail="Short name can only contain letters and numbers")

    short_url = BASE_SHORT_URL + short_name

    if url_collection.find_one({"shortname": short_name}):
        raise HTTPException(status_code=409, detail="Short name already exists")

    try:
        result = url_collection.insert_one({"shortname": short_name,"short_url" : short_url, "long_url": long_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to insert the record into the database")

    return {"short_url": short_url}
    

@app.get("/{short_name}")
async def redirect_to_long_url(short_name: str, response: Response):
    url_doc = url_collection.find_one({"shortname": short_name})

    if url_doc is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    long_url = url_doc["long_url"]
    return RedirectResponse(url=long_url)


@app.patch("/edit-url")
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


@app.delete("/delete-url")
async def delete_url(short_name: Optional[str] = None, short_url: Optional[str] = None):
    if short_name is None and short_url is None:
        raise HTTPException(status_code=400, detail="Either short_name or short_url must be provided")

    if short_name is not None:
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
