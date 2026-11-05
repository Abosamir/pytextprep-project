# word_tokenize, sent_tokenize
import re
from cleaning import require_str

GET_TOKENS = re.compile(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*")
SPLIT_PATERN = re.compile(r"""
    (?<!\bDr\.)(?<!\bMr\.)(?<!\bMrs\.)(?<!\bMs\.)  
    (?<!\be\.g\.)(?<!\bi\.e\.)(?<!\betc\.)         
    (?<=[.!?])                                      
    \s+                                            
    (?=[A-Z0-9])                                   
""", re.VERBOSE)

@require_str
def word_tokenize(text: str) -> list[str]:
    """split the text into tokenize

    Args:
        text (str): raw input text

    Returns:
        list[str]: list of tokenized words
    """
    return re.findall(GET_TOKENS, text)

@require_str
def sent_tokenize(text: str) -> str:
    pass




if __name__ == "__main__":
    print(word_tokenize(10))