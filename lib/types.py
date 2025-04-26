from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Result:
    """
    Represents truth detection on a result by LLM

    :param id: Unique identifier for the result.
    :param input: Original input from user.
    :param timestamp: Timestamp when the result is created.
    :param link: Optional link if content is from web.
    :param content: Cleaned or downloaded content to feed to LLM.
    :param title: Title of the result.
    :param result: Numeric outcome of the result.
    :param reason: Explanation or reason for the result.
    """
    # On creation
    id: str
    input: str
    timestamp: datetime = field(default_factory=datetime.now)

    # Filled with parsing
    link: Optional[str] = None
    content: Optional[str] = None

    # Filled by ChatGPT
    title: Optional[str] = None
    reason: Optional[str] = None
    
    # From API
    predictions: Optional[list] = None