import json
import logging
import re
import warnings
from typing import Optional, Dict, Any

# Suppress library deprecation and SSL notice warnings
warnings.filterwarnings("ignore", module="urllib3")
warnings.filterwarnings("ignore", module="google")

from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

# Fallback models in priority order
FALLBACK_MODELS = [
    GEMINI_MODEL,
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-flash-latest"
]

def extract_text_safely(response: Any) -> Optional[str]:
    """Extracts text content cleanly from Gemini response, avoiding thought parts."""
    if not response:
        return None
    try:
        if hasattr(response, "text") and response.text:
            return response.text.strip()
    except Exception:
        pass

    # Alternative candidate extraction
    try:
        if hasattr(response, "candidates") and response.candidates:
            first_candidate = response.candidates[0]
            if hasattr(first_candidate, "content") and first_candidate.content:
                parts = first_candidate.content.parts or []
                text_segments = [p.text for p in parts if hasattr(p, "text") and p.text]
                if text_segments:
                    return "".join(text_segments).strip()
    except Exception as e:
        logger.debug(f"Candidate parsing error: {e}")

    return None

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize AI Client: {e}")

    def is_available(self) -> bool:
        return self.client is not None

    def generate_json(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Calls AI model to generate structured JSON output.
        Returns parsed dict or None on failure.
        """
        if not self.is_available():
            return None

        # Clean prompt
        unique_models = list(dict.fromkeys(FALLBACK_MODELS))
        for model in unique_models:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        response_mime_type="application/json"
                    )
                )
                raw_text = extract_text_safely(response)
                if raw_text:
                    if raw_text.startswith("```"):
                        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
                        raw_text = re.sub(r"\s*```$", "", raw_text)
                    return json.loads(raw_text)
            except Exception as e:
                logger.warning(f"AI generate_json failed with model {model}: {e}")
                continue

        return None

    def generate_text(self, prompt: str) -> Optional[str]:
        """
        Calls AI model to generate free-form text.
        Returns generated string or None on failure.
        """
        if not self.is_available():
            return None

        unique_models = list(dict.fromkeys(FALLBACK_MODELS))
        for model in unique_models:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3
                    )
                )
                raw_text = extract_text_safely(response)
                if raw_text:
                    return raw_text
            except Exception as e:
                logger.warning(f"AI generate_text failed with model {model}: {e}")
                continue

        return None

gemini_service = GeminiService()
