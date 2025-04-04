from lib.types import Result
import logging
import openai
import json
from dotenv import load_dotenv

load_dotenv()

def test(res: Result) -> Result | None:
    """
    Get the result about truth from a model
    """
    logging.info(f"Getting result for {res.id}")

    [result, reason] = query(res.content)

    result = int(result) 
    reason = str(reason) 

    if not verify_result(result):
        logging.warn(f"Unable to verify the result from the model:\n{result}")
        return None
    
    if not verify_reason(reason): 
        logging.warn(f"Unable to verify the reason from the model:\n{reason}")
        return None

    logging.info("Returning result with summarization")

    res.result = result
    res.reason = reason
    return res


def verify_result(result: int) -> bool:
    """
    Verify an inputted result to be within spec 
    """
    if type(result) is not int:
        return False

    return 0 <= result <= 100


def verify_reason(reason: str) -> bool:
    """
    Verify an inputted reason is within spec
    """
    if type(reason) is not str:
        return False

    return 0 < len(reason) < 1000


def query(content: str) -> list[int, str]:
    """
    Query ChatGPT to assign a result score and reason to the given result
    """
    logging.info(f"Summarizing from ChatGPT")

    prompt = f"""
    You are a content moderator. Your job is to be as fair as possible. Given the following content, provide:

    - result: an integer score between 0 (the **truth**) to 100 (definitely **fake**)
    - reason: a short explanation, less than 750 characters

    Respond ONLY in JSON format like: {{"result": int, "reason": string}}.

    Content:
    {content}
    """
    response = openai.responses.create(
        model="gpt-3.5-turbo",
        input=prompt
    )

    logging.debug(f"Received response back from ChatGPT", response.output_text)
    data = json.loads(response.output_text)
    return [data['result'], data['reason']]
