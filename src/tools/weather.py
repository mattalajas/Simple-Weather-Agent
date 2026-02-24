from __future__ import annotations

from src.clients.weather_client import WeatherClient


def get_forecast_for_location(
    location: str,
    days: int = 3,
    weather_client: WeatherClient | None = None,
) -> dict:
    client = weather_client or WeatherClient()
    geo = client.geocode_location(location)
    forecast = client.get_forecast(geo["latitude"], geo["longitude"], days=days)
    return {"location": geo, "forecast": forecast}
