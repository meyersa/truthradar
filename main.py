from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging
from lib.model import test
from lib.parsing import get_input
from lib.title import get_title
from lib.types import Result
import sys
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

RESULTS = list()


def create_result(input: str) -> Result:
    """
    Creates a result 
    """
    id = hash_text(input)

    logging.info(f"Creating result: {id}")

    res = get_input(res)
    res = get_title(res)
    res = test(res)
    save_result(res)

    return Result(id=id, input=input)


def save_result(res: Result) -> bool:
    """
    Save a result by adding it to the results list
    """
    logging.info(f"Saving result: {res.id}")

    for result in RESULTS:
        if result.id == res.id:
            logging.info(f"Not saving {res.id}, duplicate found")
            return False

    RESULTS.append(res)
    logging.info(f"Saved result: {res.id}")
    return True


def get_result(id: int) -> Result | None:
    """
    Locate a result from the ID
    """
    logging.info(f"Looking for ID: {id}")

    for result in RESULTS:
        if result.id == id:
            logging.info(f"Returning ID: {id}")
            return result

    logging.info(f"Unable to find result: {id}")
    return None


def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

# Home route


@app.route("/")
def home():
    return render_template("index.html")

# Loading page


@app.route("/loading")
def loading():
    return render_template("loading.html")

# Result page


@app.route("/result")
def result():
    id = request.args.get('id')
    res = get_result(id)

    if not res:
        return render_template("404.html")

    return render_template("result.html", result=get_result(id))

# Submission route


@app.route('/api/check', methods=['POST'])
def check():
    data = request.get_json()
    input_text = data.get('text', '')
    api_key = data.get('key', '')

    logging.info(f"Received a request with key: {api_key}")
    if api_key != API_KEY:
        return jsonify({"Error": "No access"})

    create_result(input_text)

    logging.info(f"Returning ID: {id}")
    return jsonify({'id': id})


if __name__ == "__main__":
    from datetime import datetime
    print(save_result(Result(id="12345", input="this is a test", link="https://google.com", content="this is also a test", title="Testing Result", result=50,
      reason="Fugiat nulla quis culpa magna ullamco et et ut nostrud. Lorem pariatur mollit ipsum et labore mollit qui fugiat commodo ad. Do qui elit id esse qui veniam pariatur ullamco esse.")))
    app.run(debug=True)
