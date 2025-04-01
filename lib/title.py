from lib.types import Result
from openai import OpenAI
import logging
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
CLIENT = OpenAI()


def summarize(content: str) -> str:
    """
    Given a content string, summarize the data into a title
    """
    logging.info("Querying ChatGPT for a title")

    prompt = f"""
    Please summarize the following content for a title. 
    - It should cover the key idea(s) of the content
    - It should be between 5 and 50 characters

    Content:
    {content}
    """
    response = CLIENT.responses.create(
        model="gpt-3.5-turbo",
        input=prompt
    )

    logging.info(
        f"Queried ChatGPT and received a response of length {len(response.output_text)}")
    return response.output_text


def download(url: str) -> str | None:
    """
    Given a URL, download the page and get the title
    """
    logging.info(f"Downloading website title from {url}")

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        if not soup.title:
            raise ValueError("No title found on page")

        logging.info(f"Found page title {soup.title.string}")
        return soup.title.string

    except:
        logging.warn(f"Unable to get title from {url}")
        return None


def get_title(res: Result) -> Result | None:
    """
    Gets a title for a result either from the URL or ChatGPT summarization
    """
    logging.info(f"Filling the title for {res.id}")

    title = None
    if res.link:
        logging.debug("Found URL, using that to get the title")
        title = download(res.link)

    if not title:
        logging.debug("Trying to summarize title with ChatGPT")
        title = summarize(res.content)

    if not title:
        logging.warn("No title found, defaulting")
        title = "User Input"

    logging.info(f"Filled title for {res.id} with {title}")
    res.title = title
    return res
