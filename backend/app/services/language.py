import re

# Unicode range for Bengali: U+0980 to U+09FF
BANGLA_CHAR_PATTERN = re.compile(r"[\u0980-\u09FF]")

# Common Banglish lexical markers (phonetic transliterated Bengali in Latin letters)
BANGLISH_WORDS = {
    "kobe", "koto", "chai", "ache", "ami", "apnader", "vai", "bhai",
    "gula", "naki", "korle", "pabo", "kothay", "hobe", "bolen",
    "kibhabe", "korbo", "mane", "pawa", "jay", "shuru", "amar",
    "apni", "tumi", "ei", "ki", "ta", "er", "te", "shob", "bhalo",
    "bujhte", "jani", "dekhi", "dibo", "dite", "parbo", "ashole",
    "dhonnobad", "assalamualaikum", "walaikumsalam", "khobor",
    "korte", "hobe", "keno", "kemon"
}

def detect_language(text: str) -> str:
    """
    Detect language based on project rules:
    - Bangla script present -> "bangla"
    - Latin letters with Bangla words -> "banglish"
    - else -> "english"
    """
    if not text:
        return "english"

    # Check for Bengali script
    if BANGLA_CHAR_PATTERN.search(text):
        return "bangla"

    # Normalize and tokenize Latin words
    words = set(re.findall(r"[a-zA-Z]+", text.lower()))
    
    # Check intersection with Banglish keywords
    if words.intersection(BANGLISH_WORDS):
        return "banglish"

    return "english"

def get_reply_language(detected_lang: str) -> str:
    """
    Language matching rule:
    - If sender wrote in Bangla -> reply in "bangla" (বাংলা লিপি)
    - If sender wrote in Banglish -> reply in "banglish" (Latin script)
    - If sender wrote in English -> reply in "english"
    """
    if detected_lang in ["bangla", "banglish", "english"]:
        return detected_lang
    return "bangla" if detected_lang == "bangla" else "banglish"


