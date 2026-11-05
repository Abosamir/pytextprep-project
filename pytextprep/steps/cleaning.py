import unicodedata
import string
from functools import wraps
from collections import Counter
import re

SPACES_RE = re.compile(r"\s+")
URL_RE = re.compile(r"https?://\S+|www\.[^\s,!?;]+")
MAIL_RE = re.compile(r"\S+@\S+")


def require_str(func):

    @wraps(func)

    def wrapper(text, *args, **kwargs):
        if not isinstance(text, str):
            raise  TypeError(f"{func.__name__}() expects str, got {type(text).__name__}")

        return func(text, *args, **kwargs)

    return wrapper


@require_str
def lower_case(text: str) -> str:
    """This function is to make all the text letters to be in lowercase.

    Args:
        text (str): the raw input text.

    Returns:
        str: the result text after lowering it.
    """
    return text.casefold()

@require_str
def normalize_whitespace(text: str) -> str:
    """This function is made to remove multiple white spaces and taps and also newlines.

    Args:
        text (str): the raw input text.

    Returns:
        str: the result text after removing unnecessary spaces.
    """

    return SPACES_RE.sub(" ", text)

@require_str
def remove_urls(text: str, replace_with: str = "") -> str:

    """This function is to remove urls from the raw text

    Args:
        text (str): the raw input text
        replace_with (_type_, optional): what you want to replace the urls with

    Returns:
        str: the result text after removing urls.
    """

    return URL_RE.sub(replace_with, text)

@require_str
def remove_emails(text: str, replace_with: str = "") -> str:
    
    """This function is to remove emails from raw text

    Args:
        text (str): the raw input text
        replace_with (str, optional): what you want to replace the emails with

    Returns:
        str: the result text after removing emails.
    """

    return MAIL_RE.sub(replace_with, text)

@require_str
def is_emoji(char: str) -> bool:
    """detect if a given character is an emoji.

    Args:
        char (str): the character we will put on test.

    Returns:
        bool: True is an emoji, and False if not.
    """

    return unicodedata.category(char) == 'So'

@require_str
def remove_punctuation(text: str, keep_emojis: bool = True):
    """This function is made to remove punctuation from a string and also emojis if the user want

    Args:
        text (str): the raw input text
        keep_emojis (bool, optional): if you want to keep the emojis inside the raw text Defaults to True.

    Returns:
        str: the result text after removing punctuations and emojis (if needed). 
    """
    pun = set(string.punctuation)
    result_text = ""

    if keep_emojis:
        for i in range(len(text)):
            if text[i] not in pun:
                result_text += text[i]
            else:
                if text[i] =="'" and text[i-1] == "n":
                    result_text += "'"
                else:
                    result_text += " "
    else:
        for i in range(len(text)):

            if text[i] in pun:
                if text[i] =="'" and text[i-1] == "n":
                    result_text += "'"
                else:
                    result_text += " "

            elif is_emoji(text[i]):
                result_text += ""
            else:
                result_text += text[i]
    return result_text

@require_str
def normalize_repeating_chars(text, keep=1):

    return re.sub(r'(.)\1{2,}', lambda m: m.group(1) * keep, text)

if __name__ == "__main__":


    text = "I looove it, sooo good"
    print(normalize_repeating_chars(text))