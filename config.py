import os

PETSTORE_BASE_URL = os.getenv("PETSTORE_BASE_URL", "https://petstore.swagger.io/v2")
WEATHER_BASE_URL = os.getenv("WEATHER_BASE_URL", "https://api.open-meteo.com/v1")
VERIFY_SSL = os.getenv("VERIFY_SSL", "false").lower() in {"true", "1", "yes"}
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "30"))
RETRY_COUNT = int(os.getenv("RETRY_COUNT", "2"))
API_TOKEN = os.getenv("API_TOKEN") or None
