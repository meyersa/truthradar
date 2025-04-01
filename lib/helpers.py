import hashlib
import logging
import os
from pymongo import MongoClient
from lib.model import test
from lib.parsing import get_input
from lib.title import get_title
from lib.types import Result
from dotenv import load_dotenv

load_dotenv() 

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URL)
db = client[MONGO_DB]
results_collection = db["results"]

def create_result(input: str) -> str:
    """
    Creates a result 
    """
    id = hash_text(input)
    logging.info(f"Creating result: {id}")
    res = Result(id=id, input=input)

    res = get_input(res)
    if not res: 
        logging.warn("Failed to get input")
        return None 
    
    res = get_title(res)
    if not res: 
        logging.warn("Failed to get title")
        return None 
    
    res = test(res)
    if not res: 
        logging.warn("Failed to run test")
        return None 
    
    logging.info(f"Result created for: {id}")
    save_result(res)
    return id

def save_result(res: Result) -> bool:
    """
    Save a result to MongoDB
    """
    logging.info(f"Saving result: {res.id}")

    if results_collection.find_one({"id": res.id}):
        logging.info(f"Not saving {res.id}, duplicate found")
        return False

    results_collection.insert_one(res.__dict__)
    logging.info(f"Saved result: {res.id}")
    return True


def get_result(id: int) -> Result | None:
    """
    Locate a result from MongoDB by ID
    """
    logging.info(f"Looking for ID: {id}")

    doc = results_collection.find_one({"id": id})
    if doc:
        doc.pop("_id", None)  # Remove MongoDB's _id
        logging.info(f"Returning ID: {id}")
        return Result(**doc)

    logging.info(f"Unable to find result: {id}")
    return None


def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()
