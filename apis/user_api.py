class UserAPI:
    def __init__(self, api_client):
        self.api_client = api_client

    def user_register(self, username, email, password):
        payload = {"username": username, "email": email, "password": password}
        return self.api_client.post("/auth/register", json=payload)

