import pytest

@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_pet_by_status(pet_api, status):
    response = pet_api.find_by_status(status)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for pet in data:
        assert pet["status"] == status

def test_get_pet(test_pet, pet_api):
    response = pet_api.get_pet(test_pet)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == test_pet
    assert data["name"] == "AutomationTestPet"

def test_create_pet(pet_api):
    response = pet_api.create_pet({"name": "CreatedByAutomation", "status": "available"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "CreatedByAutomation"
    assert data["status"] == "available"
    pet_api.delete_pet(data["id"])

def test_update_pet(test_pet, pet_api):
    response = pet_api.update_pet({"id": test_pet, "name": "UpdatedAutomationPet", "status": "sold"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_pet
    assert data["name"] == "UpdatedAutomationPet"
    assert data["status"] == "sold"

def test_delete_pet(test_pet, pet_api):
    response = pet_api.delete_pet(test_pet)
    assert response.status_code == 200
    assert response.json()["message"] == str(test_pet)

def test_get_non_existing_pet(pet_api):
    response = pet_api.get_pet(999999999)
    assert response.status_code == 404
