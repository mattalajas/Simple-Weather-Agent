from __future__ import annotations

from typing import Any

import requests


class WeatherClient:
    GEO_BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def geocode_location(self, location: str) -> dict[str, Any]:
        params = {"name": location, "count": 1, "language": "en", "format": "json"}
        response = requests.get(self.GEO_BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        results = data.get("results") or []
        if not results:
            raise ValueError(f"Could not resolve location: {location}")
        top = results[0]
        return {
            "name": top.get("name"),
            "country": top.get("country"),
            "latitude": top.get("latitude"),
            "longitude": top.get("longitude"),
            "timezone": top.get("timezone"),
        }

    def get_forecast(self, latitude: float, longitude: float, days: int = 3) -> dict[str, Any]:
        safe_days = max(1, min(days, 7))
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "forecast_days": safe_days,
            "timezone": "auto",
        }
        response = requests.get(self.FORECAST_BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
