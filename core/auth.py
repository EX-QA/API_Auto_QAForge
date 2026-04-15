from typing import Optional, Dict
from .api_client import APIClient


class AuthManager:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self._token: Optional[str] = None

    def login(self, username: str, password: str, login_path: str = "/auth/login") -> Dict:
        payload = {"username": username, "password": password}
        response = self.api_client.post(login_path, json=payload)
        response.raise_for_status()
        data = response.json()
        self._token = data.get("token") or data.get("access_token")
        if self._token:
            self.set_bearer_token(self._token)
        return data

    def set_bearer_token(self, token: str):
        self._token = token
        self.api_client.set_header("Authorization", f"Bearer {token}")

    def set_api_key(self, key: str, header_name: str = "X-API-Key"):
        self.api_client.set_header(header_name, key)

    def logout(self):
        if self._token:
            self.api_client.remove_header("Authorization")
            self._token = None

    @property
    def token(self) -> Optional[str]:
        return self._token
