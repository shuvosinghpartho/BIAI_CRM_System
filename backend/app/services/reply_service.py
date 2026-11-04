import logging
from pathlib import Path
from typing import Optional, Dict, Any

from app.services.language import detect_language, get_reply_language
from app.services.gemini_service import gemini_service
from app.services.reply_templates import get_template_reply

logger = logging.getLogger(__name__)

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "reply.txt"

def load_reply_prompt_template() -> str:
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text(encoding="utf-8")
    return "Suggest a polite reply matching the customer's language:"

def suggest_reply(
    message: str,
    name: Optional[str] = None,
    interest: Optional[str] = None,
    enquiry_type: Optional[str] = None,
    language: Optional[str] = None
) -> str:
    """
    Suggests a reply in English or Banglish, matching how the person wrote.
    Uses Gemini when available, falls back to reply templates if Gemini fails.
    """
    detected_lang = language or detect_language(message)
    reply_lang = get_reply_language(detected_lang)
    resolved_interest = interest or "unknown"
    resolved_type = enquiry_type or "sales"

    # 1. Attempt Gemini generation
    if gemini_service.is_available():
        try:
            template = load_reply_prompt_template()
            prompt = template.format(
                name=name or "Customer",
                interest=resolved_interest,
                enquiry_type=resolved_type,
                reply_language=reply_lang,
                message=message
            )
            ai_reply = gemini_service.generate_text(prompt)
            if ai_reply and len(ai_reply.strip()) > 10:
                return ai_reply.strip()
        except Exception as e:
            logger.warning(f"Gemini reply generation failed, falling back to template: {e}")

    # 2. Template fallback
    return get_template_reply(
        reply_language=reply_lang,
        interest=resolved_interest,
        enquiry_type=resolved_type,
        name=name
    )
