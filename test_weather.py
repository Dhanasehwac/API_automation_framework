def test_get_current_weather(weather_api):
    response = weather_api.get_current_weather(13.0827, 80.2707)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    data = response.json()
    assert "current" in data
    assert "temperature_2m" in data["current"]
    assert "wind_speed_10m" in data["current"]

def test_invalid_latitude(weather_api):
    response = weather_api.get_current_weather(100.0, 80.2707)
    assert response.status_code == 400
    data = response.json()
    assert data.get("error") is True
    assert "reason" in data
