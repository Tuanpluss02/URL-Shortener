import logging
from typing import Optional
from bson import ObjectId
import pymongo
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from config import MONGODB_NAME, BASE_SHORT_URL,MONGODB_URL
from validate import is_valid_url
from api import router as api_router


app = FastAPI()
mongo_client = pymongo.MongoClient(MONGODB_URL)



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# async def startup_event():
    # await connect_to_mongo()
    # db = mongo_client[MONGODB_NAME]
    # if "url_collection" not in db.list_collection_names():
    #     try:
    #         db.create_collection("url_collection")
    #     except pymongo.error.CollectionInvalid as error: # type: ignore
    #         logging.warning(error)
    # if "user_collection" not in db.list_collection_names():
    #     try:
    #         db.create_collection("user_collection")
    #     except pymongo.error.CollectionInvalid as error: # type: ignore
    #         logging.warning(error)
    # try:
    #     user_collection = db.user_collection
    #     user_collection.create_index(
    #         "username", username="username", unique=True)
    # except: # type: ignore
    #     logging.warning("user_collection already exists")


    # try:
    #     url_collection = db.url_collection
    #     url_collection.create_index(
    #         "shortname", shortname="shortname", unique=True)
    # except pymongo.error.CollectionInvalid as error: # type: ignore
    #     logging.warning(error)


@app.on_event("shutdown")
async def shutdown_event():
    try:
        mongo_client.close()
        logging.info("Closed mongo connection")
    except Exception as e:
        logging.warning(e)
    

app.include_router(api_router)
