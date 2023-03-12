import logging
from pymongo import MongoClient
from config import MONGODB_URL


# MongoDB
class MongoDB:
    client: MongoClient = None # type: ignore


db = MongoDB()


async def get_nosql_db() -> MongoClient:
    '''It returns a MongoClient object

    Returns
    -------
      A MongoClient object.

    '''
    return db.client


async def connect_to_mongo():
    '''It connects to MongoDB

    '''
    db.client = MongoClient(str(MONGODB_URL))
    logging.info("connected to mongodb")


async def close_mongo_connection():
    '''> It closes the connection to the MongoDB database

    '''
    db.client.close()
    logging.info("closed mongo connection")
