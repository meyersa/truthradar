# Truth Radar 

Fact checking powered by machine learning. Paste a link or text and Truth Radar will advise on the truthality of the content. 

## Installation 

> pip install -r requirements 

## Running 

> python -m main.py 

## Testing 

> python -m unittest discover -s tests

## ENVs 

- `OPENAI_API_KEY`: OpenAI key for ChatGPT queries 
- `API_KEY`: To restrict usage of site
- `MONGO_DB`: MongoDB to connect to
- `MONGO_URL`: MongoDB URL to use to connect with
- `MODEL_API`: Model API Server to use for querying
- `MODEL_API_KEY`: Key for Model API Server to use