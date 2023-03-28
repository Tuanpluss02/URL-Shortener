from pymongo import MongoClient
from config import MONGODB_NAME, MONGODB_URL

client = MongoClient(MONGODB_URL)


async def get_mongo_user_collection():
    return client[MONGODB_NAME].user_collection

async def get_mongo_url_collection():
    return client[MONGODB_NAME].url_collection

async def get_mongo_client() -> MongoClient:
    return MongoClient(MONGODB_URL)