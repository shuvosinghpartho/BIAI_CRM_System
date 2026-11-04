import json
import logging
import re
from typing import Optional, Dict, Any
from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

# Fallback candidate models if the primary configured model has a momentary spike
FALLBACK_MODELS = [GEMINI_MODEL, "gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-flash-latest"]

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Gemini Client: {e}")

    def is_available(self) -> bool:
        return self.client is not None

    def generate_json(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Calls Gemini to generate structured JSON output.
        Returns parsed dict or None on failure.
        """
        if not self.is_available():
            return None

        # Clean prompt
        for model in dict.fromkeys(FALLBACK_MODELS):  # Preserve order, unique
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        response_mime_type="application/json"
                    )
                )
                if response and response.text:
                    raw_text = response.text.strip()
                    # Strip any markdown fences if present
                    if raw_text.startswith("```"):
                        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
                        raw_text = re.sub(r"\s*```$", "", raw_text)
                    return json.loads(raw_text)
            except Exception as e:
                logger.warning(f"Gemini generate_json failed with model {model}: {e}")
                continue

        return None

    def generate_text(self, prompt: str) -> Optional[str]:
        """
        Calls Gemini to generate free-form text.
        Returns generated string or None on failure.
        """
        if not self.is_available():
            return None

        for model in dict.fromkeys(FALLBACK_MODELS):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3
                    )
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                logger.warning(f"Gemini generate_text failed with model {model}: {e}")
                continue

        return None

gemini_service = GeminiService()
