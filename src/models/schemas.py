from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class WeatherQuery:
    location: str
    days: int = 3


@dataclass(frozen=True)
class ToolResult:
    name: str
    payload: dict[str, Any]
