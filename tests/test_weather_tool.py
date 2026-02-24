from src.tools.weather import get_forecast_for_location


class StubWeatherClient:
    def geocode_location(self, location: str) -> dict:
        return {
            "name": location,
            "country": "US",
            "latitude": 47.6062,
            "longitude": -122.3321,
            "timezone": "America/Los_Angeles",
        }

    def get_forecast(self, latitude: float, longitude: float, days: int = 3) -> dict:
        return {"latitude": latitude, "longitude": longitude, "days": days}


def test_get_forecast_for_location_uses_geocode_and_forecast():
    payload = get_forecast_for_location("Seattle", days=2, weather_client=StubWeatherClient())

    assert payload["location"]["name"] == "Seattle"
    assert payload["forecast"]["days"] == 2
