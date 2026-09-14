class PetAPI:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_pet(self, pet_id):
        return self.api_client.get(f"/pet/{pet_id}")

    def find_by_status(self, status):
        return self.api_client.get("/pet/findByStatus", params={"status": status})

    def create_pet(self, payload):
        return self.api_client.post("/pet", json=payload)

    def update_pet(self, payload):
        return self.api_client.put("/pet", json=payload)

    def delete_pet(self, pet_id):
        return self.api_client.delete(f"/pet/{pet_id}")
