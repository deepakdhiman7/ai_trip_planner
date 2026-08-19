from tools.weather_client import WeatherClient
from dotenv import load_dotenv

load_dotenv()


client = WeatherClient()
current_weather = client.get_current_weather("Noida")
print(current_weather)