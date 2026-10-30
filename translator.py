"""Thin wrapper around the Microsoft Translator (Azure AI Translator) REST API v3."""

import os
import uuid

import requests
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
API_KEY = os.getenv("TRANSLATOR_KEY")
REGION = os.getenv("TRANSLATOR_REGION")

# Display name -> Microsoft Translator language code
LANGUAGES = {
    "Arabic": "ar",
    "Bengali": "bn",
    "Chinese (Simplified)": "zh-Hans",
    "Dutch": "nl",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Hindi": "hi",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Russian": "ru",
    "Spanish": "es",
    "Swedish": "sv",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
}

AUTO_DETECT = "Auto-detect"


class TranslationError(Exception):
    """Raised when the translation request fails."""


def is_configured() -> bool:
    return bool(API_KEY and REGION)


def translate(text: str, target: str, source: str | None = None) -> dict:
    """Translate `text` into `target`.

    `source` is a language code, or None to let the API detect it.
    Returns {"text": translated_text, "detected": code_or_None, "score": float_or_None}.
    """
    if not text.strip():
        raise TranslationError("Please enter some text to translate.")
    if not is_configured():
        raise TranslationError(
            "Translator API key/region missing. Copy .env.example to .env and fill it in."
        )

    params = {"api-version": "3.0", "to": target}
    if source:
        params["from"] = source

    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Ocp-Apim-Subscription-Region": REGION,
        "Content-Type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    try:
        response = requests.post(
            f"{ENDPOINT}/translate",
            params=params,
            headers=headers,
            json=[{"Text": text}],
            timeout=15,
        )
    except requests.RequestException as exc:
        raise TranslationError(f"Network error: {exc}") from exc

    if response.status_code != 200:
        try:
            message = response.json()["error"]["message"]
        except (ValueError, KeyError):
            message = response.text
        raise TranslationError(f"API error {response.status_code}: {message}")

    result = response.json()[0]
    detected = result.get("detectedLanguage", {})
    return {
        "text": result["translations"][0]["text"],
        "detected": detected.get("language"),
        "score": detected.get("score"),
    }
