from __future__ import annotations

import argparse
import logging

from src.agent import WeatherAgent
from src.clients.llm_client import build_gemini_client
from src.config import get_settings
from src.utils.logging import configure_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple Weather Agent CLI")
    parser.add_argument("query", nargs="+", help="User weather question")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    user_input = " ".join(args.query).strip()

    settings = get_settings()
    client = build_gemini_client(settings.gemini_api_key)
    agent = WeatherAgent(
        client=client,
        model=settings.gemini_model,
        temperature=settings.temperature,
    )

    logging.info("Running weather agent for query: %s", user_input)
    response = agent.ask(user_input)
    print(response)


if __name__ == "__main__":
    main()
