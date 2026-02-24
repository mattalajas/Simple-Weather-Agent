from __future__ import annotations

from src.clients.weather_client import WeatherClient


def geocode_location(location: str, weather_client: WeatherClient | None = None) -> dict:
    client = weather_client or WeatherClient()
    return client.geocode_location(location)
