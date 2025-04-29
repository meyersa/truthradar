import logging
import html
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from lib.types import Result
import os 

MAX_WEB_LENGTH = os.getenv("MAX_WEB_LENGTH", 5000)

def clean_input(content: str) -> str | None:
    """
    Cleans the input string by:
    - Stripping leading/trailing spaces
    - Escaping HTML characters
    - Limiting length to 5000 characters
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
        content = content[:MAX_WEB_LENGTH]
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
    Downloads and parses a website using `requests`.
    Extracts and aggressively cleans visible text content.

    :param url: The URL of the website to parse.
    :returns: Cleaned extracted text if successful, else None.
    """
    logging.info(f"Starting parse for site: {url}")

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
        }
        logging.debug("Sending GET request...")
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
        logging.info(f"Downloaded {len(res.text)} characters from {url}")

    except requests.RequestException as e:
        logging.error(f"Request failed for {url}: {e}")
        return None

    try:
        soup = BeautifulSoup(res.text, "html.parser")

        # Remove non-content tags
        for tag in soup(["script", "style", "noscript", "iframe", "svg", "canvas", "form", "footer", "header", "nav", "aside", "video", "img"]):
            tag.decompose()

        # Remove likely cookie/popup divs
        for div in soup.find_all(lambda t: t.name == "div" and any(
            kw in (t.get("id", "") + str(t.get("class", "")).lower())
            for kw in ["cookie", "consent", "banner", "popup", "overlay", "subscribe", "ad", "paywall", "notification"]
        )):
            div.decompose()

        # Remove elements that aren't displayed
        for elem in soup.find_all(style=lambda value: value and "display:none" in value.replace(" ", "").lower()):
            elem.decompose()

        # Remove data hidden elements
        for elem in soup.find_all(attrs={"aria-hidden": "true"}):
            elem.decompose()

        logging.debug("Extracting text from cleaned soup...")
        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = text.replace("  ", " ")
        text = text.replace(". ", ".")
        
        if len(text) < 10:
            logging.warning(
                f"Extracted text too short from {url} ({len(text)} chars)")
            return None

        cleaned_content = clean_input(text)
        if cleaned_content:
            logging.info(
                f"Final cleaned content length: {len(cleaned_content)}")
        return cleaned_content

    except Exception as e:
        logging.error(f"Parsing failed for {url}: {e}")
        return None


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
