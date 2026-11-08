from .cleaning import require_str
from ..registry import register_step

TASHKEEL = set(range(0x064B, 0x0653)) | {0x0670} | {0x0640}
ALEF =  set(range(0x0622, 0x0628)) 
taa_marbuta = True
ALEF_MAKSURA = 0x0649
TAA_MARBUTA = 0x0629


@register_step("normalize_arabic")
@require_str
def normalize_arabic(text: str) -> str:
    """remove tashkeel from the arabic words

    Args:
        text (str): arabic word with tashkeel

    Returns:
        str: arabic word without tashkeel 
    """
    result_text = ""
    for ch in text:
        if taa_marbuta:
            if ord(ch) == TAA_MARBUTA:
                result_text += "ه"
                continue

        if ord(ch) == ALEF_MAKSURA:
            result_text += "ي"
            continue

        if ord(ch) in ALEF:
            result_text += "ا"
            continue

        if ord(ch) not in TASHKEEL:
            result_text += ch
            continue
    return result_text


if __name__ == "__main__":

    print(normalize_arabic("أَهْلاً بِكُم في الـــمـعهد") == "اهلا بكم في المعهد")