import logging
import pymongo
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from config import MONGODB_URL
from api import router as api_router
from starlette.exceptions import HTTPException
from starlette.templating import Jinja2Templates


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

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
css = "static/style.css"

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return templates.TemplateResponse("404.html", {"request": request,"css": css }, status_code=404)
    else:
        return exc

@app.on_event("shutdown")
async def shutdown_event():
    try:
        mongo_client.close()
        logging.info("Closed mongo connection")
    except Exception as e:
        logging.warning(e)
    

app.include_router(api_router)
