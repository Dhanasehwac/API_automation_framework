class WeatherAPI:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_current_weather(self, latitude, longitude):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m",
        }
        return self.api_client.get("/forecast", params=params)
