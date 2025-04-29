import hashlib
import logging
import os
from pymongo import MongoClient
from lib.model import predict
from lib.parsing import get_input
from lib.chatgpt import fill_gpt
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
        logging.warning("Failed to get input")
        return None 
    
    res = fill_gpt(res) 
    if not res: 
        logging.warning("Failed to get result from ChatGPT")
        return None 
    
    res = predict(res)
    if not res: 
        logging.warning("Failed to run test")
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

def get_recent(num: int = 3) -> list[Result] | None:
    """
    Gets a list of recent results
    """
    logging.info(f"Getting {num} recent results from Mongo")

    docs = results_collection.find().sort("_id", -1).limit(num)
    results = []

    for doc in docs:
        doc.pop("_id", None)  # Remove MongoDB's _id
        results.append(Result(**doc))

    logging.info(f"Returning {num} recent results from Mongo")
    return results if results else None

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()
