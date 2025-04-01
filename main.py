from flask import Flask, render_template, request, redirect, url_for, jsonify

test_result = {
    "id": 12345,
    "result": "Fake",
    "title": "Is this website working?",
    "link": "https://truthradar.meyersa.com/",
    "score": 42,
    "reason": "Labore sint fugiat tempor irure sunt id adipisicing amet amet. Sit id eu sint Lorem duis magna officia ad ea veniam magna. Magna duis ut Lorem sint sint velit laborum laborum id. Proident cupidatat consectetur ipsum aliquip eu excepteur. Anim et cupidatat tempor incididunt et."
}

app = Flask(__name__)

@app.route("/")
def home(): 
    return render_template("index.html")

@app.route("/loading")
def loading(): 
    return render_template("loading.html")

@app.route("/result")
def result(): 
    id = request.args.get('id')
    return render_template("result.html", result=test_result)

@app.route('/api/check', methods=['POST'])
def check():
    data = request.get_json()
    input_text = data.get('text', '')

    print(input_text)
    
    return jsonify({'result': f'Received: {input_text}'})

if __name__ == "__main__":
    app.run(debug=True)