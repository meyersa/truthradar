from flask import Flask, render_template, request, jsonify
import logging
import sys
import os
from dotenv import load_dotenv
from lib.helpers import get_result_cached, create_result, get_recent_cached

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
    recent_items = get_recent_cached()
    p_items = []
    for item in recent_items: 
        avg_score = round(sum([prediction.get("score") for prediction in item.predictions]) / len(item.predictions) * 100)

        p_items.append({"score": avg_score, "title": item.title, "id": item.id })

    return render_template("index.html", recent=p_items)


@app.route("/result")
def result():
    """
    Shows the result of a check
    """
    id = request.args.get('id')
    res = get_result_cached(id)

    if not res:
        return render_template("404.html", back=True)

    # calculate average score
    if res.predictions and res.predictions:
        scores = [pred['score'] for pred in res.predictions]
        durations = [pred['duration_ms'] for pred in res.predictions]
        avg_score = round(sum(scores) / len(scores) * 100, 1)  # 0-100 scale
        max_duration_ms = round(max(durations) * 1.1, 1)  # 10% padding
    else:
        avg_score = 0
        max_duration_ms = 100  # default

    return render_template(
        "result.html",
        result=res,
        avg_score=avg_score,
        max_duration_ms=max_duration_ms,
        back=True
    )

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
    app.run(debug=True)
