from os import getenv
from dotenv import load_dotenv


load_dotenv()

WEATHER_API = "http://api.weatherapi.com/v1/"
WEATHER_API_TOKEN = getenv("WEATHER_API_TOKEN")
BASE_HOST = getenv("API_URL")
