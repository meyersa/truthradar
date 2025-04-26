import logging
import html
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from lib.types import Result


def clean_input(content: str) -> str | None:
    """
    Cleans the input string by:
    - Stripping leading/trailing spaces
    - Escaping HTML characters
    - Limiting length to 1000 characters
    - Removing unwanted special characters

    :param content: The input string to be cleaned.
    :returns: Cleaned string if successful, else None.
    """
    logging.debug("Cleaning input")

    try:
        if not content:
            raise ValueError("Empty input")

        content = str(content).strip()
        content = html.escape(content)
        content = content[:1000]
        content = re.sub(r'[^\w\s.:/-]', '', content)

    except Exception as e:
        logging.error(f"Unable to clean input:\n{e}")
        return None

    logging.info(f"Cleaned input with length: {len(content)}")
    logging.debug(f"Full cleaned content:", content)
    return content


def is_url(content: str) -> bool:
    """
    Checks if the given string is a valid URL.

    :param content: The string to check.
    :returns: True if the string is a valid URL, otherwise False.
    """
    logging.debug(f"Checking content for Url")

    parsed_url = urlparse(content)
    full_url = all([parsed_url.scheme, parsed_url.netloc])

    url_p = "is" if full_url else "is not"
    logging.info(f"Input {url_p} a URL")
    return full_url


def parse_site(url: str) -> str | None:
    """
    Downloads and parses a website from the given URL.
    Extracts visible text content and cleans it.

    :param url: The URL of the website to parse.
    :returns: Cleaned extracted text if successful, else None.
    """
    logging.info(f"Starting parse for site: {url}")

    res = None
    try:
        logging.debug(f"Downloading site: {url}")
        res = requests.get(url, headers={
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"})
        if not res.ok:
            logging.warn(f"Failed to get website:\n{res.content}")
            raise ValueError("Unable to download")

        logging.debug(f"Downloaded site: {url}")

    except Exception as e:
        logging.error(f"Unable to download website:\n{e}")
        return None

    content = None
    try:
        logging.debug(f"Parsing site: {url}")
        soup = BeautifulSoup(res.text, "html.parser")
        content = soup.get_text()

        if not content or len(content) < 10:
            raise ValueError("Unable to parse text from site")

        logging.debug(f"Parsed site for {len(content)} chars")

    except Exception as e:
        logging.error(f"Unable to parse website:\n{e}")
        return None

    cleaned_content = clean_input(content)
    logging.info(f"Parsed website for final char of {len(cleaned_content)}")
    return cleaned_content


def get_input(inResult: Result) -> Result | None:
    """
    Processes the given input by:
    - Cleaning the input
    - If it's a valid URL, downloads and parses the website content

    :param content: The input result to process.
    :returns: Filled in result
    """
    if not inResult or type(inResult) is not Result:
        logging.warning("Input was not a result")
        return None

    cleaned = clean_input(inResult.input)
    if not cleaned:
        logging.warning("Input cleaning failed or resulted in empty content.")
        return None

    if is_url(cleaned):
        inResult.link = cleaned
        parsed = parse_site(cleaned)

        if not parsed:
            logging.warning("URL parsing failed.")
            return None

        # This is the new content to return
        cleaned = parsed

    # Assign and return
    inResult.content = cleaned
    return inResult
