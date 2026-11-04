import logging
from pathlib import Path
from typing import Optional, Dict, Any

from app.services.rules import extract_with_rules, extract_phone
from app.services.language import detect_language
from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "extract.txt"

def load_extract_prompt_template() -> str:
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text(encoding="utf-8")
    return "Extract JSON {name, phone, source, interest, enquiry_type, language} from:"

def extract_enquiry_data(message: str, source: Optional[str] = None) -> Dict[str, Any]:
    """
    Hybrid extraction:
    1. Rules first (regex for phone, Bangla digit normalization, keywords, script detection)
    2. Gemini LLM for semantic extraction (name in complex syntax, context-aware intent)
    3. Seamless fallback to rules if Gemini fails or is rate-limited.
    """
    # 1. Rules first
    rule_results = extract_with_rules(message, default_source=source or "website")
    
    # Standardize result dict
    result = {
        "name": rule_results.get("name"),
        "phone": rule_results.get("phone"),
        "source": source or rule_results.get("source", "website"),
        "interest": rule_results.get("interest", "unknown"),
        "enquiry_type": rule_results.get("enquiry_type", "sales"),
        "language": rule_results.get("language", "english"),
    }

    # 2. Gemini semantic extraction
    if gemini_service.is_available():
        try:
            prompt_template = load_extract_prompt_template()
            full_prompt = f"{prompt_template}\nInput message: {message}\nProvided channel: {source or 'unknown'}\nJSON:"
            gemini_data = gemini_service.generate_json(full_prompt)

            if gemini_data and isinstance(gemini_data, dict):
                # Name: Use Gemini if extracted and clean
                if gemini_data.get("name") and str(gemini_data["name"]).strip().lower() not in ["null", "none", "unknown"]:
                    result["name"] = str(gemini_data["name"]).strip()

                # Phone: Regex phone is authoritative; use Gemini phone only if rules didn't find one
                if not result["phone"] and gemini_data.get("phone"):
                    g_phone = extract_phone(str(gemini_data["phone"])) or str(gemini_data["phone"]).strip()
                    if g_phone and len(g_phone) >= 11:
                        result["phone"] = g_phone

                # Source: Use passed source first, then Gemini if valid
                if not source and gemini_data.get("source") in ["whatsapp", "facebook", "website", "phone"]:
                    result["source"] = gemini_data["source"]

                # Interest: Prefer Gemini semantic classification if non-unknown, or if rule is unknown
                g_interest = str(gemini_data.get("interest", "")).lower()
                if g_interest in ["bootcamp", "fellowship", "corporate", "unknown"]:
                    if result["interest"] == "unknown" or g_interest != "unknown":
                        result["interest"] = g_interest

                # Enquiry Type: Prefer Gemini semantic classification if valid
                g_etype = str(gemini_data.get("enquiry_type", "")).lower()
                if g_etype in ["sales", "support", "spam", "job_seeker"]:
                    result["enquiry_type"] = g_etype

                # Language: Script-based regex is very reliable; fallback to Gemini if detected language was english
                g_lang = str(gemini_data.get("language", "")).lower()
                if g_lang in ["bangla", "banglish", "english"]:
                    if result["language"] == "english" and g_lang != "english":
                        result["language"] = g_lang

        except Exception as e:
            logger.warning(f"Gemini extraction encountered error, falling back to rules: {e}")

    # Ensure non-null values for required fields
    if not result.get("source"):
        result["source"] = source or "website"
    if not result.get("interest"):
        result["interest"] = "unknown"
    if not result.get("enquiry_type"):
        result["enquiry_type"] = "sales"
    if not result.get("language"):
        result["language"] = detect_language(message)

    return result
