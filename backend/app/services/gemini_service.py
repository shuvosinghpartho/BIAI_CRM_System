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
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite"
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
        self._cache: Dict[str, Any] = {}
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize AI Client: {e}")

    def is_available(self) -> bool:
        return self.client is not None

    def generate_json(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Calls AI model to generate structured JSON output with low latency.
        Returns parsed dict or None on failure.
        """
        if not self.is_available():
            return None

        cache_key = f"json:{hash(prompt)}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        unique_models = list(dict.fromkeys(FALLBACK_MODELS))
        for model in unique_models:
            # Models that support thinking_budget=0
            supports_budget = "flash-lite" not in model
            if supports_budget:
                try:
                    config = types.GenerateContentConfig(
                        temperature=0.1,
                        max_output_tokens=350,
                        response_mime_type="application/json",
                        thinking_config=types.ThinkingConfig(thinking_budget=0)
                    )
                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=config
                    )
                    raw_text = extract_text_safely(response)
                    if raw_text:
                        if raw_text.startswith("```"):
                            raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
                            raw_text = re.sub(r"\s*```$", "", raw_text)
                        parsed = json.loads(raw_text)
                        self._cache[cache_key] = parsed
                        return parsed
                except Exception as e:
                    logger.debug(f"Budget=0 JSON config failed on {model}: {e}")

            # Standard config without thinking_budget
            try:
                config = types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=350,
                    response_mime_type="application/json"
                )
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config
                )
                raw_text = extract_text_safely(response)
                if raw_text:
                    if raw_text.startswith("```"):
                        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
                        raw_text = re.sub(r"\s*```$", "", raw_text)
                    parsed = json.loads(raw_text)
                    self._cache[cache_key] = parsed
                    return parsed
            except Exception as e:
                logger.warning(f"AI generate_json failed with model {model}: {e}")
                continue

        return None

    def generate_text(self, prompt: str, max_tokens: int = 350) -> Optional[str]:
        """
        Calls AI model to generate free-form text with low latency.
        Returns generated string or None on failure.
        """
        if not self.is_available():
            return None

        cache_key = f"text:{hash(prompt)}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        unique_models = list(dict.fromkeys(FALLBACK_MODELS))
        for model in unique_models:
            supports_budget = "flash-lite" not in model
            if supports_budget:
                try:
                    config = types.GenerateContentConfig(
                        temperature=0.2,
                        max_output_tokens=max_tokens,
                        thinking_config=types.ThinkingConfig(thinking_budget=0)
                    )
                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=config
                    )
                    raw_text = extract_text_safely(response)
                    if raw_text:
                        self._cache[cache_key] = raw_text
                        return raw_text
                except Exception as e:
                    logger.debug(f"Budget=0 text config failed on {model}: {e}")

            try:
                config = types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=max_tokens
                )
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config
                )
                raw_text = extract_text_safely(response)
                if raw_text:
                    self._cache[cache_key] = raw_text
                    return raw_text
            except Exception as e:
                logger.warning(f"AI generate_text failed with model {model}: {e}")
                continue

        return None

gemini_service = GeminiService()
