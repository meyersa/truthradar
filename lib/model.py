from lib.types import Result
import logging
import requests
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_API = os.getenv("MODEL_API")
MODEL_API_KEY = os.getenv("MODEL_API_KEY")

if not MODEL_API:
    raise ValueError("Cannot be missing Model API Env")

def predict(res: Result) -> Result | None:
    """
    Sends a text input to the Model API and attaches the predictions to a Result.

    :param res: Result object containing at least an 'id' and 'content'.
    :return: Updated Result with 'predictions' field populated, or None if prediction failed.
    """
    try:
        logging.info(f"Starting prediction for result ID: {res.id}")

        # Ensure MODEL_API starts with http/https
        if not MODEL_API.startswith("http"):
            url = f"http://{MODEL_API}/predict"
        else:
            url = f"{MODEL_API.rstrip('/')}/predict"

        payload = {
            "text": res.content
        }

        headers = {
            "Content-Type": "application/json"
        }

        if MODEL_API_KEY:
            headers["X-API-Key"] = MODEL_API_KEY

        logging.debug(f"Sending request to {url} with payload: {payload}")

        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code != 200:
            logging.error(f"Prediction API call failed. Status: {response.status_code}, Response: {response.text}")
            return None

        predictions = response.json().get("predictions")

        if not predictions: 
            logging.error(f"Prediction API call failed. Empty predictions")
            return None

        # Attach predictions to Result
        res.predictions.extend(predictions)
        logging.info(f"Prediction successful for {res.id}: {predictions}")

        return res

    except Exception as e:
        logging.exception(f"Prediction failed for {res.id}: {e}")
        return None
