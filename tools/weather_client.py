import os
import requests

class WeatherClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    
    def _get_lat_long(self, city_name: str) -> tuple[float, float]:
        """Private: resolve a city name to (lat, lon). Raises on failure."""
        limit=5
        url_geo_coding = (f"http://api.openweathermap.org/geo/1.0/direct"
                              f"?q={city_name}&limit={limit}&appid={self.api_key}")
        
        response = requests.get(url_geo_coding, timeout=10)
        response.raise_for_status()

        results = response.json()
        if not results:
            raise ValueError(f"No location found for city: {city_name}")

        location = results[0]
        return location["lat"], location["lon"]


    def _fetch_raw(self, lat: float, lon: float) -> dict:
        """Private: raw current-weather call for a resolved lat/lon."""

        url_current_weather = (f"https://api.openweathermap.org/data/2.5/weather"
                               f"?lat={lat}&lon={lon}&units=metric&appid={self.api_key}")

        response = requests.get(url_current_weather, timeout=10)
        response.raise_for_status()

        results = response.json()
        if not results:
            raise ValueError(f"No data received...")
        return results


    def get_current_weather(self, city_name: str) -> dict:
        """Public: city name in, shaped weather dict out."""
        lat, lon = self._get_lat_long(city_name)
        raw = self._fetch_raw(lat, lon)

        weather_info = raw["weather"][0]

        return {
            "city": city_name,
            "description": weather_info["description"],
            "temp": raw["main"]["temp"],
            "feels_like": raw["main"]["feels_like"],
            "humidity": raw["main"]["humidity"]
        }

