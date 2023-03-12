import logging
import pymongo
import json
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from mongodb import close_mongo_connection, connect_to_mongo, get_nosql_db
from config import MONGODB_NAME, BASE_SHORT_URL


app = FastAPI()

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


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    client = await get_nosql_db()
    db = client[MONGODB_NAME]
    if "url_collection" not in db.list_collection_names():
        try:
            db.create_collection("url_collection")
        except pymongo.errors.CollectionInvalid as error:
            logging.warning(error)
    try:
        url_collection = db.url_collection
        url_collection.create_index(
            "shortname", shortname="shortname", unique=True)
    except pymongo.errors.CollectionInvalid as error:
        logging.warning(error)


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


@app.get("/")
async def root():
    "Root endpoint"
    return RedirectResponse(url="https://stormx.software")


@app.post("/shorten")
async def shorten_url(long_url: str, short_name: str):
    short_url = BASE_SHORT_URL + short_name
    db = await get_nosql_db()
    url_collection = db.url_collection
    url = await url_collection.find_one({"shortname": short_name})
