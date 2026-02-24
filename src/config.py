import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gemini_model: str = "gemini-2.0-flash"
    temperature: float = 0.2


def get_settings() -> Settings:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is required. Add it to your environment or .env file.")

    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip() or "gemini-2.0-flash"
    temperature_raw = os.getenv("TEMPERATURE", "0.2").strip()
    try:
        temperature = float(temperature_raw)
    except ValueError as exc:
        raise ValueError("TEMPERATURE must be a valid float.") from exc

    return Settings(gemini_api_key=api_key, gemini_model=model, temperature=temperature)
