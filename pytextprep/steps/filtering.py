from .cleaning import require_str
from .tokenizer import word_tokenize
from importlib.resources import files
from pytextprep.registry import register_step

STOPWORDS = set(
    files("pytextprep.resources")
    .joinpath("stopwords_en.txt")
    .read_text(encoding="utf-8")
    .splitlines()
)

text = files("pytextprep.resources").joinpath("contractions_en.tsv").read_text(encoding="utf-8")

CONTRACTIONS = {}
for line in text.splitlines():
    if not line.strip():
        continue                      
    short, full = line.split("\t", 1)
    CONTRACTIONS[short] = full


@register_step("remove_stopwords", params={"custom_words", "extra_only"})
@require_str
def remove_stopwords(text: str, custom_words=None, extra_only=False) -> str:
    """Remove stop words from a raw text with considering the custom words

    Args:
        text (str): The raw input text
        custom_words (list[str], optional): list of custom of stop wards. Defaults to None.
        extra_only (bool, optional): define where to look at when removing stop words. Defaults to False.

    Returns:
        str: the result text after dealing with the stop words
    """

    tokenized_words = word_tokenize(text)
    result_text = ""

    if not extra_only:
        if custom_words:
            for word in tokenized_words:
                if word.lower() not in custom_words and word.lower() not in STOPWORDS:
                    result_text += word + " "
        else:
            for word in tokenized_words:
                if word.lower() not in STOPWORDS:
                    result_text += word + " "
    else:
        if custom_words:
            for word in tokenized_words:
                if word.lower() not in custom_words:
                    result_text += word + " "
        else:
            result_text = text + " "


    return result_text[:-1]

@register_step("expand_contractions")
@require_str
def expand_contractions(text: str) -> str:
    """Transform contraction words into full form.

    Args:
        text (str): The raw input text with contraction words involved into it.

    Returns:
        str: The result text after transforming the contraction words.
    """

    result_str = ""

    for word in text.split():
        if word in CONTRACTIONS:
            result_str += CONTRACTIONS[word] + " "
        else:
            result_str += word + " "
    return result_str[:-1]

if __name__ == "__main__":

    print(remove_stopwords("THE end"))
