from __future__ import annotations

import json
from typing import Any

from openai import OpenAI

from src.prompts import SYSTEM_PROMPT
from src.tools.weather import get_forecast_for_location


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_forecast_for_location",
            "description": "Get weather forecast and current conditions for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City, region, or place name."},
                    "days": {
                        "type": "integer",
                        "description": "Number of forecast days (1-7).",
                        "minimum": 1,
                        "maximum": 7,
                    },
                },
                "required": ["location"],
            },
        },
    }
]


class WeatherAgent:
    def __init__(self, client: OpenAI, model: str, temperature: float = 0.2) -> None:
        self.client = client
        self.model = model
        self.temperature = temperature

    def ask(self, user_input: str) -> str:
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ]

        first = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=self.temperature,
        )

        first_message = first.choices[0].message
        tool_calls = first_message.tool_calls or []

        if not tool_calls:
            return first_message.content or "I could not generate a response."

        messages.append(
            {
                "role": "assistant",
                "content": first_message.content or "",
                "tool_calls": [call.model_dump() for call in tool_calls],
            }
        )

        for call in tool_calls:
            if call.function.name != "get_forecast_for_location":
                continue

            args = json.loads(call.function.arguments or "{}")
            location = args.get("location", "")
            days = int(args.get("days", 3))

            try:
                result = get_forecast_for_location(location=location, days=days)
            except Exception as exc:  # pragma: no cover - network/runtime errors
                result = {"error": str(exc), "location": location, "days": days}

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": "get_forecast_for_location",
                    "content": json.dumps(result),
                }
            )

        final = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
        return final.choices[0].message.content or "I could not generate a response."
