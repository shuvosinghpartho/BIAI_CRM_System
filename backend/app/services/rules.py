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
    fellowship_terms = ["fellowship", "ফেলোশিপ"]
    if any(term in t_lower for term in fellowship_terms):
        return "fellowship"

    # Bootcamp indicators
    bootcamp_terms = ["bootcamp", "বুটক্যাম্প", "3 day", "3-day"]
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
    Attempts to extract sender name if mentioned in text e.g. "আমার নাম ফারজানা রহমান".
    """
    if not text:
        return None
    
    # Bangla name pattern: "আমার নাম [Name]"
    m_bn = re.search(r"আমার\s+নাম\s+([^\s।,.?!]+(?:\s+[^\s।,.?!]+)?)", text)
    if m_bn:
        return m_bn.group(1).strip()
    
    # English name pattern: "My name is [Name]" or "I am [Name]"
    m_en = re.search(r"(?:my name is|i am)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)", text, re.IGNORECASE)
    if m_en:
        return m_en.group(1).strip()

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

