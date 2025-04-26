import logging 
import openai
from lib.types import Result
import time
import json 

def fill_gpt(res: Result) -> Result | None:
    """
    Fill information in a Result object using ChatGPT.

    :param res: The Result object to fill.
    :type res: Result
    :return: Updated Result object if successful, otherwise None.
    :rtype: Result | None
    """
    logging.info(f"Filling {res.id} with ChatGPT")

    start = time.perf_counter()
    [score, reason, title] = query(res.content)
    duration_ms = (time.perf_counter() - start) * 1000  # milliseconds

    if not verify_score(score):
        logging.warning(f"Unable to verify the score from the model:\n{score}")
        return None
    
    if not verify_reason(reason):
        logging.warning(f"Unable to verify the reason from the model:\n{reason}")
        return None    
    
    if not verify_title(title):
        logging.warning(f"Unable to verify the title from the model:\n{title}")
        return None
    
    res.title = title 
    res.reason = reason 
    res.predictions = dict({"name": "ChatGPT3.5Turbo", "score": score, "duration_ms": duration_ms})

    logging.info("Returning result with summarization")
    return res

def verify_title(title: str) -> bool:
    """
    Verify that the title is a string within allowed length.

    :param title: Title to verify.
    :type title: str
    :return: True if valid, False otherwise.
    :rtype: bool
    """
    if type(title) is not str:
        return False

    return 5 <= len(title) <= 50

def verify_score(score: float) -> bool:
    """
    Verify that the score is a float between 0.0 and 1.0.

    :param score: Score to verify.
    :type score: float
    :return: True if valid, False otherwise.
    :rtype: bool
    """
    if type(score) not in (float, int):
        return False

    return 0.0 <= score <= 1.0

def verify_reason(reason: str) -> bool:
    """
    Verify that the reason is a string with reasonable length.

    :param reason: Reason to verify.
    :type reason: str
    :return: True if valid, False otherwise.
    :rtype: bool
    """
    if type(reason) is not str:
        return False

    return 0 < len(reason) <= 750

def query(content: str) -> list[float, str, str]:
    """
    Query ChatGPT to generate a score, reason, and title based on content.

    :param content: The content to analyze.
    :type content: str
    :return: [score (float), reason (str), title (str)]
    :rtype: list[float, str, str]
    """
    logging.info(f"Summarizing from ChatGPT")

    prompt = f"""
    You are a fair and impartial content moderator. Given the following content, assess its truthfulness and provide:

    - score: a FLOAT from 0.0 to 1.0, where:
        - 0.0 means completely true
        - 0.01-0.32 suggests likely true
        - 0.33-0.66 indicates uncertainty or mixed truth
        - 0.67-0.99 suggests likely false
        - 1.0 means completely false

    - reason: a concise explanation (under 750 characters) of why you gave that score.

    - title: a short summary title (5-50 characters) covering the key idea(s) of the content.

    Respond ONLY in JSON format like: {{"score": float, "reason": string, "title": string}}.

    Content:
    {content}
    """

    response = openai.responses.create(
        model="gpt-3.5-turbo",
        input=prompt
    )

    logging.debug(f"Received response back from ChatGPT: {response.output_text}")
    data = json.loads(response.output_text)
    return [data['score'], data['reason'], data['title']]
