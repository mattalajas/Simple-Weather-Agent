from __future__ import annotations

from openai import OpenAI


def build_gemini_client(api_key: str) -> OpenAI:
    return OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
