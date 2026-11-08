from .cleaning import require_str
from ..registry import register_step


VOWELS = {"a", "o", "e", "i", "u"}

def cv_pattern(word: str) -> str:
    """Compress a word into runs of c and v, e.g. 'tree' -> 'cv'."""
    if not word:
        return ""

    pattern = ""
    p1 = 0
    p2 = 0

    while p2 < len(word):
        if word[p1] not in VOWELS:
            while p2 < len(word) and word[p2] not in VOWELS:
                p2 += 1
            pattern += "c"
        else:
            while p2 < len(word) and word[p2] in VOWELS:
                p2 += 1
            pattern += "v"
        p1 = p2

    return pattern


def measure(word: str) -> int:
    """m = number of 'vc' pairs in the pattern."""
    return cv_pattern(word).count("vc")


def has_vowel(word: str) -> bool:
    return any(c in VOWELS for c in word)


def ends_double_consonant(word: str) -> bool:
    return len(word) >= 2 and word[-1] == word[-2] and word[-1] not in VOWELS


def ends_cvc(word: str) -> bool:
    """Last 3 letters are consonant, vowel, consonant (last not w, x, y)."""
    if len(word) < 3:
        return False
    c1, v, c2 = word[-3], word[-2], word[-1]
    return (c1 not in VOWELS and v in VOWELS
            and c2 not in VOWELS and c2 not in "wxy")


def apply_rules(word: str, rules, min_m: int) -> str:
    for suffix, replacement in rules:
        if word.endswith(suffix):
            base = word[:-len(suffix)]
            if measure(base) > min_m:
                return base + replacement
            return word
    return word



def step1a(word: str) -> str:
    if word.endswith("sses"):
        return word[:-2]          
    if word.endswith("ies"):
        return word[:-2]          
    if word.endswith("ss"):
        return word               
    if word.endswith("s"):
        return word[:-1]          
    return word


def step1b_cleanup(word: str) -> str:
    if word.endswith(("at", "bl", "iz")):
        return word + "e"
    if ends_double_consonant(word) and word[-1] not in "lsz":
        return word[:-1]
    if measure(word) == 1 and ends_cvc(word):
        return word + "e"
    return word


def step1b(word: str) -> str:
    if word.endswith("eed"):
        if measure(word[:-3]) > 0:
            return word[:-1]      # eed -> ee
        return word               # stop here, do not try ed

    for suffix in ("ed", "ing"):
        if word.endswith(suffix):
            base = word[:-len(suffix)]
            if has_vowel(base):
                return step1b_cleanup(base)
            return word
    return word


def step1c(word: str) -> str:
    if word.endswith("y") and has_vowel(word[:-1]):
        return word[:-1] + "i"
    return word



STEP2_RULES = [
    ("ational", "ate"), ("tional", "tion"), ("enci", "ence"),
    ("anci", "ance"), ("izer", "ize"), ("abli", "able"),
    ("alli", "al"), ("entli", "ent"), ("eli", "e"),
    ("ousli", "ous"), ("ization", "ize"), ("ation", "ate"),
    ("ator", "ate"), ("alism", "al"), ("iveness", "ive"),
    ("fulness", "ful"), ("ousness", "ous"), ("aliti", "al"),
    ("iviti", "ive"), ("biliti", "ble"),
]

STEP3_RULES = [
    ("icate", "ic"), ("ative", ""), ("alize", "al"),
    ("iciti", "ic"), ("ical", "ic"), ("ful", ""), ("ness", ""),
]

STEP4_SUFFIXES = [
    "al", "ance", "ence", "er", "ic", "able", "ible", "ant",
    "ement", "ment", "ent", "ion",
    "ou", "ism", "ate", "iti", "ous", "ive", "ize",
]


def step2(word: str) -> str:
    return apply_rules(word, STEP2_RULES, min_m=0)


def step3(word: str) -> str:
    return apply_rules(word, STEP3_RULES, min_m=0)


def step4(word: str) -> str:
    for suffix in STEP4_SUFFIXES:
        if word.endswith(suffix):
            base = word[:-len(suffix)]
            if measure(base) > 1:
                if suffix == "ion" and not base.endswith(("s", "t")):
                    return word
                return base
            return word
    return word


def step5a(word: str) -> str:
    if word.endswith("e"):
        base = word[:-1]
        m = measure(base)
        if m > 1 or (m == 1 and not ends_cvc(base)):
            return base
    return word


def step5b(word: str) -> str:
    if measure(word) > 1 and word.endswith("ll"):
        return word[:-1]
    return word


@register_step("stem")
@require_str
def stem(word: str) -> str:
    word = word.lower()
    if len(word) <= 2:
        return word

    for step in (step1a, step1b, step1c, step2, step3,
                step4, step5a, step5b):
        word = step(word)

    return word


if __name__ == "__main__":
    
    print(stem("ponies"))