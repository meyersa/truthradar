from flask import Flask, render_template, request, jsonify
import logging
import sys
import os
from dotenv import load_dotenv
from lib.helpers import get_result, create_result

load_dotenv()
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logging.getLogger("pymongo").setLevel(logging.CRITICAL)
app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


@app.route("/")
def home():
    """
    Home page
    """
    return render_template("index.html")


@app.route("/result")
def result():
    """
    Shows the result of a check
    """
    id = request.args.get('id')
    res = get_result(id)

    if not res:
        return render_template("404.html", back=True)

    return render_template("result.html", result=get_result(id), back=True)


@app.route('/api/check', methods=['POST'])
def check():
    """
    Check on a link or block of text
    """
    data = request.get_json()
    input_text = data.get('text', '')
    api_key = data.get('key', '')

    logging.info(f"Received a request with key: {api_key}")
    if api_key != API_KEY:
        logging.info("Invalid API Key")
        return jsonify({'status': "error", 'error': "No access"})

    logging.info("Valid API Key")
    id = create_result(input_text)

    if not id:
        return jsonify({'status': "error", 'error': "Failed to create result"})

    logging.info(f"Returning ID: {id}")
    return jsonify({'id': id})


if __name__ == "__main__":
    app.run()
