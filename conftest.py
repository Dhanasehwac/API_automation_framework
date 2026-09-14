import pytest

from api.api_client import APIClient
from api.pet_api import PetAPI
from api.weather_api import WeatherAPI
from config import PETSTORE_BASE_URL, WEATHER_BASE_URL, VERIFY_SSL, REQUEST_TIMEOUT, RETRY_COUNT, API_TOKEN

@pytest.fixture
def api_client():
    return APIClient(PETSTORE_BASE_URL, verify=VERIFY_SSL, timeout=REQUEST_TIMEOUT,
                     retries=RETRY_COUNT, token=API_TOKEN)

@pytest.fixture
def pet_api(api_client):
    return PetAPI(api_client)

@pytest.fixture
def weather_api():
    return WeatherAPI(APIClient(WEATHER_BASE_URL, verify=VERIFY_SSL,
                                timeout=REQUEST_TIMEOUT, retries=RETRY_COUNT))

@pytest.fixture
def test_pet(pet_api):
    response = pet_api.create_pet({"name": "AutomationTestPet", "status": "available"})
    assert response.status_code == 200, response.text
    pet_id = response.json()["id"]
    yield pet_id
    delete_response = pet_api.delete_pet(pet_id)
    assert delete_response.status_code in (200, 404)
