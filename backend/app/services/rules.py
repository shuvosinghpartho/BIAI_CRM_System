import re
from typing import Optional, Dict, Any
from app.services.language import detect_language

BANGLA_TO_ENG_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

def convert_bangla_digits(text: str) -> str:
    """Converts Bangla numerical digits (০-৯) to standard English digits (0-9)."""
    if not text:
        return ""
    return text.translate(BANGLA_TO_ENG_DIGITS)

def extract_phone(text: str) -> Optional[str]:
    """
    Extracts and normalizes Bangladeshi phone numbers to 01XXXXXXXXX format.
    Handles Bangla digits, spaces, hyphens, and +88 / 88 country codes.
    """
    if not text:
        return None
    
    # 1. Convert any Bangla digits to English
    converted = convert_bangla_digits(text)
    
    # 2. Find phone pattern: optional (+88 or 88), followed by 01[3-9] and 8 digits
    # Allow spaces or hyphens between digits
    phone_pattern = re.compile(
        r"(?:\+?88\s*)?(01[3-9](?:[\s-]?\d){8})\b"
    )
    match = phone_pattern.search(converted)
    if match:
        digits_only = re.sub(r"\D", "", match.group(0))
        if digits_only.startswith("880"):
            digits_only = digits_only[2:]
        if len(digits_only) == 11 and digits_only.startswith("01"):
            return digits_only

    return None

def extract_interest(text: str) -> str:
    """
    Classifies interest into: bootcamp | fellowship | corporate | unknown
    """
    if not text:
        return "unknown"
    
    t_lower = text.lower()
    
    # Corporate indicators
    corporate_terms = [
        "corporate", "company", "textile", "team", "employees", "onsite",
        "কোম্পানি", "কর্মী", "কর্মীর", "ব্যাংক", "bank", "group discount", "গ্রুপ ডিসকাউন্ট"
    ]
    if any(term in t_lower for term in corporate_terms):
        return "corporate"

    # Fellowship indicators
    fellowship_terms = ["fellowship", "ফেলোশিপ", "cohort", "কোহর্ট", "6 month", "6-month", "৬ মাস", "ছয় মাস"]
    if any(term in t_lower for term in fellowship_terms):
        return "fellowship"

    # Bootcamp indicators (Includes Masterclass, Workshops, Crash courses)
    bootcamp_terms = [
        "bootcamp", "বুটক্যাম্প", "3 day", "3-day", "৩ দিন", "৩ দিনের",
        "masterclass", "মাস্টারক্লাস", "মাস্টার ক্লাস", "workshop", "ওয়ার্কশপ", "ওয়ার্কশপ",
        "webinar", "ওয়েবিনার", "ওয়েবিনার", "ফ্রি ক্লাস", "free class", "crash course"
    ]
    if any(term in t_lower for term in bootcamp_terms):
        return "bootcamp"

    return "unknown"

def extract_enquiry_type(text: str) -> str:
    """
    Classifies enquiry_type into: sales | support | spam | job_seeker
    """
    if not text:
        return "sales"

    t_lower = text.lower()

    # Spam detection
    spam_terms = ["crypto", "bit.ly", "usd every day", "earn 5000", "signals!", "click bit.ly"]
    if any(term in t_lower for term in spam_terms):
        return "spam"

    # Job seeker detection
    # Note: "ei course korle job pabo?" asks about post-course employment (sales inquiry).
    # "looking for a job as an AI intern" is seeking employment at BIAI (job seeker).
    if ("looking for a job" in t_lower or "ai intern" in t_lower or "where do i apply" in t_lower
        or "apply for internship" in t_lower or "cv send" in t_lower) and "course korle" not in t_lower:
        return "job_seeker"

    # Support detection
    # Issues from existing customers: payment confirmation, refund/cancellation of existing enrolment
    support_terms = [
        "পেমেন্ট করেছি কিন্তু কোনো কনফার্মেশন পাইনি",
        "বিকাশে দিয়েছি",
        "cancel his enrolment",
        "cancel enrolment",
        "get his money back",
        "money back",
        "very upset",
        "post about it on facebook"
    ]
    if any(term in t_lower for term in support_terms):
        return "support"

    # Pre-purchase questions or questions about discounts/eligibility/courses are sales
    return "sales"

def extract_name_from_text(text: str) -> Optional[str]:
    """
    Attempts to extract sender name if mentioned in text e.g. "আমার নাম ফারজানা রহমান", "ami Tanvir", "I am Rafi".
    """
    if not text:
        return None
    
    # 1. Bangla name patterns: "আমার নাম [Name]", "নাম: [Name]"
    m_bn = re.search(r"(?:আমার\s+নাম[:ঃ\s]+|নাম[:ঃ\s]+)([^\s।,.?!0-9]+(?:\s+[^\s।,.?!0-9]+)?)", text)
    if m_bn:
        candidate = m_bn.group(1).strip()
        if len(candidate) > 1 and candidate not in ["কি", "হলো", "আছে"]:
            return candidate

    # Bangla "আমি [Name]" (guarding against common verbs/nouns like "আমি কি", "আমি ক্লাস")
    m_bn_ami = re.search(r"\bআমি\s+([^\s।,.?!0-9]+(?:\s+[^\s।,.?!0-9]+)?)", text)
    if m_bn_ami:
        candidate = m_bn_ami.group(1).strip()
        stop_words = {"কি", "চাই", "ক্লাস", "একটি", "কোর্স", "পারব", "পড়ি", "পড়ি", "বলছি", "হতে", "করতে", "একজন"}
        first_word = candidate.split()[0] if candidate.split() else ""
        if first_word not in stop_words and len(candidate) > 2:
            return candidate
    
    # 2. Banglish name patterns: "amar naam [Name]", "amar nam [Name]", "name: [Name]"
    m_bg = re.search(r"(?:amar\s+na?am[:\s]+|name[:\s]+|this\s+is\s+)([A-Za-z]+(?:\s+[A-Za-z]+)?)", text, re.IGNORECASE)
    if m_bg:
        candidate = m_bg.group(1).strip()
        if len(candidate) > 1 and candidate.lower() not in ["ki", "hobe", "chai"]:
            return candidate

    # Banglish "ami [Name]"
    m_bg_ami = re.search(r"\bami\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)\b", text, re.IGNORECASE)
    if m_bg_ami:
        candidate = m_bg_ami.group(1).strip()
        stop_words_bg = {"ki", "chai", "class", "course", "parbo", "bolte", "korbo", "hote", "korte", "student"}
        first_word = candidate.lower().split()[0] if candidate.split() else ""
        if first_word not in stop_words_bg and len(candidate) > 2:
            return candidate

    # 3. English name patterns: "My name is [Name]" or "I am [Name]"
    m_en = re.search(r"(?:my name is|i am)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)", text, re.IGNORECASE)
    if m_en:
        candidate = m_en.group(1).strip()
        stop_words_en = {"a", "an", "the", "looking", "interested", "writing", "student", "working"}
        first_word = candidate.lower().split()[0] if candidate.split() else ""
        if first_word not in stop_words_en and len(candidate) > 2:
            return candidate

    return None

def extract_with_rules(text: str, default_source: str = "website") -> Dict[str, Any]:
    """
    Rule-based extraction pipeline for initial classification and fallback.
    """
    return {
        "name": extract_name_from_text(text),
        "phone": extract_phone(text),
        "source": default_source or "website",
        "interest": extract_interest(text),
        "enquiry_type": extract_enquiry_type(text),
        "language": detect_language(text),
    }

